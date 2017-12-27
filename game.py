#!/usr/bin/env/python

import random
from rmq_params import rmq_params
import pika
import json
import time

cred = pika.PlainCredentials(rmq_params['username'], rmq_params['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_params['bridgeip'], virtual_host=rmq_params['vhost'], credentials=cred))
channel = connection.channel();
print("Connected to vhost'" + rmq_params["vhost"] + "' on RMQ server at 'localhost' as user'" + rmq_params["username"] + "'")

def callback(ch, method, properties, body):
    print(json.loads(body.decode()))
    prop = pika.BasicProperties(correlation_id = properties.correlation_id)
    channel.basic_publish(exchange="apptoserver", routing_key=properties.reply_to, properties=prop, body={"Recieved": "True"})
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue="server", no_ack=True)

channel.start_consuming()
