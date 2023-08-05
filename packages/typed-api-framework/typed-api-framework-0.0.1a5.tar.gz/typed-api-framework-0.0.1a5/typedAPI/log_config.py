import logging
import sys
import os

class CustomFormatter(logging.Formatter):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    def format(self, record):
        # Replace the original pathname with one that doesn't include the base directory.
        record.pathname = os.path.relpath(record.pathname, self.base_dir)
        record.pathname = record.pathname.replace(os.sep, '.').rsplit('.', 1)[0]

        return super().format(record)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(funcName)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.getLogger().handlers[0].setFormatter(CustomFormatter(
    '%(levelname)-8s %(pathname)s:%(funcName)s:%(lineno)-40d %(message)s'
))

# Log some messages
logging.debug('This is a debug message')
logging.info('This is an informational message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')