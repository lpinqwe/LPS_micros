from flask import Flask, jsonify
from app.utils.BrockerManager import BrokerM
from app.utils.RestManager import RestAPIHandler
from app.utils.factory import Factory
from app.utils.configurator import Configurator
from app.utils import SettingsTMP
from app.utils.logger import get_logger
from prometheus_client import start_http_server, Counter, Summary
from prometheus_client import generate_latest


# Initialize the logger
logger = get_logger('app.run')

app = Flask(__name__)
configurator = Configurator("config.json")

# Initialize the factory and broker components
factory = Factory()

if SettingsTMP.Brocker == "rabbit":
    broker = BrokerM(factory)
    logger.info("Broker set to RabbitMQ")
else:
    broker = RestAPIHandler(factory, app)
    logger.info("Broker set to REST API")

# List of objects for health check
objList = [factory, broker]

# Initialize Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Summary('http_request_duration_seconds', 'Duration of HTTP requests in seconds',
                           ['method', 'endpoint'])


# Health check route with Prometheus metrics
@app.route('/health', methods=['GET'])
def lifecheck():
    logger.info("Health check initiated")
    resp = ""

    for obj in objList:
        logger.debug(f"Performing life check on {obj.__class__.__name__}")
        respond = obj.lifeCheck()

        if respond[0] != True:
            logger.error(f"Health check failed for {obj.__class__.__name__}: {respond}")
            resp += str(respond)

    if resp == "":
        logger.info("Health check successful")
        return "ok", 200
    else:
        logger.error(f"Health check failed with details: {resp}")
        return jsonify({"status": "error", "details": resp}), 500


# Metrics endpoint for Prometheus
@app.route('/metrics')
def metrics():
    # Increment the request count for the /metrics endpoint
    REQUEST_COUNT.labels(method='GET', endpoint='/metrics').inc()
    return generate_latest()


if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)

    # Start the Flask app
    logger.info("Starting Flask application")
    app.run(debug=True)
