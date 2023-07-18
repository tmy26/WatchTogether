import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve.parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')

"""
This file contains developer loggers related to:
    - Users
"""

LOGGING = {
    'version' : 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'developer_format': {
            'format': '%(asctime)s | %(levelname)-8s | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'users': {
            'level': 'DEBUG',
            'class': 'loggingFileHandler',
            'formatter': 'developer_format',
            'filename': os.path.join(LOG_DIR, 'users_logging.log')
        }
    },
    'loggers': {
        'users': {
            'level': 'DEBUG',
            'handlers': ['console', 'users'],
            'propagate': False
        }
    }
}