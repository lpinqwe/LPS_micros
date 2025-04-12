import json
import os
import threading
import pika
from app.PrivacyAndLogic import PrivacyAndLogic
from app.interfaces.messageHandler import MessageHandler
from app.utils import SettingsTMP
from app.utils.logger import get_logger

# Initialize the logger
logger = get_logger('app.BrokerM')


class BrokerM(MessageHandler):
    channel = None
    connection = None
    factory = None
    consumerThread = None
    PAL = PrivacyAndLogic()

    def lifeCheck(self):
        try:
            if self.connection:
                logger.info("Broker connection is live.")
                return [True, "brocker"]
            logger.warning("Broker connection is not established.")
            return [False, "brocker"]
        except Exception as e:
            logger.error(f"Error in lifeCheck: {str(e)}")
            return [e, "broker"]

    def __init__(self, FactoryObj):
        self.factory = FactoryObj
        try:
            rabbitmq_host = os.getenv('RABBITMQ_HOST', '127.0.0.1')
            rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
            rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
            rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')

            logger.info(f"Connecting to RabbitMQ at {rabbitmq_host}:{rabbitmq_port} with user {rabbitmq_user}")

            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
            connection_params = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                credentials=credentials
            )

            self.connection = pika.BlockingConnection(connection_params)
            self.channel = self.connection.channel()

            self.channel.queue_declare(queue=SettingsTMP.RABBITMQ_QUEUE_post)
            self.channel.queue_declare(queue=SettingsTMP.RABBITMQ_QUEUE_get)
            logger.info("RabbitMQ connection established successfully.")

        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise

    def send_message(self, message: str):
        try:
            self.channel.basic_publish(exchange='', routing_key=SettingsTMP.RABBITMQ_QUEUE_post, body=message)
            logger.info(f" [x] Sent message: {message}")
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")

    def receive_messages(self):
        try:
            logger.info("Start consuming messages.")
            self.consumerThread = threading.Thread(target=self.receive_messages)
            self.consumerThread.start()
        except Exception as e:
            logger.error(f"Error while starting consumer thread: {str(e)}")

    def callback(self, ch, method, properties, body):
        logger.info(f" [x] Received message: {body.decode()}")
        tmp = body.decode()

        try:
            tmp_dict = json.loads(tmp)
            logger.info("Message decoded successfully.")
            tmp_dict = self.PAL.process(tmp_dict)
            tmp = json.dumps(tmp_dict)
            logger.debug(f"Processed message: {tmp}")
        except json.JSONDecodeError:
            logger.error("Error decoding JSON message")

        try:
            tmp = self.factory.execute_command(tmp)
            if tmp:
                logger.info(f"Command executed successfully: {str(tmp)}")
                self.send_message(str(tmp))
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")

    def __del__(self):
        try:
            if self.connection:
                self.connection.close()
                logger.info("RabbitMQ connection closed.")
        except Exception as e:
            logger.error(f"Error closing connection: {str(e)}")
