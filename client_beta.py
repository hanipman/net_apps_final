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
connection = None
channel = None
consumer_id = None
playerNum = ""

def getPlayerNum():
    global playerNum

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
            print(arg)
            if arg == 'player1' or arg == 'player2':
                playerNum = arg
            else:
                print("Argument must be: 'player1' or 'player2'")
                sys.exit(2)

def connectRMQ():
    global channel
    login = pika.PlainCredentials(rmq_params.rmq_params["username"], rmq_params.rmq_params["password"])
    connection = pika.BlockingConnection(pika.ConnectionParameters(rmq_params.rmq_params["bridgeip"], credentials=login, virtual_host=rmq_params.rmq_params["vhost"]))
    channel = connection.channel()
    channel.exchange_declare(exchange='apptoserver', exchange_type='direct')
    return None

def mainMenu():
    while True:
        i = input("Type 'play' to play")
        if i == 'play':
            break

def printBoard():
    global consumer_id
    consumer_id = channel.basic_consume(grabBoard,
                                        queue=playerNum,
                                        no_ack=True)
    channel.start_consuming()

def grabBoard(ch, method, properties, body):
    global gameBoard
    gameBoard = json.loads(body)
    print(gameBoard)
    channel.basic_cancel(consumer_tag=consumer_id)

def connectToServer():
    channel.basic_publish(exchange='apptoserver',
                          routing_key='server',
                          body=playerNum)

def main():
    #TODO
    #Get the player number, ie. 'player1' or 'player2'
    #Will remove after beta
    getPlayerNum()
    #Get RMQ server address
    #print and get login info
    #connect to rmq
    connectRMQ()
    #print command line (accepting only 'play') ~!concept of a main menu.
    mainMenu()
    #connect to game exchange
    connectToServer()
    #wait for other player to connect to game
    #print board
    printBoard()
    #deploy
    #print board
    #main loop:
        #take turn
        #wait for turn
if __name__ == "__main__":
    main()
