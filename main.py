import os
import logging
from logging.handlers import TimedRotatingFileHandler
import argparse

from Config import baseConfig
config = baseConfig()
api = config["API"]

# logger
parser = argparse.ArgumentParser()
parser.add_argument("--logs", help="Set log level")
args = parser.parse_args()
log_level=args.logs or "info"

numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % log_level)

if not os.path.exists("logs/"):
        os.makedirs("logs/")

logging.basicConfig(level=numeric_level)

rotatory_handler = TimedRotatingFileHandler(
    "logs/combined.log", when="D", interval=1, backupCount=30
)
rotatory_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s", "%m-%d-%Y %H:%M:%S"
)
rotatory_handler.setFormatter(formatter)

from src.router.request_handler import RH

from flask import Flask

app = Flask(__name__)

app.register_blueprint(RH, url_prefix="/v1")

logger = logging.getLogger()

logger.addHandler(rotatory_handler)

logger.info("Log_Level: %s" % log_level.upper())

if __name__ == "__main__":
    app.logger.info("Running on un-secure port: %s" % api['PORT'])
    app.run(host=api['HOST'], port=api['PORT'])