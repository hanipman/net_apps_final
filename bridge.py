#!/usr/bin/env/python

import pika
import sys
from pymongo import MongoClient
from rmq_params import rmq_params;
import json

cred = pika.PlainCredentials(rmq_params['username'], rmq_params['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_params['bridgeip'], virtual_host=rmq_params['vhost'], credentials=cred))
channel = connection.channel();
print("Connected to vhost'" + rmq_params["vhost"] + "' on RMQ server at 'localhost' as user'" + rmq_params["username"] + "'")

# create exchanges
count = 0;
list_exchanges=list(rmq_params["exchanges"])
while count < len(list_exchanges):
    channel.exchange_declare(exchange=list_exchanges[count], exchange_type='direct')
    print("Created " + list_exchanges[count] + " exchange")
    count = count + 1

# create queue for app to server
result = channel.queue_declare(queue="server")
queue_name = result.method.queue
channel.queue_purge(queue_name)
channel.queue_unbind(queue=queue_name, exchange="apptoserver", routing_key=queue_name)
channel.queue_bind(exchange="apptoserver", queue=queue_name, routing_key=queue_name)
print("Created " + queue_name + " queue for apptoserver")

# create queue for server to database
result = channel.queue_declare(queue="store")
queue_name = result.method.queue
channel.queue_purge(queue_name)
channel.queue_unbind(queue=queue_name, exchange="servertodatabase", routing_key=queue_name)
channel.queue_bind(exchange="servertodatabase", queue=queue_name, routing_key=queue_name)
print("Created " + queue_name + " queue for servertodatabase")

# initialize database and collection
client = MongoClient()
db = client.gameStorage
print("Created database 'gameStorage'")
accounts = db.accounts
print("Created collection 'accounts'")
instances = db.instances
print("Created collection 'instances'")

# parse message based on identifier and message
def callback(ch, method, properties, body):
    print(json.loads(body.decode()))

channel.basic_consume(callback, queue="store", no_ack=True)

channel.start_consuming()
