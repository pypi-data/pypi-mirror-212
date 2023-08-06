""" Unit tests """
import unittest
import os
from pathlib import Path
import logging

from log_mgr import Logger, LoggerMode


class Testing(unittest.TestCase):
    """Unittesting class"""

    def test_000_log_file(self):
        """Test for logging to file
        """
        log_path = os.path.join(str(Path.home()), 'var', 'log', 'log_helper', 'dryrun_log', 'logtest.log')
        if os.path.exists(log_path):
            os.remove(log_path)

        logger = Logger('log_helper', 'logtest', mode=LoggerMode.FILE, level=logging.INFO, dry_run=True)

        self.assertEqual(log_path, logger.get_log_path())

        logger.debug('debug message')
        logger.info('info message')

        content = logger.get_log_lines()

        self.assertEqual(len(content), 1)

        skip_date = content[0].rstrip()[-12:]
        self.assertEqual(skip_date, 'info message')

if __name__ == "__main__":
    unittest.main()
