import logging
import os
import pika
from mqrabbit.config import *
from mqrabbit.callbacks import *


def on_channel_open(channel):
    channel.basic_consume(CHANNEL_CANCEL_RESERVATION_QUEUE,
                          cancel_reservation,
                          auto_ack=AUTO_ACK)
    channel.basic_consume(CHANNEL_NEW_SHOWING_QUEUE,
                          new_showing,
                          auto_ack=AUTO_ACK)
    channel.basic_consume(CHANNEL_CONFIRM_RESERVATION_QUEUE,
                          confirm_reservation,
                          auto_ack=AUTO_ACK)
    channel.basic_consume(CHANNEL_TEST_QUEUE,
                          test,
                          auto_ack=AUTO_ACK)


def on_open(connection_):
    connection_.channel(on_open_callback=on_channel_open)


def start_mqrabbit(mq_connection):
    try:
        mq_connection.ioloop.start()
    except KeyboardInterrupt:
        mq_connection.close()
        mq_connection.ioloop.start()


logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', CLOUDAMQP_URL)
params = pika.URLParameters(url)
params.socket_timeout = SOCKET_TIMEOUT
connection = pika.SelectConnection(parameters=params,
                                   on_open_callback=on_open)
connection2 = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel_receiver = connection2.channel()
channel_receiver.queue_declare(queue=CHANNEL_CANCEL_RESERVATION_NOTIFICATION_QUEUE, durable=True)
channel_receiver.queue_declare(queue=CHANNEL_REFUND_QUEUE, durable=True)
channel_receiver.queue_declare(queue=CHANNEL_TICKET_NOTIFICATION_QUEUE, durable=True)
channel_receiver.queue_declare(queue=CHANNEL_TEST_QUEUE, durable=True)
channel_receiver.queue_declare(queue=CHANNEL_CANCEL_RESERVATION_QUEUE, durable=True)
channel_receiver.queue_declare(queue=CHANNEL_NEW_SHOWING_QUEUE, durable=True)
channel_receiver.queue_declare(queue=CHANNEL_CONFIRM_RESERVATION_QUEUE, durable=True)
channel_receiver.queue_declare(queue=CHANNEL_TEST_QUEUE, durable=True)
#  how to publish message to MQRabbit customer
#  channel.basic_publish(exchange='', routing_key='cancel-reservation', body='User information')
