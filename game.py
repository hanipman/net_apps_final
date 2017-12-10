#This module handles the game mechanics and communicates with the bridge Pi using RMQ

#imports
import random
import rmq_params
import pika
import json

#define globals
player1_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
player2_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
player1_vision = set()
player2_vision = set()
gameBoard = None
gameOver = False
channel = None

#Put the bridge's ip into the rmq_params file
def connectRMQ():
    global channel
    login = pika.PlainCredentials(rmq_params.rmq_params["username"], rmq_params.rmq_params["password"])
    connection = pika.BlockingConnection(pika.ConnectionParameters(rmq_params.rmq_params["bridgeip"], credentials=login, virtual_host=rmq_params.rmq_params["vhost"]))
    channel = connection.channel()
    return None

#returns a set of the spaces a unit could see from the range they can see, 
#the pos on the board, and is the unit a Ranger in a forest? True or False
def setVisionFromStatAndPos(visionRange, pos, isRangerInForest):
    vision = set()
    stopUp = False
    stopUpRight = False
    stopRight = False
    stopRightDown = False
    stopDown = False
    stopDownLeft = False
    stopLeft = False
    stopLeftUp = False
    if(pos in gameBoard):
        vision.add(pos)
        row = pos[0]
        col = pos[1]
        temp = visionRange+1
        for visionIt in range(1, temp):
            #diagonals can only be -1 visionRange
            if(visionIt == visionRange):
                stopUpRight = True
                stopRightDown = True
                stopDownLeft = True
                stopLeftUp = True
            #handle up
            if(stopUp == False):
                space = chr(ord(row)-visionIt)+col
                if(space in gameBoard):
                    vision.add(space)
                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                        stopUp = True
                        if(isRangerInForest and gameBoard[space] == 'forest'):
                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                            stopUp = False
            #handle upRight
            if(stopUpRight == False):
                space = chr(ord(row)-visionIt)+str(int(col)+visionIt)
                if(space in gameBoard):
                    vision.add(space)
                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                        stopUpRight = True
                        if(isRangerInForest and gameBoard[space] == 'forest'):
                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                            stopUpRight = False
                    if(stopUpRight == False):
                        #look up and right
                        stopUpRightUp = False
                        stopUpRightRight = False
                        for it in range(1, visionRange-visionIt):
                            #up
                            if(stopUpRightUp == False):
                                space = chr(ord(row)-visionIt-it)+str(int(col)+visionIt)
                                if(space in gameBoard):
                                    vision.add(space)
                                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                                        stopUpRightUp = True
                                        if(isRangerInForest and gameBoard[space] == 'forest'):
                                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                                            stopUpRightUp = False
                            #right
                            if(stopUpRightRight == False):
                                space = chr(ord(row)-visionIt)+str(int(col)+visionIt+it)
                                if(space in gameBoard):
                                    vision.add(space)
                                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                                        stopUpRightRight = True
                                        if(isRangerInForest and gameBoard[space] == 'forest'):
                                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                                            stopUpRightRight = False
            #handle Right
            if(stopRight == False):
                space = row+str(int(col)+visionIt)
                if(space in gameBoard):
                    vision.add(space)
                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                        stopRight = True
                        if(isRangerInForest and gameBoard[space] == 'forest'):
                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                            stopRight = False
            #handle rightDown
            if(stopRightDown == False):
                space = chr(ord(row)+visionIt)+str(int(col)+visionIt)
                if(space in gameBoard):
                    vision.add(space)
                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                        stopRightDown = True
                        if(isRangerInForest and gameBoard[space] == 'forest'):
                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                            stopRightDown = False
                    if(stopRightDown == False):
                        #look right and down
                        stopRightDownRight = False
                        stopRightDownDown = False
                        for it in range(1, visionRange-visionIt):
                            #right
                            if(stopRightDownRight == False):
                                space = chr(ord(row)+visionIt)+str(int(col)+visionIt+it)
                                if(space in gameBoard):
                                    vision.add(space)
                                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                                        stopRightDownRight = True
                                        if(isRangerInForest and gameBoard[space] == 'forest'):
                                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                                            stopRightDownRight = False
                            #down
                            if(stopRightDownDown == False):
                                space = chr(ord(row)+visionIt+it)+str(int(col)+visionIt)
                                if(space in gameBoard):
                                    vision.add(space)
                                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                                        stopRightDownDown = True
                                        if(isRangerInForest and gameBoard[space] == 'forest'):
                                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                                            stopRightDownDown = False
            #handle Down
            if(stopDown == False):
                space = chr(ord(row)+visionIt)+col
                if(space in gameBoard):
                    vision.add(space)
                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                        stopDown = True
                        if(isRangerInForest and gameBoard[space] == 'forest'):
                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                            stopDown = False
            #handle DownLeft
            if(stopDownLeft == False):
                space = chr(ord(row)+visionIt)+str(int(col)-visionIt)
                if(space in gameBoard):
                    vision.add(space)
                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                        stopDownLeft = True
                        if(isRangerInForest and gameBoard[space] == 'forest'):
                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                            stopDownLeft = False
                    if(stopDownLeft == False):
                        #look down and left
                        stopDownLeftDown = False
                        stopDownLeftLeft = False
                        for it in range(1, visionRange-visionIt):
                            #down
                            if(stopDownLeftDown == False):
                                space = chr(ord(row)+visionIt+it)+str(int(col)-visionIt)
                                if(space in gameBoard):
                                    vision.add(space)
                                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                                        stopDownLeftDown = True
                                        if(isRangerInForest and gameBoard[space] == 'forest'):
                                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                                            stopDownLeftDown = False
                            #left
                            if(stopDownLeftLeft == False):
                                space = chr(ord(row)+visionIt)+str(int(col)-visionIt-it)
                                if(space in gameBoard):
                                    vision.add(space)
                                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                                        stopDownLeftLeft = True
                                        if(isRangerInForest and gameBoard[space] == 'forest'):
                                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                                            stopDownLeftLeft = False
            #handle Left
            if(stopLeft == False):
                space = row+str(int(col)-visionIt)
                if(space in gameBoard):
                    vision.add(space)
                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                        stopLeft = True
                        if(isRangerInForest and gameBoard[space] == 'forest'):
                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                            stopLeft = False
            #handle LeftUp
            if(stopLeftUp == False):
                space = chr(ord(row)-visionIt)+str(int(col)-visionIt)
                if(space in gameBoard):
                    vision.add(space)
                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                        stopLeftUp = True
                        if(isRangerInForest and gameBoard[space] == 'forest'):
                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                            stopLeftUp = False
                    if(stopLeftUp == False):
                        #look left and up
                        stopLeftUpLeft = False
                        stopLeftUpUp = False
                        for it in range(1, visionRange-visionIt):
                            #left
                            if(stopLeftUpLeft == False):
                                space = chr(ord(row)-visionIt)+str(int(col)-visionIt-it)
                                if(space in gameBoard):
                                    vision.add(space)
                                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                                        stopLeftUpLeft = True
                                        if(isRangerInForest and gameBoard[space] == 'forest'):
                                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                                            stopLeftUpLeft = False
                            #up
                            if(stopLeftUpUp == False):
                                space = chr(ord(row)-visionIt-it)+str(int(col)-visionIt)
                                if(space in gameBoard):
                                    vision.add(space)
                                    if((gameBoard[space] != 'plains') and (gameBoard[space] != 'lake')):
                                        stopLeftUpUp = True
                                        if(isRangerInForest and gameBoard[space] == 'forest'):
                                            #rangers aren't inhibitted from seeing over treetops, when in another forest
                                            stopLeftUpUp = False
    return vision


