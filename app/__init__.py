# run.py or __init__.py

from flask import Flask, jsonify
from app.utils.BrockerManager import BrokerM
from app.utils.RestManager import RestAPIHandler
from app.utils.factory import Factory
from app.utils.configurator import Configurator

app = Flask(__name__)
configurator = Configurator("config.json")
configurator.configure()
factory = Factory()
broker = RestAPIHandler(factory, app)
# broker = BrokerM(factory)  # <-- если хочешь переключиться на RabbitMQ

objList = [factory, broker]

@app.route('/health', methods=['GET'])
def lifecheck():
    resp = ""
    for obj in objList:
        respond = obj.lifeCheck()
        if respond[0] != True:
            resp += str(respond)

    if resp == "":
        return "ok", 200
    return jsonify({"status": "error", "details": resp}), 500

if __name__ == '__main__':
    app.run(debug=True)
