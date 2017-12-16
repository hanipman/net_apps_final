#This module handles the game mechanics and communicates with the bridge Pi using RMQ
#MUST REPORT consumed moves, MUST REPORT response to be produced

#imports
import random
import rmq_params
import pika
import json
import time

#define globals
player1_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
player2_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
player1_vision = set()
player2_vision = set()
gameBoard = None
gameOver = False
channel = None
player1Wins = False
player2Wins = False

def updateGameOver():
    global gameOver
    global player1Wins
    global player2Wins
    dict = {}
    #check if player 2 won
    if player1_units['warrior'] == 'DEAD' and player1_units['ranger'] == 'DEAD' and player1_units['sorceress'] == 'DEAD':
        gameOver = True
        player2Wins = True
    #check if player 1 won
    if player2_units['warrior'] == 'DEAD' and player2_units['ranger'] == 'DEAD' and player2_units['sorceress'] == 'DEAD':
        gameOver = True
        if player2Wins:
            dict['cats'] = gameOver
        else:
            dict['player1'] = gameOver        
    elif player2Wins:
        dict['player2'] = gameOver
    else:
        dict['cont'] = gameOver
    time.sleep(1)
    channel.basic_publish(exchange='apptoserver',
                              routing_key='player1',
                              body=json.dumps(dict))
    channel.basic_publish(exchange='apptoserver',
                              routing_key='player2',
                              body=json.dumps(dict))
    print("Game Over status published to both players")

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


#Turner's Code
def blockForResponse(player) :
    method_frame, header_frame, body = channel.basic_get(player)
    if method_frame:
        return body
        #print method_frame, header_frame, body
        #channel.basic_ack(method_frame.delivery_tag)
    else:
        blockForResponse(player)

def getTargetLoc(received):
    #extract target location from the message
    #*******NEEDS COMPLETION AFTER FORMAT DECIDED*****
    return None

def showAvailableMovement(unit, currentLoc) :
    #transmit over RMQ the  immediately adjacent and current positions
    available = set()
    row = currentLoc[0]
    col = currentLoc[1]
    #this spot
    available.add(currentLoc)
    #up
    space = chr(ord(row)-1)+col
    if(checkValidMove(unit, space)):
        available.add(space)
    #right
    space = row+str(int(col)+1)
    if(checkValidMove(unit, space)):
        available.add(space)
    #down
    space = chr(ord(row)+1)+col
    if(checkValidMove(unit, space)):
        available.add(space)
    #left
    space = row+str(int(col)-1)
    if(checkValidMove(unit, space)):
        available.add(space)
    return msg

def processMoves(player, unit):
    currentLoc = None
    if(player == 'player1') :
        currentLoc = player1_units[unit]
    else :
        currentLoc = player2_units[unit]
    #show the available movements for the unit
    availableMoves = showAvailableMovement(unit, currentLoc)
    #wait for a selection from the app
    received = blockForResponse()
    #extract choice from the received message
    targetLoc = getTargetLoc(received)
    #move the unit in the server
    moveUnit(player, unit, targetLoc)
    #report new unit positions
    sendUnitPositions(player)
    #report new unit vision
    #*******
    return None

def getDistance(pointA, pointB): 
    AY = ord(pointA[0])
    AX = int(pointA[1])
    BY = ord(pointB[0])
    BX = int(pointB[1])
    diffY = abs(AY - BY)
    diffX = abs(AX - BX)
    totalDiff = diffY + diffX
    return int(totalDiff)


def showAvailableTargets(player, unit, currentLoc) :
    myVisibility = None
    enemyUnits = None
    attackRange = 0
    if(player == 'player1') :
        myVisibility = player1_vision
        enemyUnits = player2_units
    else :
        myVisibility = player2_vision
        enemyUnits = player1_units
    myVisibility = None;
    enemyUnits = None;
    attackRange = 0;
    ewloc = None;
    erloc = None;
    esloc = None;
    if(player == 'player1') :
        ewloc = player2_units['warrior']
        erloc = player2_units['ranger']
        esloc = player2_units['sorceress']
        myVisibility = player1_vision;
        enemyUnits = player2_units;
    else :
        ewloc = player1_units['warrior']
        erloc = player1_units['ranger']
        esloc = player1_units['sorceress']
        myVisibility = player2_vision;
        enemyUnits = player1_units;
    if(unit == 'warrior') :
        attackRange = 0    #must be on the unit it wants to kill
    elif(unit == 'ranger') :
        attackRange = 3
    else:
        attackRange = 2
    #check if there are units in range and vision
    targets = set()
    for position in enemyUnits :
        if(position in myVisibility) :
            targets.add(position)
    return targets

