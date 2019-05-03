logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'consoleFormatter': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s | %(message)s'
        },
        'outputFormatter': {
            'format': '%(label)-10s |%(mention)-50s |%(tp_fn_entity)-50s |%(sentence)-256s'
        }
    },
    'handlers': {
        'consoleHandler': {
            'level': 'INFO',
            'formatter': 'consoleFormatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'fileHandler': {
            'level': 'INFO',
            'formatter': 'outputFormatter',
            'class': 'logging.FileHandler',
            'filename': 'logs/classifiers.log',
            'mode': 'w',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {   # root logger
            'handlers': ['consoleHandler'],
            'level': 'NOTSET',
            'propagate': True
        },
        'sampleOutput': {
            'handlers': ['fileHandler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}