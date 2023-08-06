#
# Copyright (c) 2023 Macrometa Corp All rights reserved.
#

#!/usr/bin/env python3
import argparse
import asyncio
import io
import json
import pymongo
import sys
import uuid
from asyncio import AbstractEventLoop
from datetime import datetime
from pathlib import Path
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
from threading import Thread, Lock
from typing import Dict
from urllib import parse

import jsonschema
from adjust_precision_for_schema import adjust_decimal_precision_for_schema
from jsonschema import Draft4Validator
from singer import get_logger

logger = get_logger('macrometa_target_mongo')

DEFAULT_BATCH_SIZE_ROWS = 1000
DEFAULT_BATCH_FLUSH_INTERVAL = 60
DEFAULT_MIN_BATCH_FLUSH_TIME_GAP = 60


class RecordBatch:
    """Class wrapping the record batch in order to make it thread safe."""

    def __init__(self, config: dict):
        self._list = list()
        self._lock = Lock()
        self.interval = config.get('batch_flush_interval', DEFAULT_BATCH_FLUSH_INTERVAL)
        self.last_executed_time = datetime.now()
        self.min_time_gap = config.get('batch_flush_min_time_gap', DEFAULT_MIN_BATCH_FLUSH_TIME_GAP)
        self.max_batch_size = config.get('batch_size_rows', DEFAULT_BATCH_SIZE_ROWS)

    def append(self, value) -> None:
        """Acquire the lock and add a record to the list."""
        with self._lock:
            self._list.append(value)

    def length(self) -> int:
        """Acquire the lock and return the number of items in the list."""
        with self._lock:
            return len(self._list)

    def flush(self) -> list:
        """Acquire the lock, create a copy of the existing batch,
        clear the existing batch, and return the copy."""
        with self._lock:
            c = self._list.copy()
            self._list.clear()
            return c


def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()


def try_upsert(collection, record_batch: RecordBatch, hard_delete=False, force=False):
    if record_batch.length() >= record_batch.max_batch_size or (force and record_batch.length() > 0):
        to_upsert = record_batch.flush()
        operations = []

        for record in to_upsert:
            if '_id' in record:
                record_filter = {'_id': record.pop('_id')}
            else:
                # If no key property is available just insert the record as it is
                record_filter = {'_id': {'$exists': False}}
            operations.append(UpdateOne(record_filter, {'$set': record}, upsert=True))
        try:
            if operations:
                count_upsert = len(operations)
                logger.info(f"Upserting {count_upsert} records into {collection.full_name}.")
                collection.bulk_write(operations, ordered=False)
                logger.info(f"{count_upsert} records upserted into {collection.full_name}.")
        except BulkWriteError as bwe:
            write_errors = bwe.details['writeErrors']
            for error in write_errors:
                failed_operation = operations[error['index']]
                logger.warn(f"Failed upsert operation: {failed_operation}, Error: {error['errmsg']}")
        except Exception as e:
            logger.warn(f"Failed to upsert records: {e}.")
        if hard_delete:
            try_delete(collection)
        record_batch.last_executed_time = datetime.now()


def try_delete(collection):
    try:
        collection.delete_many({"_sdc_deleted_at":{"$ne":None}})
        logger.info(f"Deleted records with field _sdc_deleted_at not equal to null.")
    except Exception as e:
        logger.warn(f"Failed to delete records. {e}")


def persist_messages(collection, messages: io.TextIOWrapper, record_batch: RecordBatch, hard_delete: bool):
    state = None
    schemas = {}
    key_properties = {}
    validators = {}

    for message in messages:
        try:
            o = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            logger.error(f"Unable to parse:\n{message}")
            raise e

        message_type = o['type']
        if message_type == 'RECORD':
            stream = o['stream']
            if stream not in schemas:
                raise Exception(f"A record for stream {stream} was encountered before a corresponding schema")

            try:
                validators[stream].validate((o['record']))
            except jsonschema.ValidationError as e:
                logger.error(f"Failed parsing the json schema for stream: {stream}.")
                raise e

            rec = o['record']
            try:
                kps = key_properties[stream]
                if len(kps) > 1:
                    logger.warn(f'Multiple key_properties found ({",".join(kps)}).'
                                f' Only `{kps[0]}` will be considered.')
                elif len(kps) == 0:
                    logger.debug(f"key_properties not found for stream: {stream}")

                if kps:
                    _id = rec[kps[0]]
                    rec['_id'] = _id
            except:
                _id = None

            if '_sdc_deleted_at' in rec and not rec['_sdc_deleted_at']:
                rec.pop('_sdc_deleted_at', None)
            record_batch.append(rec)
            state = None
            try_upsert(collection, record_batch, hard_delete)
        elif message_type == 'STATE':
            logger.debug('Setting state to {}'.format(o['value']))
            state = o['value']
        elif message_type == 'SCHEMA':
            stream = o['stream']
            schemas[stream] = o['schema']
            adjust_decimal_precision_for_schema(schemas[stream])
            validators[stream] = Draft4Validator((o['schema']))
            key_properties[stream] = o['key_properties']
        else:
            logger.warning("Unknown message type {} in message {}".format(o['type'], o))
    return state


def setup_batch_task(collection, record_batch: RecordBatch, hard_delete) -> AbstractEventLoop:
    event_loop = asyncio.new_event_loop()
    Thread(target=start_background_loop, args=(event_loop,), daemon=True).start()
    asyncio.run_coroutine_threadsafe(process_batch(collection, record_batch, hard_delete), event_loop)
    return event_loop


