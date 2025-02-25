import pika
from threading import Thread
from django.core.cache import cache
import ast
from django.conf import settings
import json


def Rabbitmq_Consumer_AuthUser(exchange_name, queue_name):
    def callback(ch, method, properties, body):
        print(body)            
        body = Decode_And_Conversion_Dictionary(body=body)
        if body["id_user"]:
            Rabbitmq_Producer_AuthUser(body=Get_All_User_Order(user_id=body["id_user"]),
                                       exchange_name='User', queue_name="get_order_user",)
        cache.set(key="Data",value=body, timeout=5)
        cache.close()
        # ch.basic_ack(delivery_tag=method.delivery_tag)
    def start_consumer():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=queue_name)

        channel.basic_consume(queue=queue_name,
                            on_message_callback=callback,
                            auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    consumer_thread = Thread(target=start_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()

def Rabbitmq_Producer_AuthUser(exchange_name, queue_name, body=None, headers=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=queue_name)
    # properties = pika.BasicProperties(headers=headers) if headers else None
    channel.basic_publish(exchange=exchange_name,
                        routing_key=queue_name,
                        body=json.dumps(body),
                        properties=pika.BasicProperties(
                            delivery_mode=2,
                            headers={"JWT": headers}  if headers else None
                    ))
    
    connection.close()


def Get_All_User_Order(user_id):
    orders = list(settings.ORDER_COLLECTION.find({"user_id": user_id}))

    for order in orders:
        order['_id'] = str(order['_id'])
        order['user_id'] = str(order['user_id'])
    return orders


def Decode_And_Conversion_Dictionary(body):
        body = body.decode('utf-8')
        body = ast.literal_eval(body)
        return body