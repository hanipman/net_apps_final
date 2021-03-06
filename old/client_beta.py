#This file serves as a command line based client
#As we approach the final iteration, we'll be implementing this
#in the Android environment

import pika
import json
import getopt
import sys
import rmq_params
from collections import OrderedDict

player1_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
player2_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
gameBoard = None
connection = None
channel = None
consumer_id = None
playerNum = ""
vision = set()
playerTurn = False

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
    gameBoard = json.loads(body.decode())
    printBoardCMD()
    channel.basic_cancel(consumer_tag=consumer_id)

def connectToServer():
    channel.basic_publish(exchange='apptoserver',
                          routing_key='server',
                          body=playerNum)
    
    
    
###########################################CMDLINE PRINT BOARD#########################################################
def printBoardCMD():
    #player 1
    if(playerNum == 'player1'):
        #CommandLine print
        row =[]
        letters = 'ABCDEFGH'
        numbers = '12345678'
        print('  '+numbers)
        wloc = player1_units['warrior']
        rloc = player1_units['ranger']
        sloc = player1_units['sorceress']
        otherWloc = player2_units['warrior']
        otherRloc = player2_units['ranger']
        otherSloc = player2_units['sorceress']
        for let in letters:
            for num in numbers:
                if(let+num in vision):
                    if(let+num == otherWloc):
                        if(gameBoard[let+num] == 'mountain'):
                            row.append('W')
                            continue
                        else:
                            row.append('w')
                            continue
                    elif(let+num == otherRloc):
                        if(gameBoard[let+num] == 'forest'):
                            row.append('R')
                            continue
                        else:
                            row.append('r')
                            continue
                    elif(let+num == otherSloc):
                        if(gameBoard[let+num] == 'lake'):
                            row.append('S')
                            continue
                        else:
                            row.append('s')
                            continue
                if(gameBoard[let+num] == 'plains'):
                    if(let+num == wloc):
                        row.append('w')
                    elif(let+num == rloc):
                        row.append('r')
                    elif(let+num == sloc):
                        row.append('s')
                    else:
                        row.append('p')
                elif(gameBoard[let+num] == 'mountain'):
                    if(let+num == wloc):
                        row.append('W')
                    else:
                        row.append('m')
                elif(gameBoard[let+num] == 'forest'):
                    if(let+num == wloc):
                        row.append('w')
                    elif(let+num == rloc):
                        row.append('R')
                    elif(let+num == sloc):
                        row.append('s')
                    else:
                        row.append('f')
                elif(gameBoard[let+num] == 'lake'):
                    if(let+num == sloc):
                        row.append('S')
                    else:
                        row.append('l')

            print(let+' '+row[0]+row[1]+row[2]+row[3]+row[4]+row[5]+row[6]+row[7])
            row.clear()
    #player 2
    else:
        #CommandLine print
        row =[]
        letters = 'ABCDEFGH'
        numbers = '12345678'
        print('  '+numbers)
        wloc = player2_units['warrior']
        rloc = player2_units['ranger']
        sloc = player2_units['sorceress']
        otherWloc = player1_units['warrior']
        otherRloc = player1_units['ranger']
        otherSloc = player1_units['sorceress']
        for let in letters:
            for num in numbers:
                if(let+num in vision):# and (let+num == otherWloc or let+num == otherRloc or let+num == otherSloc)):
                    if(let+num == otherWloc):
                        if(gameBoard[let+num] == 'mountain'):
                            row.append('W')
                        else:
                            row.append('w')
                    elif(let+num == otherRloc):
                        if(gameBoard[let+num] == 'forest'):
                            row.append('R')
                        else:
                            row.append('r')
                    elif(let+num == otherSloc):
                        if(gameBoard[let+num] == 'lake'):
                            row.append('S')
                        else:
                            row.append('s')
                if(gameBoard[let+num] == 'plains'):
                    if(let+num == wloc):
                        row.append('w')
                    elif(let+num == rloc):
                        row.append('r')
                    elif(let+num == sloc):
                        row.append('s')
                    else:
                        row.append('p')
                elif(gameBoard[let+num] == 'mountain'):
                    if(let+num == wloc):
                        row.append('W')
                    else:
                        row.append('m')
                elif(gameBoard[let+num] == 'forest'):
                    if(let+num == wloc):
                        row.append('w')
                    elif(let+num == rloc):
                        row.append('R')
                    elif(let+num == sloc):
                        row.append('s')
                    else:
                        row.append('f')
                elif(gameBoard[let+num] == 'lake'):
                    if(let+num == sloc):
                        row.append('S')
                    else:
                        row.append('l')

            print(let+' '+row[0]+row[1]+row[2]+row[3]+row[4]+row[5]+row[6]+row[7])
            row.clear()
