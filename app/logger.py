import logging
import json
import os
import traceback
import contextvars
from logstash_async.handler import AsynchronousLogstashHandler

request_headers = contextvars.ContextVar('request_headers')

def is_prod_mode():
    if os.getenv('PROD_MODE') is not None:
        logging.getLogger().info("Production mode")
        return True
    else:
        logging.getLogger().info("Developer mode")
        return False

def init_logger():
    handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    ) if is_prod_mode() else logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=logging.INFO if is_prod_mode() else logging.DEBUG,
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [handler]
    )

    logging.getLogger().info(f"Prod mode: {is_prod_mode()}")

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