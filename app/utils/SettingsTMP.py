# Параметры подключения к RabbitMQ
import os

#RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")  # Адрес RabbitMQ (например, 127.0.0.1 или имя хоста)
#RABBITMQ_HOST = "172.21.16.1"
#RABBITMQ_HOST = "rabbitmq"
RABBITMQ_HOST = "192.168.213.28"
RABBITMQ_QUEUE_get = 'TODB'  # Имя очереди
RABBITMQ_QUEUE_post = 'TOHERE'  # Имя очереди

#прочитать про .env
