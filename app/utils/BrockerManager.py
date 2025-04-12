import json
import os
import threading

import pika

from app.PrivacyAndLogic import PrivacyAndLogic
from app.utils import SettingsTMP


class BrockerM:
    channel = None
    connection = None
    factory = None
    consumerThread = None
    PAL = PrivacyAndLogic()
    def lifeCheck(self):
        try:
            if self.connection:
                return [True,"brocker"]
            return [False,"brocker"]
        except (Exception) as e:
            return [e,"broker"]

    def __init__(self, FactoryObj):
        self.factory=FactoryObj
        try:
            # Получение конфигурации из переменных окружения
            rabbitmq_host = os.getenv('RABBITMQ_HOST', '127.0.0.1')
            #rabbitmq_host = "192.168.213.28"
            rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
            rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
            rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')

            print(f"Connecting to RabbitMQ at {rabbitmq_host}:{rabbitmq_port} with user {rabbitmq_user}")

            # Настройка соединения
            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
            connection_params = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                credentials=credentials
            )

            # Устанавливаем соединение с RabbitMQ
            self.connection = pika.BlockingConnection(connection_params)
            self.channel = self.connection.channel()

            # Объявление очередей
            self.channel.queue_declare(queue=SettingsTMP.RABBITMQ_QUEUE_post)
            self.channel.queue_declare(queue=SettingsTMP.RABBITMQ_QUEUE_get)
            print("RabbitMQ connection established successfully.")

        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            raise

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key=SettingsTMP.RABBITMQ_QUEUE_post, body=message)
        print(f" [x] Sent message: {message}")

    # Функция для получения сообщений из очереди
    def receive_messages(self):
        # Подпишемся на очередь
        # auto_ack=True -- no matter if lost
        self.channel.basic_consume(queue=SettingsTMP.RABBITMQ_QUEUE_get, on_message_callback=self.callback,
                                   auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    # Callback для обработки сообщения
    def start_consuming(self):
        print("start consuming")
        self.consumerThread = threading.Thread(target=self.receive_messages)
        self.consumerThread.start()


    def callback(self, ch, method, properties, body):
        print(f" [x] Received message: {body.decode()}")
        tmp = body.decode()

        # Преобразуем строку JSON в словарь
        try:
            tmp_dict = json.loads(tmp)

            # Рекурсивно заменяем все null значения на пустые строки


            tmp_dict = self.PAL.process(tmp_dict)

            # Преобразуем обратно в строку JSON
            tmp = json.dumps(tmp_dict)

        except json.JSONDecodeError:
            print("Error decoding JSON message")
        tmp = self.factory.execute_command(tmp)

        if tmp:
            print("EXAMPLE")
            print(str(tmp))
            self.send_message(str(tmp))

    def __del__(self):
        try:
            self.connection.close()
        except:
            print("connection = none")
