# run.py or __init__.py
import threading

from flask import Flask, jsonify
from app.utils.RestManager import RestAPIHandler
from app.utils.factory import Factory
from app.utils.configurator import Configurator
from app.utils.BrockerManager import BrockerM
app = Flask(__name__)
#configurator = Configurator("config.json")
#configurator.configure()
factory = Factory()
broker = RestAPIHandler(factory, app)
#
#
# broker =BrockerM(factory)
# def runAll():
#     thread_msg = threading.Thread(target=broker.start_consuming)
#     thread_msg.start()
#
# runAll()


broker.receive_messages()
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