def processCombat(player, unit) :
    currentLoc = None
        #Check if we're allowed to kill that
    if(unit == 'warrior'):
        if(position == ewloc or position == erloc):
            targets.add(position);
    elif(unit == 'ranger'):
        if(position == esloc or position == erloc):
            targets.add(position);
    else:
        if(position == ewloc or position == esloc):
            targets.add(position);
    return targets

def processCombat(player, unit) :
    global player2_units;
    global player1_units;
    #TODO*****
    #   make it so Warriors try to attack when they move on someone
    currentLoc = None;
    if(player == 'player1') :
        currentLoc = player1_units[unit]
    else :
        currentLoc = player2_units[unit]
    #show targetable units
    availableTargets = showAvailableTargets(player, unit, currentLoc)
    #send targets
    sendTargets(availableTargets)
    #wait for selection from app
    target = blockForResponse()
    #kill them dead in the face
    if(player == 'player1'):
        player2_units[target] = 'DEAD'
        if(target == unit):
            player1_units[unit] = 'DEAD'
    else:
        player1_units[target] = 'DEAD'
        if(target == unit):
            player2_units[unit] = 'DEAD'

def checkValidMove(unit, newLoc) :
    if(newLoc in gameBoard) :
        if player1Turn == True:
            loc = player1_units[unit]
        else:
            loc = player2_units[unit]
        if(newLoc == chr(ord(loc[0])+1)+loc[1] or newLoc == chr(ord(loc[0])-1)+loc[1] or newLoc == loc[0]+str(int(loc[1])+1) or loc[0]+str(int(loc[1])-1) ):
            #can only move up down right or left 1 space at a time
            if(isEmptySpace(newLoc)):
                if(gameBoard[newLoc] == 'mountain') :
                    if(unit == 'warrior'):
                        return True
                    else:
                        return False
                elif (gameBoard[newLoc] == 'lake') :
                    if(unit == 'sorceress'):
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                #warrior can move into enemy ranger
                if(unit == 'warrior'):
                    if(player1Turn):
                        if(newLoc == player2_units['ranger'] or newLoc == player2_units['warrior']):
                            return True
                        else:
                            return False
                    else:
                        if(newLoc == player1_units['ranger'] or newLoc == player1_units['warrior']):
                            return True
                        else:
                            return False
    else:
        return False

def moveUnit(player, unit, newLoc) :
    global player1_units;
    global player2_units;
    if(player == 'player1'):
        player1_units[unit] = newLoc
    else:
        player2_units[unit] = newLoc

def checkVisionBonus(unit, loc):
    if(gameBoard[loc] == 'plains'):
        return False
    elif(gameBoard[loc] == 'forest' and unit == 'ranger'):
        return True
    else:
        return False
    
    
################VISION#######################

def PublishVision(player):
    time.sleep(1)#helps RMQ
    dict = {}
    x = 0
    if(player == 'player1'):
        for each in player1_vision:
            dict[each] = x
            x = x+1
        channel.basic_publish(exchange='apptoserver',
                            routing_key='player1',
                            body=json.dumps(dict),
                            properties=pika.BasicProperties(delivery_mode = 2))
    else:
        #player2
        for each in player2_vision:
            dict[each] = x
            x = x+1
        channel.basic_publish(exchange='apptoserver',
                            routing_key='player2',
                            body=json.dumps(dict),
                            properties=pika.BasicProperties(delivery_mode = 2))
    print("published vision for "+player)

#Sets player vision
def UpdateVision():
    global player1_vision
    global player2_vision
    player1_vision = setPlayerVision(player1_units)
    player2_vision = setPlayerVision(player2_units)
    #vision message on RMQ
    PublishVision('player1')
    PublishVision('player2')