#returns a set containing a player's vision, given their units' positions
def setPlayerVision(players_units):
    vision = set()
    wloc = players_units['warrior']
    rloc = players_units['ranger']
    sloc = players_units['sorceress']
    units_loc = [wloc, rloc, sloc]
    for each in units_loc:
        if(each != 'DEAD' and each != 'DEPLOY'):
            #warriors vision
            if(each == wloc):
                if(gameBoard[each] == 'forest'):
                    #1 less vision
                    vision = vision | setVisionFromStatAndPos(2, wloc, False)
                else:
                    #add vision to warrior space normally
                    vision = vision | setVisionFromStatAndPos(3, wloc, False)

            #ranger's vision
            elif(each == rloc):
                if(gameBoard[each] == 'forest'):
                    #5 space vision
                    vision = vision | setVisionFromStatAndPos(5, rloc, True)
                else:
                    #4 space vision
                    vision = vision | setVisionFromStatAndPos(4, rloc, False)
            #sorceress vision
            elif(each == sloc):
                if(gameBoard[each] == 'forest'):
                    #1 less
                    vision = vision | setVisionFromStatAndPos(2, sloc, False)
                else:
                    #3 vision
                    vision = vision | setVisionFromStatAndPos(3, sloc, False)
    return vision


def takeTurns():
    #TODO wait to receive message, which will be from P1
    #if(play1_player1.keys() == 'warrior'):
        #if(warriorMoveValid()):
           # executeWarriorMove(play1_player1)
           return None

