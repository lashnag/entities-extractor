import logging
import json
import os
import sys
import traceback
import contextvars
from logstash_async.handler import AsynchronousLogstashHandler

request_headers = contextvars.ContextVar('request_headers')

def is_remote_logger():
    if os.getenv('REMOTE_LOGGER') is not None:
        logging.getLogger().info("Remote logger")
        return True
    else:
        logging.getLogger().info("Local logger")
        return False

def init_logger():
    handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    ) if is_remote_logger() else logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging_level = logging.INFO if is_remote_logger() else logging.DEBUG
    logging.basicConfig(
        level=logging_level,
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [handler]
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    root_logger.addHandler(handler)

    logging.getLogger().info(f"Prod mode: {is_remote_logger()}")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'application': 'entities-extractor',
            'level': record.levelname,
            'message': record.getMessage(),
            'logger_name': record.filename,
        }
        if record.exc_info:
            log_obj['exception'] = ''.join(traceback.format_exception(*record.exc_info))

        headers = request_headers.get(None)
        if isinstance(headers, dict):
            for key, value in headers.items():
                if key.startswith('custom-'):
                    log_obj[key.removeprefix('custom-')] = value

        return json.dumps(log_obj)