#######################################################PRINT BOARD#########################################################
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
#Where m=mountainl=lakef=forestp=plainss=sorceressr=rangerw=warrior
#A unit capitalized means that it is in its respective bonus-granting geo-location
#e.g. W in m, w in p or f
#def printBoardP2():
    ##TODO P2 units status message on RMQ
    ##CommandLine print
    #row =[]
    #letters = 'ABCDEFGH'
    #numbers = '12345678'
    #print('  '+numbers)
    #wloc = player2_units['warrior']
    #rloc = player2_units['ranger']
    #sloc = player2_units['sorceress']
    #otherWloc = player1_units['warrior']
    #otherRloc = player1_units['ranger']
    #otherSloc = player1_units['sorceress']
    #for let in letters:
        #for num in numbers:
            #if(let+num in player2_vision):# and (let+num == otherWloc or let+num == otherRloc or let+num == otherSloc)):
                #if(let+num == otherWloc):
                    #if(gameBoard[let+num] == 'mountain'):
                        #row.append('W')
                    #else:
                        #row.append('w')
                #elif(let+num == otherRloc):
                    #if(gameBoard[let+num] == 'forest'):
                        #row.append('R')
                    #else:
                        #row.append('r')
                #elif(let+num == otherSloc):
                    #if(gameBoard[let+num] == 'lake'):
                        #row.append('S')
                    #else:
                        #row.append('s')
            #if(gameBoard[let+num] == 'plains'):
                #if(let+num == wloc):
                    #row.append('w')
                #elif(let+num == rloc):
                    #row.append('r')
                #elif(let+num == sloc):
                    #row.append('s')
                #else:
                    #row.append('p')
            #elif(gameBoard[let+num] == 'mountain'):
                #if(let+num == wloc):
                    #row.append('W')
                #else:
                    #row.append('m')
            #elif(gameBoard[let+num] == 'forest'):
                #if(let+num == wloc):
                    #row.append('w')
                #elif(let+num == rloc):
                    #row.append('R')
                #elif(let+num == sloc):
                    #row.append('s')
                #else:
                    #row.append('f')
            #elif(gameBoard[let+num] == 'lake'):
                #if(let+num == sloc):
                    #row.append('S')
                #else:
                    #row.append('l')

        #print(let+' '+row[0]+row[1]+row[2]+row[3]+row[4]+row[5]+row[6]+row[7])
        #row.clear()

#def printBoardP1():
    ##TODO P1 units status on RMQ
    ##CommandLine print
    #row =[]
    #letters = 'ABCDEFGH'
    #numbers = '12345678'
    #print('  '+numbers)
    #wloc = player1_units['warrior']
    #rloc = player1_units['ranger']
    #sloc = player1_units['sorceress']
    #otherWloc = player2_units['warrior']
    #otherRloc = player2_units['ranger']
    #otherSloc = player2_units['sorceress']
    #for let in letters:
        #for num in numbers:
            #skipSpace = False
            #if(let+num in player1_vision):
                #if(let+num == otherWloc):
                    #skipSpace = True
                    #if(gameBoard[let+num] == 'mountain'):
                        #row.append('W')
                    #else:
                        #row.append('w')
                #elif(let+num == otherRloc):
                    #skipSpace = True
                    #if(gameBoard[let+num] == 'forest'):
                        #row.append('R')
                    #else:
                        #row.append('r')
                #elif(let+num == otherSloc):
                    #skipSpace = True
                    #if(gameBoard[let+num] == 'lake'):
                        #row.append('S')
                    #else:
                        #row.append('s')
            #if(skipSpace == False):
                #if(gameBoard[let+num] == 'plains'):
                    #if(let+num == wloc):
                        #row.append('w')
                    #elif(let+num == rloc):
                        #row.append('r')
                    #elif(let+num == sloc):
                        #row.append('s')
                    #else:
                        #row.append('p')
                #elif(gameBoard[let+num] == 'mountain'):
                    #if(let+num == wloc):
                        #row.append('W')
                    #else:
                        #row.append('m')
                #elif(gameBoard[let+num] == 'forest'):
                    #if(let+num == wloc):
                        #row.append('w')
                    #elif(let+num == rloc):
                        #row.append('R')
                    #elif(let+num == sloc):
                        #row.append('s')
                    #else:
                        #row.append('f')
                #elif(gameBoard[let+num] == 'lake'):
                    #if(let+num == sloc):
                        #row.append('S')
                    #else:
                        #row.append('l')

        #print(let+' '+row[0]+row[1]+row[2]+row[3]+row[4]+row[5]+row[6]+row[7])
        #row.clear()

#########################################################################################################################

