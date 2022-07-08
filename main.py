import logging
import argparse

# logger
parser = argparse.ArgumentParser()
parser.add_argument("--logs", help="Set log level")
args = parser.parse_args()
log_level=args.logs or "info"

numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % log_level)

logging.basicConfig(level=numeric_level)

from src.router.request_handler import RH

from flask import Flask

app = Flask(__name__)

app.register_blueprint(RH, url_prefix="/v1")

if __name__ == "__main__":
    app.logger.info("Running on un-secure port: %s" % 10000)
    app.run(host="127.0.0.1", port=10000)