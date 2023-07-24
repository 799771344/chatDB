# coding: utf8
"""
日志
"""
import logging

from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.handlers.files import AsyncTimedRotatingFileHandler
from aiologger.handlers.streams import AsyncStreamHandler
from pathlib import Path
from common.file_path import file_path

BASE_DIR = Path().cwd()
LOG_FILE_PATH = "{}/log/%s.log".format(file_path)


class LogConfig:
    def __init__(self, log_file=LOG_FILE_PATH, log_name="run"):
        """异步日志，按日期切割"""
        log_file = log_file % log_name
        logger = Logger(name=log_name, level=logging.DEBUG)
        formatter = Formatter("%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s")
        logfile_path = Path(log_file)
        logfile_path.parent.mkdir(parents=True, exist_ok=True)
        logfile_path.touch(exist_ok=True)
        atr_file_handler = AsyncTimedRotatingFileHandler(
            filename=str(logfile_path),
            interval=1,
            backup_count=30,
            encoding="utf8"
        )
        atr_file_handler.formatter = formatter
        logger.add_handler(atr_file_handler)
        self.logger = logger


logger = LogConfig().logger