###############################################END PRINTCMD#######################################################

###################################################VISION#############################################
def getVision():
    global consumer_id
    consumer_id = channel.basic_consume(assignVision,queue=playerNum,no_ack=True)
    channel.start_consuming()

def assignVision(ch, method, properties, body):
    global vision
    body = json.loads(body.decode())
    vision = list(body.keys())
    print("vision = ", vision)
    printBoardCMD()
    channel.basic_cancel(consumer_tag=consumer_id)
##################################################END VISION#################################################

####################################################DEPLOYMENT#########################################
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
        p1Deploy = input("Player 1: Where for "+unit+'\n')
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
                    channel.basic_publish(exchange='apptoserver',
                                          routing_key='server',
                                          body=json.dumps(deployInfo),
                                          properties=pika.BasicProperties(delivery_mode = 2))

def deployP2UnitFromCommandLine(unit):
    global player2_units
    while(player2_units[unit] == 'DEPLOY'):
        p2Deploy = input("Player 2: Where for "+unit+'\n')
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
    getOpponentUnitInfo()
    getVision()
    
def getOpponentUnitInfo():
    global consumer_id
    consumer_id = channel.basic_consume(assignOppUnits, queue=playerNum, no_ack=True)
    channel.start_consuming()
    
def assignOppUnits(ch, method, properties, body):
    print("collecting opposing unit info from server")
    global player1_units
    global player2_units
    body = json.loads(body.decode())
    print(body)
    if(playerNum == 'player1'):
        player2_units['warrior'] = body['warrior']
        player2_units['ranger'] = body['ranger']
        player2_units['sorceress'] = body['sorceress']
    else:
        player1_units['warrior'] = body['warrior']
        player1_units['ranger'] = body['ranger']
        player1_units['sorceress'] = body['sorceress']
    channel.basic_cancel(consumer_tag=consumer_id)
    
def getCurrentUnitInfo():
    global consumer_id
    consumer_id = channel.basic_consume(assignOwnUnits, queue=playerNum, no_ack=True)
    channel.start_consuming()
    
def assignOwnUnits(ch, method, properties, body):
    print("collecting own unit info from server")
    global player1_units
    global player2_units
    body = json.loads(body.decode())
    print(body)
    if(playerNum == 'player1'):
        player1_units['warrior'] = body['warrior']
        player1_units['ranger'] = body['ranger']
        player1_units['sorceress'] = body['sorceress']
    else:
        player2_units['warrior'] = body['warrior']
        player2_units['ranger'] = body['ranger']
        player2_units['sorceress'] = body['sorceress']
    channel.basic_cancel(consumer_tag=consumer_id)
################################################END DEPLOYMENT####################################################

##############################################TURN TAKING MECHANICS#######################################
gameOver = False
def takeTurn():
    global oppIsMoving
    global moveCont
    global playerTurn
    while(gameOver == False):
        #consume if it's our turn
        getTurnNotification()
        if(playerTurn == True):
            #publish which unit will play this turn
            publishUnitToPlay()
            while moveCont == True:
                #see movementOptions
                consumeMovementOptions()
                #make move
                publishMove()
                #get current info
                getCurrentUnitInfo()
                getOpponentUnitInfo()
                #update vision
                getVision()
                #check end of movement
                isMovementDone()
            skipRestOfTurn = False
            if unitIsDead:
                skipRestOfTurn = True
            if skipRestOfTurn == False:
                #do combat phase
                if consumeCombatOptions():
                    #publish attack
                    publishCombatMove()
            #get current unit info
            getCurrentUnitInfo()
            #get Opponent unit info
            getOpponentUnitInfo()
            #update vision
            getVision()
            moveCont = True #prime for next turn
        else:
            while oppIsMoving == True:
                #consume vision Messages from server
                getCurrentUnitInfo()
                getOpponentUnitInfo()
                getVision()
                getOppIsMoving()
            getCurrentUnitInfo()
            getOpponentUnitInfo()
            getVision()
            oppIsMoving = True #prime for next turn
        print("looking to consume game over")
        consumeGameOverStatus()
        
