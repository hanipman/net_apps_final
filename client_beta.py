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
        i = input("Type 'play' to play\n")
        if i == 'play':
            break

def grabBoard():
    global consumer_id
    consumer_id = channel.basic_consume(printBoard,
                                        queue=playerNum,
                                        no_ack=True)
    channel.start_consuming()

def printBoard(ch, method, properties, body):
    global gameBoard
    gameBoard = json.loads(body)
    print(gameBoard)
    channel.basic_cancel(consumer_tag=consumer_id)

def connectToServer():
    channel.basic_publish(exchange='apptoserver',
                          routing_key='server',
                          body=playerNum)

##################################DEPLOYMENT##########################################
def checkInDeploymentZone(player, pos):
    deploymentZone = []
    if(player == 'player1'):
        for let in 'AB':
            for num in '12345678':
                deploymentZone.append(let+num)
        if(pos in deploymentZone):
            return True
        else:
            return False
    else:
        #player2
        for let in 'GH':
            for num in '12345678':
                deploymentZone.append(let+num)
        if(pos in deploymentZone):
            return True
        else:
            return False

#checks if space has no units in it
def isEmptySpace(pos):
    p1wloc = player1_units['warrior']
    p1rloc = player1_units['ranger']
    p1sloc = player1_units['sorceress']
    p2wloc = player2_units['warrior']
    p2rloc = player2_units['ranger']
    p2sloc = player2_units['sorceress']
    if(pos != p1wloc and pos != p1rloc and pos != p1sloc and pos != p2wloc and pos != p2rloc and pos != p2sloc):
        return True
    else:
        return False

#checks if unit can go into space
def unitCanEnterSpace(unit, pos):
    if(unit == 'warrior'):
        if(gameBoard[pos] == 'plains' or gameBoard[pos] == 'mountain' or gameBoard[pos] == 'forest'):
            return True
        else:
            return False
    elif(unit == 'ranger'):
        if(gameBoard[pos] == 'plains' or gameBoard[pos] == 'forest'):
            return True
        else:
            return False
    else:
        if(gameBoard[pos] == 'plains' or gameBoard[pos] == 'forest' or gameBoard[pos] == 'lake'):
            return True
        else:
            return False

def deployP1UnitFromCommandLine(unit):
    global player1_units
    while(player1_units[unit] == 'DEPLOY'):
        p1Deploy = input("Player 1: Where for "+unit)
        if(checkInDeploymentZone('player1', p1Deploy) == False):
            print("Pick a space in the first 2 rows")
        else:
            if(unitCanEnterSpace(unit, p1Deploy) == False):
                print("Unit cannot enter "+p1Deploy)
            else:
                if(isEmptySpace(p1Deploy) == False):
                    print("Space is not empty "+p1Deploy)
                else:
                    player1_units[unit] = p1Deploy
                    deployInfo = {}
                    deployInfo['1'+unit[0]] = p1Deploy
                    print(deployInfo)
                    channel.basic_publish(exchange='apptoserver',
                                          routing_key='server',
                                          body=json.dumps(deployInfo),
                                          properties=pika.BasicProperties(delivery_mode = 2))

def deployP2UnitFromCommandLine(unit):
    global player2_units
    while(player2_units[unit] == 'DEPLOY'):
        p2Deploy = input("Player 2: Where for "+unit)
        if(checkInDeploymentZone('player2', p2Deploy) == False):
            print("Pick a space in the first 2 rows")
        else:
            if(unitCanEnterSpace(unit, p2Deploy) == False):
                print("Unit cannot enter "+p2Deploy)
            else:
                if(isEmptySpace(p2Deploy) == False):
                    print("Space is not empty "+p2Deploy)
                else:
                    player2_units[unit] = p2Deploy
                    deployInfo = {}
                    deployInfo['2'+unit[0]] = p2Deploy
                    print(deployInfo)
                    channel.basic_publish(exchange='apptoserver',
                                          routing_key='server',
                                          body=json.dumps(deployInfo),
                                          properties=pika.BasicProperties(delivery_mode = 2))

def deployPlayerCommandLine(player):
    units = ['warrior', 'ranger', 'sorceress']
    if(player == 'player1'):
        for unit in units:
            deployP1UnitFromCommandLine(unit)
    else:
        #player2
        for unit in units:
            deployP2UnitFromCommandLine(unit)
def deploy():
    deployPlayerCommandLine(playerNum)
    
##############################################################################

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
    grabBoard()
    #deploy
    deploy()
    #print board
    #main loop:
        #take turn
        #wait for turn
if __name__ == "__main__":
    main()
