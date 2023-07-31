import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')


"""
This file contains Developer loggers related to:
    - Users
"""

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'developer_format': {
            'format': '%(asctime)s | %(levelname)-8s | %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': os.path.join(LOG_DIR, 'logging_log.log')
        },
        'wt_mobile_dev': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'developer_format',
            'filename': os.path.join(LOG_DIR, 'dev_mobile_log.log')
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'wt_mobile_dev' : {
            'level': 'DEBUG',
            'handlers': ['console', 'wt_mobile_dev'],
            'propagate': False
        }
    }
}
