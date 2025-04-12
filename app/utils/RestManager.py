import json
from flask import request, jsonify
from prometheus_client import Counter, Histogram
from app.PrivacyAndLogic import PrivacyAndLogic
from app.interfaces.messageHandler import MessageHandler
from app.utils.logger import get_logger
import time

# Initialize the logger
logger = get_logger('app.RestAPIHandler')

# Define Prometheus metrics
REQUEST_COUNT = Counter('rest_api_requests_total', 'Total number of requests to the /receive endpoint', ['status'])
REQUEST_LATENCY = Histogram('rest_api_request_duration_seconds', 'Histogram of latency for requests to /receive endpoint', ['status'])

class RestAPIHandler(MessageHandler):
    def __init__(self, FactoryObj, app):
        self.factory = FactoryObj
        self.PAL = PrivacyAndLogic()

        @app.route('/receive', methods=['POST'])
        def receive():
            # Start measuring the request latency
            start_time = time.time()

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

                    # Measure request latency
                    duration = time.time() - start_time
                    REQUEST_LATENCY.labels(status='success').observe(duration)

                    if response:
                        logger.info(f"Response sent: {response}")
                        REQUEST_COUNT.labels(status='success').inc()
                        return str(response)
                    else:
                        logger.error("Invalid command, no valid response from factory.")
                        REQUEST_COUNT.labels(status='error').inc()
                        return {"status": "error", "message": "Invalid command"}
                except Exception as e:
                    logger.error(f"Error processing request: {str(e)}")
                    # Measure request latency for error response
                    duration = time.time() - start_time
                    REQUEST_LATENCY.labels(status='error').observe(duration)
                    REQUEST_COUNT.labels(status='error').inc()
                    return {"status": "error", "message": f"Processing error: {str(e)}"}
            else:
                logger.error("No JSON payload received in request")
                # Measure request latency for error response
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(status='error').observe(duration)
                REQUEST_COUNT.labels(status='error').inc()
                return {"status": "error", "message": "No JSON payload"}

    def send_message(self, message: str):
        logger.info(f"Sent message: {message}")

    def receive_messages(self):
        logger.info("REST handler is ready and waiting for POST requests.")

    def lifeCheck(self):
        logger.info("Life check for RestAPIHandler is successful.")
        return [True, "rest"]