#Turner's Code
def showAvailableMovement(unit, currentLoc) :
    #transmit over RMQ the  immediately adjacent and current positions
    msg = "a: ";
    row = currentLoc[0]
    col = currentLoc[1]
    #this spot
    msg += "[" + currentLoc + "]";
    #up
    space = chr(ord(row)-1)+col
    if(checkValidMove(unit, space)):
        msg += ", [" + space + "]"
    #right
    space = row+str(int(col)+1)
    if(checkValidMove(unit, space)):
        msg += ", [" + space + "]"
    #down
    space = chr(ord(row)+1)+col
    if(checkValidMove(unit, space)):
        msg += ", [" + space + "]"
    #left
    space = row+str(int(col)-1)
    if(checkValidMove(unit, space)):
        msg += ", [" + space + "]"
    return msg

def processMoves(player, unit, currentLoc):
    #show the available movements for the unit
    availableMoves = showAvailableMovement(unit, currentLoc);
    #wait for a selection from the app
    #move the unit in the server
    moveUnit(player, unit, targetLoc);
    #report new unit positions
    #report new unit vision
    return None

def checkValidMove(unit, loc) :
    if(loc in gameBoard) :
        if(gameBoard[loc] == 'mountain') :
            if(unit == 'warrior'):
                return True;
            else:
                return False;
        elif (gameBoard[loc] == 'lake') :
            if(unit == 'sorceress'):
                return True;
        else:
            return True;

def moveUnit(player, unit, newLoc) :
    if(player == 'player1'):
        player1_units[unit] = newLoc;
    else:
        player2_units[unit] = newLoc;

def checkVisionBonus(unit, loc):
    if(gameBoard[loc] == 'plains'):
        return False
    elif(gameBoard[loc] == 'forest' and unit == 'ranger'):
        return True
    else:
        return False
#######################################

#Sets player vision from deployment details
def afterDeployInit():
    global player1_vision
    global player2_vision
    player1_vision = setPlayerVision(player1_units)
    player2_vision = setPlayerVision(player2_units)
    #TODO vision message on RMQ
    print("Player1's Vision = " + str(player1_vision))
    print("Player2's Vision = " + str(player2_vision))

#Produces proper RMQ board
#For now it does a commandLine print of the board in this format:
#   12345678
#
#A  RWlmlffm
#B  llsfplfl
#C  lffmfpmp
#D  pmpflplm
#E  lfflpflm
#F  mfpfmfpf
#G  wfSlmpfp
#H  fmmplRpm
#
#Where m=mountain;l=lake;f=forest;p=plains;s=sorceress;r=ranger;w=warrior
#A unit capitalized means that it is in its respective bonus-granting geo-location
#e.g. W in m, w in p or f
def printBoardP2():
    #TODO P2 units status message on RMQ
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
            if(let+num in player2_vision):# and (let+num == otherWloc or let+num == otherRloc or let+num == otherSloc)):
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

def printBoardP1():
    #TODO P1 units status on RMQ
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
            skipSpace = False
            if(let+num in player1_vision):
                if(let+num == otherWloc):
                    skipSpace = True
                    if(gameBoard[let+num] == 'mountain'):
                        row.append('W')
                    else:
                        row.append('w')
                elif(let+num == otherRloc):
                    skipSpace = True
                    if(gameBoard[let+num] == 'forest'):
                        row.append('R')
                    else:
                        row.append('r')
                elif(let+num == otherSloc):
                    skipSpace = True
                    if(gameBoard[let+num] == 'lake'):
                        row.append('S')
                    else:
                        row.append('s')
            if(skipSpace == False):
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

def randomGeo():
    geo = ['plains', 'plains','forest', 'mountain', 'lake']#(L454):for now just increase amount of plains in list until stable
    return random.choice(geo)

#Assigns the gameBoard dictionary {spaceLocation:randomGeo}
def createBoard():
    #TODO if we have time, make an algorithm that prevents problems with the board. Like mountains all across the middle
    global gameBoard
    board = {}
    letters = 'ABCDEFGH'
    numbers = '12345678'
    for x in letters:
        for y in numbers:
            board[x+y] = randomGeo()
    gameBoard = board

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

##############################TEMPORARY FUNCTIONS BEING USED FOR BETA#####################################
def deployP1UnitFromCommandLine(unit):
    global player1_units
    while(player1_units[unit] == 'DEPLOY'):
        p1Deploy = input("Player 1: Where for "+unit)
        if(checkInDeploymentZone('player1', p1Deploy) == False):
            print("Pick a space in the first 2 rows")
        else:
            if(checkValidMove(unit, p1Deploy) == False):
                print("Unit cannot enter "+p1Deploy)
            else:
                if(isEmptySpace(p1Deploy) == False):
                    print("Space is not empty "+p1Deploy)
                else:
                    player1_units[unit] = p1Deploy

