import json
import logging
from flask import request, jsonify
from app.PrivacyAndLogic import PrivacyAndLogic
from app.interfaces.messageHandler import MessageHandler


class RestAPIHandler(MessageHandler):
    def __init__(self, FactoryObj, app):
        self.factory = FactoryObj
        self.PAL = PrivacyAndLogic()

        # Set up logging configuration
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

        @app.route('/receive', methods=['POST'])
        def receive():
            self.logger.info("Received request")

            body = request.get_json()
            self.logger.debug(f"=== RAW REQUEST BODY ===\n{json.dumps(body, indent=4)}")

            if body:
                tmp_dict = self.PAL.process(body)
                self.logger.debug(f"=== AFTER PrivacyAndLogic ===\n{json.dumps(tmp_dict, indent=4)}")

                tmp = json.dumps(tmp_dict)
                response = self.factory.execute_command(tmp)

                self.logger.debug(
                    f"=== FACTORY RESPONSE ===\n{json.dumps(response, indent=4) if isinstance(response, dict) else str(response)}")

                if response:
                    self.logger.info(f"Response sent: {str(response)}")
                    return str(response)
                else:
                    self.logger.warning("Invalid command in factory response")
                    return {"status": "error", "message": "Invalid command"}
            else:
                self.logger.warning("No JSON payload received")
                return {"status": "error", "message": "No JSON payload"}

    def send_message(self, message: str):
        self.logger.info(f"Sent message: {message}")

    def receive_messages(self):
        self.logger.info("REST handler is ready and waiting for POST requests.")

    def lifeCheck(self):
        self.logger.info("Life check successful.")
        return [True, "rest"]
