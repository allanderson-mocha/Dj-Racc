import os
import logging
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

DISCORD_SECRET_API = os.getenv("DISCORD_API_TOKEN")
YOUTUBE_API = os.getenv("YOUTUBE_API")
SPOTIFY_ID = os.getenv("SPOTIFY_ID")
SPOTIFY_SECRET = os.getenv('SPOTIFY_SECRET')

logging_config = {
    "version" : 1,
    "disabled_existing_Loggers": False,
    "formatters":{
        "verbose":{
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(messsage)s"
        },
        "standard":{
            "format": "%(levelname)-10s - %(name)-15s : %(messsage)s"
        }
    },
    "handlers":{
        "console":{
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2":{
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "file":{
            'level': "INFO",
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w"
        },
    },
    "loggers":{
        "bot":{
            'handlers': ['console'],
            "level": "INFO",
            "propagate": False
        },
        "discord":{
            'handlers': ['console2', "file"],
            "level": "INFO",
            "propagate": False
        }
    }

}

dictConfig(logging_config)