async def process_batch(collection, record_batch: RecordBatch, hard_delete) -> None:
    while True:
        await asyncio.sleep(record_batch.interval)
        timedelta = datetime.now() - record_batch.last_executed_time
        if timedelta.total_seconds() >= record_batch.min_time_gap:
            # if batch has records that need to be processed but haven't reached batch size then process them.
            try_upsert(collection, record_batch, hard_delete, force=True)


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

def create_certficate_files(config: Dict) -> Dict:
    path_uuid = uuid.uuid4().hex
    try:
        if config.get('tls_ca_file'):
            path = f"/opt/mongo/{path_uuid}/ca.pem"
            ca_cert = Path(path)
            ca_cert.parent.mkdir(exist_ok=True, parents=True)
            ca_cert.write_text(create_ssl_string(config['tls_ca_file']))
            config['tls_ca_file'] = path
            logger.info(f"CA certificate file created at: {path}")

        if config.get('tls_certificate_key_file'):
            path = f"/opt/mongo/{path_uuid}/client.pem"
            client_cert = Path(path)
            client_cert.parent.mkdir(exist_ok=True, parents=True)
            client_cert.write_text(create_ssl_string(config['tls_certificate_key_file']))
            config['tls_certificate_key_file'] = path
            logger.info(f"Client certificate file created at: {path}")
    except Exception as e:
        logger.warn(f"Failed to create certificate: /opt/mongo/{path_uuid}/. {e}")
    return config

def delete_certficate_files(config: Dict) -> None:
    try:
        cert = None
        if config.get('tls_ca_file'):
            path = config['tls_ca_file']
            cert = Path(path)
            config['tls_ca_file'] = cert.read_text()
            cert.unlink()
            logger.info(f"CA certificate file deleted from: {path}")

        if config.get('tls_certificate_key_file'):
            path = config['tls_certificate_key_file']
            cert = Path(path)
            config['tls_certificate_key_file'] = cert.read_text()
            cert.unlink()
            logger.info(f"Client certificate file deleted from: {path}")

        if cert is not None:
            cert.parent.rmdir()
    except Exception as e:
        logger.warn(f"Failed to delete certificate: {e}")

def create_ssl_string(ssl_string: str) -> str:
    tls_certificate_key_list = []
    split_string = ssl_string.split("-----")
    if len(split_string) < 4:
        raise Exception("Invalid PEM format for certificate.")
    for i in range(len(split_string)):
        if((i % 2) == 1):
            tls_certificate_key_list.append("-----")
            tls_certificate_key_list.append(split_string[i])
            tls_certificate_key_list.append("-----")
        else:
            tls_certificate_key_list.append(split_string[i].replace(' ', '\n'))
    
    tls_certificate_key_file = ''.join(tls_certificate_key_list)
    return tls_certificate_key_file

def get_connection_string(config: dict):
    """
    Generates a MongoClientConnectionString based on configuration
    Args:
        config: DB config
    Returns: A MongoClient connection string
    """
    srv = config.get('srv', False)

    # Default SSL verify mode to true, give option to disable
    verify_mode = config.get('verify_mode', True)
    use_ssl = config.get('ssl', False)

    direct_connection = config.get('direct_connection', False)

    connection_query = {
        'readPreference': 'secondaryPreferred',
        'authSource': config['auth_database'],
    }

    if config.get('replica_set'):
        connection_query['replicaSet'] = config['replica_set']

    if use_ssl:
        connection_query['tls'] = 'true'
        if config.get('tls_ca_file'):
            connection_query['tlsCAFile'] = config['tls_ca_file']
        if config.get('tls_certificate_key_file'):
            connection_query['tlsCertificateKeyFile'] = config['tls_certificate_key_file']
            if config.get('tls_certificate_key_file_password'):
                connection_query['tlsCertificateKeyFilePassword'] = config['tls_certificate_key_file_password']

    if direct_connection:
        connection_query['directConnection'] = 'true'

    # NB: "sslAllowInvalidCertificates" must ONLY be supplied if `SSL` is true.
    if not verify_mode and use_ssl:
        connection_query['tlsAllowInvalidCertificates'] = 'true'

    query_string = parse.urlencode(connection_query)

    port = "" if srv else f":{int(config['port'])}"

    connection_string = f'{"mongodb+srv" if srv else "mongodb"}://{parse.quote(config["user"])}:' \
                        f'{parse.quote(config["password"])}@{config["host"]}' \
                        f'{port}/{config["database"]}?{query_string}'

    return connection_string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()
    if args.config:
        with open(args.config) as input_json:
            config = json.load(input_json)
    else:
        raise Exception("Required '--config' parameter was not provided")

    try:
        config = create_certficate_files(config)
        connection_string = get_connection_string(config)
        db_name = config.get("database")
        target_collection = config.get("target_collection")
        hard_delete = config.get("hard_delete", False)

        client = pymongo.MongoClient(connection_string)
        db = client[db_name]
        collection = db[target_collection]
        record_batch = RecordBatch(config)
        event_loop = setup_batch_task(collection, record_batch, hard_delete)
        input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        state = persist_messages(collection, input_messages, record_batch, hard_delete)
        # There can still be records in the `record_batch` which is not processed,
        # So, we have to force process it one last time before the workflow terminates.
        try_upsert(collection, record_batch, hard_delete, force=True)
        emit_state(state)
        event_loop.stop()
        logger.info("Exiting normally...")
    except Exception as e:
        delete_certficate_files(config)
        raise e
    delete_certficate_files(config)


if __name__ == '__main__':
    main()