def assignNotification(ch, method, properties, body):
    global playerTurn
    if(body.decode() == playerNum):
        playerTurn = True
        print("It's your turn")
    else:
        playerTurn = False
        print("Wait for other player...")
    channel.basic_cancel(consumer_tag=consumer_id)
    
def getTurnNotification():
    global consumer_id
    consumer_id = channel.basic_consume(assignNotification, queue=playerNum, no_ack=True)
    channel.start_consuming()
    
def publishUnitToPlay():
    unit = input("Which unit will you use this turn?(w,r,s)\n")
    channel.basic_publish(exchange='apptoserver',
                          routing_key='server',
                          body=unit)
    
def consumeMovementOptions():
    global consumer_id
    consumer_id = channel.basic_consume(assignMovementOptions, queue=playerNum, no_ack=True)
    print("consuming move options")
    channel.start_consuming()

def assignMovementOptions(ch, method, properties, body):
    body = json.loads(body.decode())
    moveOptions = list(body.keys())
    print("You may move: ", moveOptions)
    channel.basic_cancel(consumer_tag=consumer_id)
    
def publishMove():
    space = input("Which space will you move to?\n")
    channel.basic_publish(exchange='apptoserver',
                          routing_key='server',
                          body=space)
def publishCombatMove():
    space = input("Which space will you attack?\n")
    channel.basic_publish(exchange='apptoserver',
                          routing_key='server',
                          body=space)
    
def isMovementDone():
    global consumer_id
    consumer_id = channel.basic_consume(assignCondMovement, queue=playerNum, no_ack=True)
    channel.start_consuming()
    
moveCont = True
unitIsDead = False
def assignCondMovement(ch, method, properties, body):
    print("consume end movement", body)
    global moveCont
    global unitIsDead
    body = body.decode()
    if body == 'n':
        moveCont = True
        unitIsDead = False
    elif body == 'y':
        moveCont = False
        unitIsDead = False
    else:
        moveCont = False
        unitIsDead = True
    channel.basic_cancel(consumer_tag=consumer_id)
    
consumeFlag = None
def consumeCombatOptions():
    global consumer_id
    consumer_id = channel.basic_consume(assignCombatOptions, queue=playerNum, no_ack=True)
    print("consuming combat options")
    channel.start_consuming()
    return consumeFlag

def assignCombatOptions(ch, method, properties, body):
    global consumeFlag
    body = json.loads(body.decode())
    moveOptions = list(body.keys())
    while len(list(moveOptions)) != 0:
        if ' ' in moveOptions:
            del moveOptions[' ']
        else:
            print("You may attack: ", moveOptions)
            consumeFlag = True
            channel.basic_cancel(consumer_tag=consumer_id)
            return None
    consumeFlag = False
    channel.basic_publish(exchange='apptoserver',
                            routing_key ='server',
                            body=' ')
    channel.basic_cancel(consumer_tag=consumer_id)
        
oppIsMoving = True
def getOppIsMoving():
    global consumer_id
    consumer_id = channel.basic_consume(oppMoving, queue=playerNum, no_ack=True)
    channel.start_consuming()

def oppMoving(ch, method, properties, body):
    global oppIsMoving
    if body.decode() == 'y':
        oppIsMoving = True
    else:
        oppIsMoving = False
    channel.basic_cancel(consumer_tag=consumer_id)
    
def consumeGameOverStatus():
    global consumer_id
    consumer_id = channel.basic_consume(checkGameOver, queue=playerNum, no_ack=True)
    channel.start_consuming()
    
def checkGameOver(ch, method, properties, body):
    global gameOver
    body =  json.loads(body.decode())
    winner = list(body.keys())
    if 'cont' in winner:
        gameOver = False
    elif playerNum in winner:
        gameOver = True
        print("You Win!")
    elif 'cats' in winner:
        gameOver = True
        print("Cat's Game")
    else:
        gameOver = True
        print("You Lose!")
    channel.basic_cancel(consumer_tag=consumer_id)
        
#########################################################################################################

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
    takeTurn()
    #print board
    #main loop:
        #take turn
        #wait for turn
if __name__ == "__main__":
    main()
