from flask import Flask, jsonify
from app.utils.BrockerManager import BrokerM
from app.utils.RestManager import RestAPIHandler
from app.utils.factory import Factory
from app.utils.configurator import Configurator
from app.utils import SettingsTMP
from app.utils.logger import get_logger

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


if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)
