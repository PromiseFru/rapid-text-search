import logging
logger = logging.getLogger(__name__)

from flask import Blueprint
from flask import jsonify
from flask import request

RH = Blueprint("request_handler", __name__)

@RH.route("/inbound", methods=["POST"])
def rst_inbound():
    try:
        body = request.json
        
        return body, 200
    except Exception as error:
        logger.exception(error)

        return error, 500