def randomGeo():
    geo = ['plains', 'plains', 'plains', 'forest', 'mountain', 'lake']#(L454):for now just increase amount of plains in list until stable
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
def deployP1UnitFromCommandLine(unit, p1Deploy):
    global player1_units
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

def deployP2UnitFromCommandLine(unit, p2Deploy):
    global player2_units
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

def deployPlayerCommandLine(player):
    units = ['warrior', 'ranger', 'sorceress']
    if(player == 'player1'):
        for unit in units:
            deployP1UnitFromCommandLine(unit)
    else:
        #player2
        for unit in units:
            deployP2UnitFromCommandLine(unit)
            
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
    #channel.basic_publish(exchange='apptoserver',
                          #routing_key='player1',
                          #body='response')
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

warriorSelectedForTurn = False
rangerSelectedForTurn = False
sorceressSelectedForTurn = False
#Probably DEAD CODE
#def game_message(ch, method, properties, body):
    #global warriorSelectedForTurn
    #global rangerSelectedForTurn
    #global sorceressSelectedForTurn
    #body = json.loads(body.decode())
    #key = body.keys().pop()
    #print(key)
    ##player 1
    #if key[0] == '1':
        #if key[1] == 'w':
            ##selected warrior
            #warriorSelectedForTurn = True
        #elif key[1] == 'r':
            ##selected ranger
            #rangerSelectedForTurn = True
        #elif key[1] == 's':
            ##selected sorceress
            #sorceressSelectedForTurn = True
        ##elif key [1] == 'm':
            ###move
        ##elif key[1] == 'c':
            ##combat
    ###player 2
    ##else:
rCombatSpot = []
def publishAvailableRCombatSpaces(loc):
    global rCombatSpot
    dict = {}
    x = 0
    killableTypes = ['ranger', 'sorceress']
    for each in killableTypes:
        if player1Turn:
            if player2_units[each] in player1_vision:
                diff = getDistance(loc, player2_units[each])
                if(diff <= 3):
                    dict[player2_units[each]] = x
                    rCombatSpot.append(player2_units[each])
            
        else:
            #player 2's ranger
            if player1_units[each] in player2_vision:
                diff = getDistance(loc, player1_units[each])
                if(diff <= 3):
                    dict[player1_units[each]] = x
                    rCombatSpot.append(player1_units[each])
    if player1Turn:
        channel.basic_publish(exchange='apptoserver',
                                    routing_key='player1',
                                    body=json.dumps(dict))
        print("publish to p1 Available Combat Spaces")
    else:
        channel.basic_publish(exchange='apptoserver',
                                    routing_key='player2',
                                    body=json.dumps(dict))
        print("publish to p2 Available Combat Spaces")
        
sCombatSpot = []
def publishAvailableSCombatSpaces(loc):
    global sCombatSpot
    dict = {}
    x = 0
    killableTypes = ['warrior', 'sorceress']
    for each in killableTypes:
        if player1Turn:
            if player2_units[each] in player1_vision:
                diff = getDistance(loc, player2_units[each])
                if(diff <= 2):
                    dict[player2_units[each]] = x
                    sCombatSpot.append(player2_units[each])            
        else:
            #player 2's ranger
            if player1_units[each] in player2_vision:
                diff = getDistance(loc, player1_units[each])
                if(diff <= 2):
                    dict[player1_units[each]] = x
                    sCombatSpot.append(player1_units[each])
    if player1Turn:
        channel.basic_publish(exchange='apptoserver',
                                    routing_key='player1',
                                    body=json.dumps(dict))
        print("publish to p1 Available Combat Spaces")
    else:
        channel.basic_publish(exchange='apptoserver',
                                    routing_key='player2',
                                    body=json.dumps(dict))
        print("publish to p2 Available Combat Spaces")
        
def assignSelectedUnitForTurn(ch, method, properties, body):
    global warriorSelectedForTurn
    global rangerSelectedForTurn
    global sorceressSelectedForTurn
    body = body.decode()
    print("received "+body+" as selected unit.")
    if(body == 'w'):
        warriorSelectedForTurn = True
        rangerSelectedForTurn = False
        sorceressSelectedForTurn = False
    elif(body == 'r'):
        warriorSelectedForTurn = False
        rangerSelectedForTurn = True
        sorceressSelectedForTurn = False
    else:#(body == 's'):
        warriorSelectedForTurn = False
        rangerSelectedForTurn = False
        sorceressSelectedForTurn = True
    channel.basic_cancel(consumer_tag=consumer_id)
    