def deployP2UnitFromCommandLine(unit):
    global player2_units
    while(player2_units[unit] == 'DEPLOY'):
        p2Deploy = input("Player 2: Where for "+unit)
        if(checkInDeploymentZone('player2', p2Deploy) == False):
            print("Pick a space in the first 2 rows")
        else:
            if(checkValidMove(unit, p2Deploy) == False):
                print("Unit cannot enter "+p2Deploy)
            else:
                if(isEmptySpace(p2Deploy) == False):
                    print("Space is not empty "+p2Deploy)
                else:
                    player2_units[unit] = p2Deploy

def deployPlayerCommandLine(player):
    units = ['warrior', 'ranger', 'sorceress']
    if(player == 'player1'):
        for unit in units:
            deployP1UnitFromCommandLine(unit)
    else:
        #player2
        for unit in units:
            deployP2UnitFromCommandLine(unit)
            
############################################################################################

####   RabbitMQ Stuff ####

bothConnected = False
player1Connected = False
player2Connected = False
consumer_id = " "

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    channel.basic_publish(exchange='servertostorage',
                          routing_key='store',
                          body=body)
    channel.basic_publish(exchange='apptoserver',
                          routing_key='player1',
                          body='response')
    channel.basic_publish(exchange='apptoserver',
                          routing_key='player1',
                          body='response')
    channel.basic_publish(exchange='apptoserver',
                          routing_key='player2',
                          body='response')

def on_message(ch, method, properties, body):
    body = str(body)
    body = body[2:-1]
    if body == "player1":
        print("Player 1 Connected")
        global player1Connected
        player1Connected = True
    elif body == "player2":
        print("Player 2 Connected")
        global player2Connected
        player2Connected = True
    if player1Connected == True and player2Connected == True:
        global bothConnected
        bothConnected = True
        channel.basic_cancel(consumer_tag=consumer_id)

def checkIfPlayersConnected():
    while bothConnected == False:
        print('Waiting for players to connect...')
        global consumer_id
        consumer_id = channel.basic_consume(on_message, queue='server', no_ack=True)
        channel.start_consuming()


#def game_message(ch, method, properties, body):
    #body = str(body)
    #temp = body[0:1]
    ##movement
    #if temp == "m":
        
    ##vision
    #elif temp == "v":
        
    ##combat
    #elif temp == "c":

#def handleGame():
    #while gameOver == False:
        #global consumer_id
        #consumer_id = channel.basic_consume(game_message, queue='server', no_ack=True)
        #channel.start_consuming()
        
def deploy_message(ch, method, properties, body):
    body = json.loads(str(body))
    if('1w' in body):
        space = body['1w']
        player1_units['warrior'] = space
    elif('1r' in body):
        space = body['1r']
        player1_units['ranger'] = space
    elif('1s' in body):
        space = body['1s']
        player1_units['sorceress'] = space
    elif('2w' in body):
        space = body['2w']
        player2_units['warrior'] = space
    elif('2r' in body):
        space = body['2r']
        player2_units['ranger'] = space
    elif('2s' in body):
        space = body['2s']
        player2_units['sorceress'] = space
    if(player1_units['warrior'] != 'DEPLOY' and player1_units['ranger'] != 'DEPLOY' and player1_units['sorceress'] != 'DEPLOY' and player2_units['warrior'] != 'DEPLOY' and player2_units['ranger'] != 'DEPLOY' and player2_units['sorceress'] != 'DEPLOY'):
        channel.basic_cancel(consumer_tag=consumer_id)
        
def handleDeployment():
    while (player1_units['warrior'] == 'DEPLOY' or player1_units['ranger'] == 'DEPLOY' or player1_units['sorceress'] == 'DEPLOY' or player2_units['warrior'] == 'DEPLOY' or player2_units['ranger'] == 'DEPLOY' or player2_units['sorceress'] == 'DEPLOY'):
        global consumer_id
        consumer_id = channel.basic_consume(deploy_message, queue='server', no_ack=True)
        channel.start_consuming()
        
###########################

def main():
    connectRMQ()
    checkIfPlayersConnected();
    createBoard()
    #push gameBoard through message queue
    channel.basic_publish(exchange='apptoserver',
                          routing_key='player1',
                          body=json.dumps(gameBoard),
                          properties=pika.BasicProperties(delivery_mode = 2))
    channel.basic_publish(exchange='apptoserver',
                          routing_key='player2',
                          body=json.dumps(gameBoard),
                          properties=pika.BasicProperties(delivery_mode = 2))
    handleDeployment()
    #deployPlayerCommandLine('player1')#TODO deploy through RMQ
    #deployPlayerCommandLine('player2')
    afterDeployInit()
    #while(~gameOver):
        #takeTurns()
    #TODO ShowEndResults()

if __name__ == "__main__":
    main()
