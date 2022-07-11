import logging
logger = logging.getLogger(__name__)

import requests

from Config import baseConfig
config = baseConfig()
contacts = config["CONTACTS"]
smswithoutborders = config["SMSWITHOUTBORDERS"]

from flask import Blueprint
from flask import request

RH = Blueprint("request_handler", __name__)

from src.search_engines.wikipedia import Wikipedia

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import InternalServerError

class RequestHandler:
    def __init__(self, MSISDN: str) -> None:
        self.MSISDN = MSISDN

    def inbound(self, text: str) -> dict:
        """
        """
        filter_data = self.__filter__()
        logger.info({
                "text": "Search text is empty." if not text else text,
                "operator_name": filter_data["operator_name"],
                "MSISDN": filter_data["MSISDN"]
            })
        if filter_data:
            return {
                "text": "Search text is empty." if not text else text,
                "operator_name": filter_data["operator_name"],
                "MSISDN": filter_data["MSISDN"]
            }
        else:
            return None

    def outbound(self, text: str, MSISDN: str, operator_name: str) -> None:
        """
        """
        url = f"{smswithoutborders['OPENAPI_URL']}//v1/sms"
        auth_id = smswithoutborders["AUTH_ID"]
        data = {
                "auth_id":auth_id,
                "data": [{
                    "operator_name":operator_name,
                    "text":text,
                    "number":MSISDN
                    }],
                "callback_url": ""
                }

        try:
            res = requests.post(url=url, json=data)

            if res.status_code == 200:
                logger.info("MSISDN = %s" % MSISDN)
                logger.info("- Successfully sent.")
                return None
            else:
                logger.error("- Cannot send SMS")
                raise InternalServerError(res.text)        
        except Exception as error:
            raise InternalServerError(error)

    def __filter__(self) -> dict:
        """
        """
        if self.MSISDN in contacts["BLACKLIST"]:
            logger.error("- %s is in blacklist" % self.MSISDN)
            return None
        else:
            url = f"{smswithoutborders['OPENAPI_URL']}/v1/sms/operators"
            data = [{"text":"", "number": self.MSISDN}]

            try:
                res = requests.post(url=url, json=data)

                if res.status_code == 200:
                    logger.info("- Successfully filtered.")
                    res_data = res.json()[0]
                    return {
                        "operator_name": res_data["operator_name"],
                        "MSISDN": res_data["number"]
                    }
                else:
                    logger.error("- Cannot get operator_name")
                    raise InternalServerError(res.text)
            except Exception as error:
                raise InternalServerError(error)

@RH.route("/inbound", methods=["POST"])
def rst_inbound() -> None:
    """
    """
    try:    
        MSISDN = request.json["MSISDN"]
        text = request.json["text"]

        rh = RequestHandler(MSISDN=MSISDN)
        inbound = rh.inbound(text=text)

        if not inbound:
            return "", 200
        else:
            wikipedia = Wikipedia()
            text_result = wikipedia.page_search(text=inbound["text"])

            # rh.outbound(text=text_result, MSISDN=inbound["MSISDN"], operator_name=inbound["operator_name"])

            return text_result, 200

    except BadRequest as err:
        return str(err), 400

    except Unauthorized as err:
        return str(err), 401

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500