def consumeWhichUnit():
    global consumer_id
    consumer_id = channel.basic_consume(assignSelectedUnitForTurn, queue='server', no_ack=True)
    channel.start_consuming()
    
player1Turn = True
def handleGame():
    global player1Turn
    while gameOver == False:
        handleTurn()
        player1Turn = not player1Turn
        #Probably DEAD CODE
        #global consumer_id
        #consumer_id = channel.basic_consume(game_message, queue='server', no_ack=True)
        #channel.start_consuming()

def getAvailableMoveSpaces(loc):
    spaces = set()
    up = chr(ord(loc[0])-1)+loc[1]
    down = chr(ord(loc[0])+1)+loc[1]
    right = loc[0]+str(int(loc[1])+1)
    left = loc[0]+str(int(loc[1])-1)
    directions = set()
    directions.add(up)
    directions.add(down)
    directions.add(left)
    directions.add(right)
    if(warriorSelectedForTurn):
        for each in directions:
            if checkValidMove('warrior', each):
                spaces.add(each)
    elif rangerSelectedForTurn:
        for each in directions:
            if checkValidMove('ranger', each):
                spaces.add(each)
    else:
        for each in directions:
            if checkValidMove('sorceress', each):
                spaces.add(each)
    spaces.add(loc)#add current space to stay
    return spaces

availableMoveSpaces = None
def publishAvailableMoveSpaces(loc):
    time.sleep(1)
    global availableMoveSpaces
    dict = {}
    availableMoveSpaces = getAvailableMoveSpaces(loc)
    x = 0
    for each in availableMoveSpaces:
        dict[each] = x
        x = x+1
    if(player1Turn):
        print("publishing available move spaces to player1")
        channel.basic_publish(exchange='apptoserver',
                                routing_key='player1',
                                body=json.dumps(dict),
                                properties=pika.BasicProperties(delivery_mode = 2))
    else:
        channel.basic_publish(exchange='apptoserver',
                                routing_key='player2',
                                body=json.dumps(dict),
                                properties=pika.BasicProperties(delivery_mode = 2))

def assignNewSpace(ch, method, properties, body):
    global player1_units
    global player2_units
    body = body.decode()
    print("Move ", body, " received")
    if body in availableMoveSpaces:
        if warriorSelectedForTurn:
            if player1Turn:
                player1_units['warrior'] = body
                if player2_units['ranger'] == player1_units['warrior']:
                    player2_units['ranger'] = 'DEAD'
                elif player2_units['warrior'] == player1_units['warrior']:
                    player2_units['warrior'] = 'DEAD'
                    player1_units['warrior'] = 'DEAD'
            else:
                player2_units['warrior'] = body
                if player1_units['ranger'] == player2_units['warrior']:
                    player1_units['ranger'] = 'DEAD'
                elif player2_units['warrior'] == player1_units['warrior']:
                    player2_units['warrior'] = 'DEAD'
                    player1_units['warrior'] = 'DEAD'
        elif rangerSelectedForTurn:
            if player1Turn:
                player1_units['ranger'] = body
            else:
                player2_units['ranger'] = body
        else:
            if player1Turn:
                player1_units['sorceress'] = body
            else:
                player2_units['sorceress'] = body
        channel.basic_cancel(consumer_tag=consumer_id)

def consumeMovementOption():
    global consumer_id
    consumer_id = channel.basic_consume(assignNewSpace, queue='server', no_ack=True)
    print("consuming move to new space")
    channel.start_consuming()
    
def consumeRCombat():
    global consumer_id
    consumer_id = channel.basic_consume(killSorceress, queue='server', no_ack=True)
    print("consuming combat space")
    channel.start_consuming()

def killSorceress(ch, method, properties, body):
    if player1Turn:
        if body.decode() in rCombatSpot:
            if body.decode() == player2_units['sorceress']:
                player2_units['sorceress'] = 'DEAD'
            elif body.decode() == player2_units['ranger']:
                player1_units['ranger'] = 'DEAD'
                player2_units['ranger'] = 'DEAD'
            
    else:
        if body.decode() in rCombatSpot:
            if body.decode() == player1_units['sorceress']:
                player1_units['sorceress'] = 'DEAD'
            elif body.decode() == player1_units['ranger']:
                player1_units['ranger'] = 'DEAD'
                player2_units['ranger'] = 'DEAD'
    channel.basic_cancel(consumer_tag=consumer_id)
    
