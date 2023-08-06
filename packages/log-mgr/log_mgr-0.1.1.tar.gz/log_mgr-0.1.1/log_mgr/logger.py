""" Logger management """
import os
import sys
import shutil
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import time
from enum import Enum


class LoggerMode(Enum):
    """ Enum class for logger modes """
    NONE = 0
    FILE = 1
    STD = 2
    BOTH = 3


class UTCFormatter(logging.Formatter):
    """ Class for formatter """
    converter = time.gmtime


class Logger():
    """ Logger class with builtin handler configuration. 
        Must be used only from the root application to define the handlers and other parameters
        In the inner libraries logging.getLogger() should be used.
        Also can be used by inner libraries, if they want for some reason a different log configuration or handlers.
        """
    def __init__(self, package_name: str,
                 log_file_name: str,
                 log_name: str = None,
                 mode: LoggerMode = LoggerMode.FILE,
                 level=logging.INFO,
                 utc: bool = False,
                 dry_run: bool = False):
        """ Init of the class
        Args:
            package_name (str): Root package name, to put the logs into the right /var/log/ subfolder
            log_file_name (str): Log file name. Just the name of the file itself
            mode (LoggerMode, optional): 
            level (_type_, optional): Logging level to be used for all handlers
            utc (bool, optional): _description_. Defaults to False.
            dry_run (bool, optional): _description_. Defaults to False.
        """
        self.log_file_name = log_file_name

        self.homevar = os.path.join(str(Path.home()), 'var', 'log', package_name)
        self.package_name = package_name

        if not os.path.exists(self.homevar):
            os.makedirs(self.homevar)

        if dry_run:
            self.dry_run = True
            self.homevar = os.path.join(self.homevar, 'dryrun_log')
            if not os.path.exists(self.homevar):
                os.makedirs(self.homevar)
        else:
            self.dry_run = False

        self.setup_logger(log_name, mode, level, utc)

    def __del__(self):
        logging.shutdown() # Shutdown logger, otherwise we cannot rmtree because files are still opened
        if self.dry_run and os.path.exists(self.homevar):
            shutil.rmtree(self.homevar)

    def __getattr__(self, name):
        """ Inherits and delegates all the functions from logging.logger (i.e. info, debug, warning, error methods)
        Args:
            name (str): Name of the property to be delegated
        Returns:
            _type_: The delegated result
        """
        return getattr(self.logger, name)

    def get_log_path(self) -> str:
        """ Returns the log path based on the homevar folder and the log file name specified"""
        return os.path.join(self.homevar, f"{self.log_file_name}.log")

    def setup_logger(self, log_name: str, mode: LoggerMode, level, utc: bool):
        """ Setup the selected mode, that means which builtin handlers will be added to the logger """
        self.logger = logging.getLogger(log_name)

        if not os.path.exists(self.homevar):
            os.mkdir(self.homevar)

        if utc:
            formatter = UTCFormatter('%(asctime)s-%(filename)s-%(message)s', '%Y-%m-%d %H:%M:%S')
        else:
            formatter = logging.Formatter('%(asctime)s-%(filename)s-%(message)s', '%Y-%m-%d %H:%M:%S')

        # Create rotating file handler
        if mode in [LoggerMode.FILE, LoggerMode.BOTH]:
            file_handler = RotatingFileHandler(self.get_log_path(), maxBytes=10000, backupCount=10)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Create stdout stream handler
        if mode in [LoggerMode.STD, LoggerMode.BOTH]:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        # Create empty log file if it doesn´t previously exist
        if not os.path.exists(self.get_log_path()):
            with open(self.get_log_path(), 'w', encoding='UTF-8'):
                pass

        # Same level in both handlers
        self.logger.setLevel(level)

    def get_log(self) -> str:
        """ Get log file content """
        with open(self.get_log_path(), 'r', encoding='UTF-8') as file:
            return file.read()

    def get_log_lines(self) -> str:
        """ Get log file content split in lines"""
        with open(self.get_log_path(), 'r', encoding='UTF-8') as file:
            return file.readlines()
