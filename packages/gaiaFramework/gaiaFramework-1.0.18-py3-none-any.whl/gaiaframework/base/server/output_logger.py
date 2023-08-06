from typing import Union, List

import logging
import sys
import time
from pythonjsonlogger import jsonlogger

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
root.addHandler(handler)

logger = logging.getLogger(__name__)

class OutputLogger:
    def __init__(self, endpoint) -> None:
        self.data = None
        self.host = None
        self.service_account = None
        self.endpoint = endpoint

    def save_request_info(self, data, host, service_account) -> None:
        self.data = data
        self.host = host
        self.service_account = service_account

    def log_output(self, output, retrieve_type='', pipeline_timing=None, predictable_object_count=None):

        extra_info = dict(input=self.data, output=output, from_host=self.host,
                          from_service_account=self.service_account,)
        if pipeline_timing:
            extra_info.update({"pipeline_exec_time": pipeline_timing,
                               "predictable_object_count": predictable_object_count})
        logger.info(f"INFO {self.endpoint} invoked {retrieve_type}", extra=extra_info)

    def log_output_company(self, output, retrieve_type='', company=None, pipeline_timing=None, predictable_object_count=None):

        extra_info = dict(input=self.data, output=output, from_host=self.host,
                          from_service_account=self.service_account)
        if pipeline_timing:
            extra_info.update({"pipeline_exec_time": pipeline_timing,
                               "predictable_object_count": predictable_object_count})
        if company and 'name' in company:
            extra_info.update({"company": company['name']})
        logger.info(f"INFO {self.endpoint} invoked {retrieve_type}", extra=extra_info)

    def log(self, level, message, extra=None):
        if extra is not None:
            if isinstance(extra, str):
                extra = {"message": extra}
            elif isinstance(extra, dict):
                extra = extra.copy()
            else:
                extra = None

        logger.log(level, f'{logging.getLevelName(level).upper()} - {self.endpoint} - {message}', extra=extra)

    def debug(self, message, extra=None):
        self.log(logging.DEBUG, message, extra=extra)

    def info(self, message, extra=None):
        self.log(logging.INFO, message, extra=extra)

    def warning(self, message, extra=None):
        self.log(logging.WARNING, message, extra=extra)

    def error(self, message, extra=None):
        self.log(logging.ERROR, message, extra=extra)

    def exception(self, message, extra=None):
        self.log(logging.ERROR, message, extra=extra)