def consumeSCombat():
    global consumer_id
    consumer_id = channel.basic_consume(killWarrior, queue='server', no_ack=True)
    print("consuming combat space")
    channel.start_consuming()

def killWarrior(ch, method, properties, body):
    if player1Turn:
        if body.decode() in sCombatSpot:
            if body.decode() == player2_units['warrior']:
                player2_units['warrior'] = 'DEAD'
            elif body.decode() == player2_units['sorceress']:
                player1_units['sorceress'] = 'DEAD'
                player2_units['sorceress'] = 'DEAD'
    else:
        if body.decode() in sCombatSpot:
            if body.decode() == player1_units['warrior']:
                player1_units['warrior'] = 'DEAD'
            elif body.decode() == player1_units['sorceress']:
                player1_units['sorceress'] = 'DEAD'
                player2_units['sorceress'] = 'DEAD'
    channel.basic_cancel(consumer_tag=consumer_id)
    
def handleTurn():
    if(player1Turn == True):
        #player 1 turn
        #tell player 1 it's their turn
        notifyPlayerOfTurn('player1')
        #consume message for which unit they'll play with this turn
        consumeWhichUnit()
        if warriorSelectedForTurn:
            for x in range(0, 2):
                time.sleep(1)
                publishAvailableMoveSpaces(player1_units['warrior'])
                consumeMovementOption()
                publishOwnUnitInfo('1')
                publishOwnUnitInfo('2')
                publishUnitInfoToOpponent('2')
                publishUnitInfoToOpponent('1')
                UpdateVision()
                if player1_units['warrior'] == 'DEAD':
                    time.sleep(1)
                    #publish movement done
                    channel.basic_publish(exchange='apptoserver',
                                                routing_key='player1',
                                                body='d')
                    channel.basic_publish(exchange='apptoserver',
                                                routing_key='player2',
                                                body='n')
                    break
                #publish movement not done
                if x == 0:
                    time.sleep(1)
                    channel.basic_publish(exchange='apptoserver',
                                        routing_key='player1',
                                        body='n')
                    channel.basic_publish(exchange='apptoserver',
                                        routing_key='player2',
                                        body='y')
                else:
                    time.sleep(1)
                    #publish movement done
                    channel.basic_publish(exchange='apptoserver',
                                                routing_key='player1',
                                                body='y')
                    channel.basic_publish(exchange='apptoserver',
                                                routing_key='player2',
                                                body='n')
            if player1_units['warrior'] != 'DEAD':
                #enter combat
                publishAvailableMoveSpaces(player1_units['warrior'])
                consumeMovementOption()
            time.sleep(1)
            publishOwnUnitInfo('2')
            publishOwnUnitInfo('1')
            publishUnitInfoToOpponent('2')
            publishUnitInfoToOpponent('1')
            UpdateVision()
            ##end warrior
        elif rangerSelectedForTurn:
            time.sleep(1)
            publishAvailableMoveSpaces(player1_units['ranger'])
            consumeMovementOption()
            publishOwnUnitInfo('1')
            publishOwnUnitInfo('2')
            publishUnitInfoToOpponent('1')
            publishUnitInfoToOpponent('2')
            UpdateVision()
            #publish movement done
            print("publishing end movement")
            time.sleep(1)
            channel.basic_publish(exchange='apptoserver',
                                        routing_key='player1',
                                        body='y')
            channel.basic_publish(exchange='apptoserver',
                                        routing_key='player2',
                                        body='n')
            time.sleep(1)
            #enter combat
            publishAvailableRCombatSpaces(player1_units['ranger'])
            consumeRCombat()
            publishOwnUnitInfo('1')
            publishOwnUnitInfo('2')
            publishUnitInfoToOpponent('1')
            publishUnitInfoToOpponent('2')
            UpdateVision()
        else:# sorceressSelectedForTurn:
            for x in range(0, 3):
                    time.sleep(1)
                    publishAvailableMoveSpaces(player1_units['sorceress'])
                    consumeMovementOption()
                    publishOwnUnitInfo('1')
                    publishOwnUnitInfo('2')
                    publishUnitInfoToOpponent('1')
                    publishUnitInfoToOpponent('2')
                    UpdateVision()
                    #publish movement not done
                    if x == 0 or x == 1:
                        time.sleep(1)
                        channel.basic_publish(exchange='apptoserver',
                                            routing_key='player1',
                                            body='n')
                        channel.basic_publish(exchange='apptoserver',
                                            routing_key='player2',
                                            body='y')
                    else:
                        time.sleep(1)
                        #publish movement done
                        channel.basic_publish(exchange='apptoserver',
                                                    routing_key='player1',
                                                    body='y')
                        channel.basic_publish(exchange='apptoserver',
                                                    routing_key='player2',
                                                    body='n')
            #enter combat
            time.sleep(1)
            publishAvailableSCombatSpaces(player1_units['sorceress'])
            consumeSCombat()
            publishOwnUnitInfo('1')
            publishOwnUnitInfo('2')
            publishUnitInfoToOpponent('1')
            publishUnitInfoToOpponent('2')
            UpdateVision()
        updateGameOver()
    else:
        ##player 2 turn
        #tell player 2 it's their turn
        notifyPlayerOfTurn('player2')
        #consume message for which unit they'll play with this turn
        consumeWhichUnit()
        if warriorSelectedForTurn:
            for x in range(0, 2):
                time.sleep(1)
                publishAvailableMoveSpaces(player2_units['warrior'])
                consumeMovementOption()
                publishOwnUnitInfo('1')
                publishOwnUnitInfo('2')
                publishUnitInfoToOpponent('2')
                publishUnitInfoToOpponent('1')
                UpdateVision()
                if player2_units['warrior'] == 'DEAD':
                    time.sleep(1)
                    #publish movement done
                    channel.basic_publish(exchange='apptoserver',
                                                routing_key='player2',
                                                body='d')
                    channel.basic_publish(exchange='apptoserver',
                                                routing_key='player1',
                                                body='n')
                    break
                #publish movement not done
                if x == 0:
                    time.sleep(1)
                    channel.basic_publish(exchange='apptoserver',
                                        routing_key='player2',
                                        body='n')
                    channel.basic_publish(exchange='apptoserver',
                                        routing_key='player1',
                                        body='y')
                else:
                    time.sleep(1)
                    #publish movement done
                    channel.basic_publish(exchange='apptoserver',
                                                routing_key='player2',
                                                body='y')
                    channel.basic_publish(exchange='apptoserver',
                                                routing_key='player1',
                                                body='n')
            if player2_units['warrior'] != 'DEAD':
                #enter combat
                publishAvailableMoveSpaces(player2_units['warrior'])
                consumeMovementOption()
            time.sleep(1)
            publishOwnUnitInfo('2')
            publishOwnUnitInfo('1')
            publishUnitInfoToOpponent('2')
            publishUnitInfoToOpponent('1')
            UpdateVision()
            ##end warrior
        elif rangerSelectedForTurn:
            time.sleep(1)
            publishAvailableMoveSpaces(player2_units['ranger'])
            consumeMovementOption()
            publishOwnUnitInfo('1')
            publishOwnUnitInfo('2')
            publishUnitInfoToOpponent('2')
            publishUnitInfoToOpponent('1')
            UpdateVision()
            #publish movement done
            print("publishing end movement")
            time.sleep(1)
            channel.basic_publish(exchange='apptoserver',
                                        routing_key='player2',
                                        body='y')
            channel.basic_publish(exchange='apptoserver',
                                        routing_key='player1',
                                        body='n')
            time.sleep(1)
            #enter combat
            publishAvailableRCombatSpaces(player2_units['ranger'])
            consumeRCombat()
            publishOwnUnitInfo('2')
            publishOwnUnitInfo('1')
            publishUnitInfoToOpponent('2')
            publishUnitInfoToOpponent('1')
            UpdateVision()
        else:# sorceressSelectedForTurn:
            for x in range(0, 3):
                    time.sleep(1)
                    publishAvailableMoveSpaces(player2_units['sorceress'])
                    consumeMovementOption()
                    publishOwnUnitInfo('1')
                    publishOwnUnitInfo('2')
                    publishUnitInfoToOpponent('2')
                    publishUnitInfoToOpponent('1')
                    UpdateVision()
                    #publish movement not done
                    if x == 0 or x == 1:
                        time.sleep(1)
                        channel.basic_publish(exchange='apptoserver',
                                            routing_key='player2',
                                            body='n')
                        channel.basic_publish(exchange='apptoserver',
                                            routing_key='player1',
                                            body='y')
                    else:
                        time.sleep(1)
                        #publish movement done
                        channel.basic_publish(exchange='apptoserver',
                                                    routing_key='player2',
                                                    body='y')
                        channel.basic_publish(exchange='apptoserver',
                                                    routing_key='player1',
                                                    body='n')
            #enter combat
            time.sleep(1)
            publishAvailableSCombatSpaces(player2_units['sorceress'])
            consumeSCombat()
            publishOwnUnitInfo('2')
            publishOwnUnitInfo('1')
            publishUnitInfoToOpponent('2')
            publishUnitInfoToOpponent('1')
            UpdateVision()
        updateGameOver()

