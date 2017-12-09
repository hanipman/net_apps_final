#This file serves as a command line based client
#As we approach the final iteration, we'll be implementing this
#in the Android environment

import pika
import json
import getopt
import sys
import rmq_params

player1_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
player2_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
gameBoard = None
channel = None
playerNum = ""

def connectRMQ():
    global channel
    login = pika.PlainCredentials(rmq_params.rmq_params["username"], rmq_params.rmq_params["password"])
    connection = pika.BlockingConnection(pika.ConnectionParameters(rmq_params.rmq_params["bridgeip"], credentials=login, virtual_host=rmq_params.rmq_params["vhost"]))
    channel = connection.channel()
    channel.exchange_declare(exchange='apptoserver', exchange_type='direct')
    return None

def getPlayerNum():
    global playerNum
    global channel

    #Get RMQ_server_address
    try:
        opts, args = getopt.getopt(sys.argv[1:],"u:")
    except getopt.GetoptError:
        print("client_beta.py -u '<player#>''")
        sys.exit(2)
    if(len(opts) < 1):
        print("Usage:")
        print("client_beta.py -u '<player#>''")
    for opt, arg in opts:
        if opt == "-u":
            global channel
            playerNum = arg
            print(playerNum)

def grabBoard(ch, method, properties, body):
    global gameBoard
    gameBoard = json.loads(body)
    print(gameBoard)

def main():
    #TODO
    getPlayerNum()
    #Get RMQ server address
    #print and get login info
    #connect to rmq
    connectRMQ()
    #print command line (accepting only 'play') ~!concept of a main menu.
    #connect to game exchange
    channel.basic_publish(exchange='apptoserver',
                          routing_key='server',
                          body=playerNum)
    channel.basic_consume(grabBoard,
                          queue=playerNum,
                          no_ack=True)
    channel.start_consuming()
    #wait for other player to connect to game
    #print board
    #deploy
    #print board
    #main loop:
        #take turn
        #wait for turn
if __name__ == "__main__":
    main()
