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

channel.basic_consume(callback, queue="server", no_ack=True)

channel.start_consuming()