def notifyPlayerOfTurn(player):
    time.sleep(1)
    if(player == 'player1'):
        channel.basic_publish(exchange='apptoserver',
                          routing_key='player1',
                          body='player1',
                          properties=pika.BasicProperties(delivery_mode = 2))
        channel.basic_publish(exchange='apptoserver',
                          routing_key='player2',
                          body='player1',
                          properties=pika.BasicProperties(delivery_mode = 2))
    else:
        #player 2
        channel.basic_publish(exchange='apptoserver',
                          routing_key='player1',
                          body='player2')
        channel.basic_publish(exchange='apptoserver',
                          routing_key='player2',
                          body='player2')
    print('Turn Notification Published')

def deploy_message(ch, method, properties, body):
    body = json.loads(body.decode())
    if('1w' in body):
        space = body['1w']
        deployP1UnitFromCommandLine('warrior', space)
    elif('1r' in body):
        space = body['1r']
        deployP1UnitFromCommandLine('ranger', space)
    elif('1s' in body):
        space = body['1s']
        deployP1UnitFromCommandLine('sorceress', space)
    elif('2w' in body):
        space = body['2w']
        deployP2UnitFromCommandLine('warrior', space)
    elif('2r' in body):
        space = body['2r']
        deployP2UnitFromCommandLine('ranger', space)
    elif('2s' in body):
        space = body['2s']
        deployP2UnitFromCommandLine('sorceress', space)
    if(player1_units['warrior'] != 'DEPLOY' and player1_units['ranger'] != 'DEPLOY' and player1_units['sorceress'] != 'DEPLOY' and player2_units['warrior'] != 'DEPLOY' and player2_units['ranger'] != 'DEPLOY' and player2_units['sorceress'] != 'DEPLOY'):
        channel.basic_cancel(consumer_tag=consumer_id)
        
