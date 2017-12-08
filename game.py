#This module handles the game mechanics

#imports
import random

#import testGame

#define globals
player1_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
player2_units = {'warrior':'DEPLOY', 'ranger':'DEPLOY', 'sorceress':'DEPLOY'}
player1_vision = set()
player2_vision = set()
gameBoard = None

gameOver = False

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

def checkValidMove(unit, loc) :
    if(loc in gameBoard) :
        if(gameBoard[loc] == 'mountain') :
            if(unit == 'warrior'):
                return True;
            else :
                return False;
        else if (gameBoard[loc] == 'forest') :
            if(unit == 'ranger') :
                return True;
            else :
                return False;
        else if (gameBoard[loc] == 'lake') :
            if(unit == 'sorceress'):
                return True;
            else :
                return False;
        else :
            return True;
    else :
        return False;

def checkVisionBonus(unit, loc) :
    if(gameBoard[loc] == 'plains'):
        return False;
    else if (gameBoard[loc] == 'forest' and unit == 'ranger') :
        return True;
    else return False;

def afterDeployInit(p1, p2):
    global player1_units
    global player2_units
    global player1_vision
    global player2_vision
    player1_units = p1
    player2_units = p2
    player1_vision = setPlayerVision(player1_units)
    player2_vision = setPlayerVision(player2_units)
    print("Player1's Vision = " + str(player1_vision))
    print("Player2's Vision = " + str(player2_vision))

def printBoard(player_units):
    row =[]
    letters = 'ABCDEFGH'
    numbers = '12345678'
    print('  '+numbers)
    wloc = player_units['warrior']
    for let in letters:
        for num in numbers:
            if(gameBoard[let+num] == 'plains'):
                if(let+num == wloc):
                    row.append('w')
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
                else:
                    row.append('f')
            elif(gameBoard[let+num] == 'lake'):
                row.append('l')
                    
        print(let+' '+row[0]+row[1]+row[2]+row[3]+row[4]+row[5]+row[6]+row[7])
        row.clear()

def randomGeo():
    geo = ['plains', 'plains','forest', 'mountain', 'lake']
    return random.choice(geo)

def createBoard():
    board = {}
    letters = 'ABCDEFGH'
    numbers = '12345678'
    for x in letters:
        for y in numbers:
            board[x+y] = randomGeo()
    return board

def main():
    global gameBoard
    gameBoard = createBoard()
    #TODO REMOVE THIS CODE
    printBoard(player1_units)
    w1Deploy = input("Player 1: Where for W")
    #r1Deploy = input("Player 1: Where for R")
    #s1Deploy = input("Player 1: Where for S")
    #w2Deploy = input("Player 2: Where for W")
    #r2Deploy = input("Player 2: Where for R")
    #s2Deploy = input("Player 2: Where for S")
    p1 = {'warrior':w1Deploy, 'ranger':'DEAD', 'sorceress':'DEAD'}
    p2 = {'warrior':'DEAD', 'ranger':'DEAD', 'sorceress':'DEAD'}
    #TODO push gameBoard through message queue
    #TODO p1 and p2 will be messages sent from services.py based on android input
    afterDeployInit(p1, p2)
    printBoard(player1_units)
    #while(~gameOver):
        #takeTurns()
    #TODO ShowEndResults()

if __name__ == "__main__":
    main()
