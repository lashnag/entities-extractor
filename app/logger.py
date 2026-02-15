import logging
import json
import os
import sys
import traceback
import contextvars
from logstash_async.handler import AsynchronousLogstashHandler

request_headers = contextvars.ContextVar('request_headers')

def is_remote_logger():
    return os.getenv('REMOTE_LOGGER') is not None

def init_logger():
    handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    ) if is_remote_logger() else logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging_level = logging.INFO if is_remote_logger() else logging.DEBUG

    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    root_logger.handlers = []
    root_logger.addHandler(handler)

    logging.basicConfig(
        level=logging_level,
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [handler]
    )

    mode = "Remote" if is_remote_logger() else "Local"
    logging.getLogger().info(f"{mode} logger initialized. Prod mode: {is_remote_logger()}")
    print(f"{mode} logger initialized. Prod mode: {is_remote_logger()}. Using print")

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