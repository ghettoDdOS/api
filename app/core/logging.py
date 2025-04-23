import logging
import logging.config


def setup_logging(level: int = logging.INFO) -> None:
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {'default': {'format': '%(message)s'}},
        'handlers': {
            'rich_handler': {
                'formatter': 'default',
                'class': 'rich.logging.RichHandler',
                'show_time': False,
                'rich_tracebacks': True,
                'markup': True,
                'show_path': False,
            }
        },
        'loggers': {
            'app': {
                'level': level,
                'handlers': ['rich_handler'],
                'propagate': False,
            }
        },
    })
