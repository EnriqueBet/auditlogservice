import sys
import logging

from api.v1 import config

class Logger:
    _instance = None

    @staticmethod
    def get_instance():
        # TODO: Add service logging handler if needed
        if __class__._instance is None:
            formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
            sysout_handler = logging.StreamHandler(sys.stdout)
            sysout_handler.setFormatter(formatter)
            __class__._instance = logging.getLogger()
            __class__._instance.addHandler(sysout_handler)
            __class__._instance.setLevel(config.LOGGING_LEVEL)
        return __class__._instance
