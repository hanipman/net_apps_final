#!/usr/bin/env/python
# pip3 install pika
# To change exchanges or queues, edit rmq_params

import pika
import sys
from pymongo import MongoClient
from rmq_params import rmq_params

cred = pika.PlainCredentials(rmq_params['username'], rmq_params['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_params['bridgeip'], virtual_host=rmq_params['vhost'], credentials=cred))
channel = connection.channel();
print("Connected to vhost'" + rmq_params["vhost"] + "' on RMQ server at 'localhost' as user'" + rmq_params["username"] + "'")

# create exchanges
count=0;
list_exchanges=list(rmq_params["exchanges"])
while count < len(list_exchanges):
    channel.exchange_declare(exchange=list_exchanges[count], exchange_type='direct')
    print("Created " + list_exchanges[count] + " exchange")
    count = count + 1

# create queues for app to server
count=0;
list_queuesGame=list(rmq_params["queuesGame"])
while count < len(list_queuesGame):
    result = channel.queue_declare(queue=list_queuesGame[count])
    queue_name = result.method.queue
    channel.queue_purge(queue_name)
    channel.queue_unbind(queue=queue_name, exchange="apptoserver", routing_key=queue_name)
    channel.queue_bind(exchange="apptoserver", queue=queue_name, routing_key=queue_name)
    print("Created " + list_queuesGame[count] + " queue for apptoserver")
    count = count + 1

# create queues for server to database
count=0;
list_queuesStorage=list(rmq_params["queuesStorage"])
while count < len(list_queuesStorage):
    result = channel.queue_declare(queue=list_queuesStorage[count])
    queue_name = result.method.queue
    channel.queue_purge(queue_name)
    channel.queue_unbind(queue=queue_name, exchange="servertostorage", routing_key=queue_name)
    channel.queue_bind(exchange="servertostorage", queue=queue_name, routing_key=queue_name)
    print("Created " + list_queuesStorage[count] + " queue for servertostorage")
    count = count + 1

# initialize database and collection
client = MongoClient()
db = client.gameStorage
print("Created database 'gameStorage'")
accounts = db.accounts
print("Created collection 'accounts'")
moveHist = db.moveHistory
print("Created collection 'moveHistory'")

#TODO Implement MongoDB stores
def callback(ch, method, properties, body):
    print(str(body))

channel.basic_consume(callback, queue="store", no_ack=True)

channel.start_consuming()