def handleDeployment():
    while (player1_units['warrior'] == 'DEPLOY' or player1_units['ranger'] == 'DEPLOY' or player1_units['sorceress'] == 'DEPLOY' or player2_units['warrior'] == 'DEPLOY' or player2_units['ranger'] == 'DEPLOY' or player2_units['sorceress'] == 'DEPLOY'):
        global consumer_id
        consumer_id = channel.basic_consume(deploy_message, queue='server', no_ack=True)
        channel.start_consuming()
    publishUnitInfoToOpponent('1')
    publishUnitInfoToOpponent('2')
    

def publishUnitInfoToOpponent(num):
    time.sleep(1)
    if num == '2':
        channel.basic_publish(exchange='apptoserver',
                            routing_key='player1',
                            body=json.dumps(player2_units),
                            properties=pika.BasicProperties(delivery_mode = 2))
        print('published opponent unit info to player 1')
    else:
        channel.basic_publish(exchange='apptoserver',
                            routing_key='player2',
                            body=json.dumps(player1_units),
                            properties=pika.BasicProperties(delivery_mode = 2))
        print('published opponent unit info to player 2')
    
def publishOwnUnitInfo(num):
    if num == '1':
        channel.basic_publish(exchange='apptoserver',
                            routing_key='player1',
                            body=json.dumps(player1_units),
                            properties=pika.BasicProperties(delivery_mode = 2))
        print("published own unit info to player 1")
    else:
        channel.basic_publish(exchange='apptoserver',
                            routing_key='player2',
                            body=json.dumps(player2_units),
                            properties=pika.BasicProperties(delivery_mode = 2))
        print("published own unit info to player 2")
#####################################################################################################

def main():
    connectRMQ()
    checkIfPlayersConnected()
    createBoard()
    #push gameBoard through message queue to both players
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
    UpdateVision()
    handleGame()
    #TODO ShowEndResults()

if __name__ == "__main__":
    main()
