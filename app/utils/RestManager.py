# app/utils/RestManager.py
import json
from flask import request, jsonify
from app.PrivacyAndLogic import PrivacyAndLogic
from app.interfaces.messageHandler import MessageHandler


class RestAPIHandler(MessageHandler):
    def __init__(self, FactoryObj, app):
        self.factory = FactoryObj
        self.PAL = PrivacyAndLogic()

        @app.route('/receive', methods=['POST'])
        def receive():
            body = request.get_json()
            print("=== RAW REQUEST BODY ===")
            print(json.dumps(body, indent=4))

            if body:
                tmp_dict = self.PAL.process(body)

                print("=== AFTER PrivacyAndLogic ===")
                print(json.dumps(tmp_dict, indent=4))

                tmp = json.dumps(tmp_dict)
                response = self.factory.execute_command(tmp)

                print("=== FACTORY RESPONSE ===")
                print(json.dumps(response, indent=4) if isinstance(response, dict) else str(response))

                if response:
                    return str(response)
                return {"status": "error", "message": "Invalid command"}
            return {"status": "error", "message": "No JSON payload"}

    def send_message(self, message: str):
        print(f"Sent message: {message}")

    def receive_messages(self):
        print("REST handler is ready and waiting for POST requests.")

    def lifeCheck(self):
        return [True, "rest"]
