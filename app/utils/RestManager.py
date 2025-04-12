import json
from flask import request, jsonify
from app.PrivacyAndLogic import PrivacyAndLogic
from app.interfaces.messageHandler import MessageHandler
from app.utils.logger import get_logger

# Initialize the logger
logger = get_logger('app.RestAPIHandler')


class RestAPIHandler(MessageHandler):
    def __init__(self, FactoryObj, app):
        self.factory = FactoryObj
        self.PAL = PrivacyAndLogic()

        @app.route('/receive', methods=['POST'])
        def receive():
            logger.info("Received POST request on /receive endpoint")

            body = request.get_json()
            logger.debug("=== RAW REQUEST BODY ===")
            logger.debug(json.dumps(body, indent=4))

            if body:
                try:
                    logger.info("Processing body with PrivacyAndLogic")
                    tmp_dict = self.PAL.process(body)

                    logger.debug("=== AFTER PrivacyAndLogic ===")
                    logger.debug(json.dumps(tmp_dict, indent=4))

                    tmp = json.dumps(tmp_dict)
                    logger.info("Executing command with Factory")
                    response = self.factory.execute_command(tmp)

                    logger.debug("=== FACTORY RESPONSE ===")
                    logger.debug(json.dumps(response, indent=4) if isinstance(response, dict) else str(response))

                    if response:
                        logger.info(f"Response sent: {response}")
                        return str(response)
                    else:
                        logger.error("Invalid command, no valid response from factory.")
                        return {"status": "error", "message": "Invalid command"}
                except Exception as e:
                    logger.error(f"Error processing request: {str(e)}")
                    return {"status": "error", "message": f"Processing error: {str(e)}"}
            else:
                logger.error("No JSON payload received in request")
                return {"status": "error", "message": "No JSON payload"}

    def send_message(self, message: str):
        logger.info(f"Sent message: {message}")

    def receive_messages(self):
        logger.info("REST handler is ready and waiting for POST requests.")

    def lifeCheck(self):
        logger.info("Life check for RestAPIHandler is successful.")
        return [True, "rest"]
