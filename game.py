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

def setPlayerVision(players_units):
    vision = set()
    wloc = players_units['warrior']
    rloc = players_units['ranger']
    sloc = players_units['sorceress']
    units_loc = [wloc, rloc, sloc]
    for each in units_loc:
    #warriors vision
        if(each == wloc):
            if(each in gameBoard):
                if(gameBoard[each] == 'forest'):
                    #1 less vision
                    #add vision to warrior space
                    vision.add(each)
                    row = each[0]
                    col = each[1]
                    #look right
                    space = row+str(int(col)+1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)+2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                    #look left
                    row = each[0]
                    col = each[1]
                    space = row+str(int(col)-1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)-2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                    #look forward
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)+1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)+2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                    #look back
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)-1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)-2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                else:
                    #add vision to warrior space normally
                    vision.add(each)
                    row = each[0]
                    col = each[1]
                    #look right
                    space = row+str(int(col)+1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)+2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = row+str(int(col)+3)
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                    #look left
                    row = each[0]
                    col = each[1]
                    space = row+str(int(col)-1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)-2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = row+str(int(col)-3)
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                    #look forward
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)+1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)+2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = chr(ord(row)+3)+col
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                    #look back
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)-1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)-2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = chr(ord(row)-3)+col
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
        #ranger's vision
        elif(each == rloc):
            if(each in gameBoard):
                if(gameBoard[each] == 'forest'):
                    #5 space vision
                    vision.add(each)
                    row = each[0]
                    col = each[1]
                    #look right
                    space = row+str(int(col)+1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)+2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = row+str(int(col)+3)
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                            space = row+str(int(col)+4)
                                            if(space in gameBoard):
                                                #add 4th right space
                                                vision.add(space)
                                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                                    space = row+str(int(col)+5)
                                                    if(space in gameBoard):
                                                        #add 5th right space
                                                        vision.add(space)
                    #look left
                    row = each[0]
                    col = each[1]
                    space = row+str(int(col)-1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)-2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = row+str(int(col)-3)
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                            space = row+str(int(col)-4)
                                            if(space in gameBoard):
                                                #add 4th right space
                                                vision.add(space)
                                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                                    space = row+str(int(col)-5)
                                                    if(space in gameBoard):
                                                        #add 5th right space
                                                        vision.add(space)
                    #look forward
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)+1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)+2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = chr(ord(row)+3)+col
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                            space = chr(ord(row)+4)+col
                                            if(space in gameBoard):
                                                #add 4th right space
                                                vision.add(space)
                                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                                    space = chr(ord(row)+5)+col
                                                    if(space in gameBoard):
                                                        #add 5th right space
                                                        vision.add(space)
                                        
                    #look back
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)-1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)-2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = chr(ord(row)-3)+col
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                            space = chr(ord(row)-4)+col
                                            if(space in gameBoard):
                                                #add 4th right space
                                                vision.add(space)
                                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                                    space = chr(ord(row)-5)+col
                                                    if(space in gameBoard):
                                                        #add 5th right space
                                                        vision.add(space)
                                    
                else:
                    #4 space vision
                    vision.add(each)
                    row = each[0]
                    col = each[1]
                    #look right
                    space = row+str(int(col)+1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)+2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = row+str(int(col)+3)
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                            space = row+str(int(col)+4)
                                            if(space in gameBoard):
                                                #add 4th right space
                                                vision.add(space)
                    #look left
                    row = each[0]
                    col = each[1]
                    space = row+str(int(col)-1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)-2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = row+str(int(col)-3)
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                            space = row+str(int(col)-4)
                                            if(space in gameBoard):
                                                #add 4th right space
                                                vision.add(space)
                    #look forward
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)+1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)+2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = chr(ord(row)+3)+col
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                            space = chr(ord(row)+4)+col
                                            if(space in gameBoard):
                                                #add 4th right space
                                                vision.add(space)
                                        
                    #look back
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)-1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)-2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = chr(ord(row)-3)+col
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                            space = chr(ord(row)-4)+col
                                            if(space in gameBoard):
                                                #add 4th right space
                                                vision.add(space)
        #sorceress vision
        elif(each == sloc):
            if(each in gameBoard):
                if(gameBoard[each] == 'forest'):
                    #1 less
                    vision.add(each)
                    row = each[0]
                    col = each[1]
                    #look right
                    space = row+str(int(col)+1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)+2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                    #look left
                    row = each[0]
                    col = each[1]
                    space = row+str(int(col)-1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)-2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                    #look forward
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)+1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)+2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                    #look back
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)-1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)-2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                else:
                    #3 vision
                    vision.add(each)
                    row = each[0]
                    col = each[1]
                    #look right
                    space = row+str(int(col)+1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)+2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = row+str(int(col)+3)
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                    #look left
                    row = each[0]
                    col = each[1]
                    space = row+str(int(col)-1)
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = row+str(int(col)-2)
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = row+str(int(col)-3)
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                    #look forward
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)+1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)+2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = chr(ord(row)+3)+col
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
                    #look back
                    row = each[0]
                    col = each[1]
                    space = chr(ord(row)-1)+col
                    if(space in gameBoard):
                        #add space to right
                        vision.add(space)
                        if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                            space = chr(ord(row)-2)+col
                            if(space in gameBoard):
                                #add 2nd right space
                                vision.add(space)
                                if(gameBoard[space] == 'plains' or gameBoard[space] == 'lake'):
                                    space = chr(ord(row)-3)+col
                                    if(space in gameBoard):
                                        #add 3rd right space
                                        vision.add(space)
    return vision
        
            

def takeTurns():
    #TODO wait to receive message, which will be from P1
    #if(play1_player1.keys() == 'warrior'):
        #if(warriorMoveValid()):
           # executeWarriorMove(play1_player1)
           return None

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

def randomGeo():
    geo = ['plains', 'forest', 'mountain', 'lake']
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
    print(gameBoard)
    w1Deploy = input("Player 1: Where for W")
    r1Deploy = input("Player 1: Where for R")
    s1Deploy = input("Player 1: Where for S")
    w2Deploy = input("Player 2: Where for W")
    r2Deploy = input("Player 2: Where for R")
    s2Deploy = input("Player 2: Where for S")
    p1 = {'warrior':w1Deploy, 'ranger':r1Deploy, 'sorceress':s1Deploy}
    p2 = {'warrior':w2Deploy, 'ranger':r2Deploy, 'sorceress':s2Deploy}
    #TODO push gameBoard through message queue
    #TODO p1 and p2 will be messages sent from services.py based on android input
    afterDeployInit(p1, p2)
    while(~gameOver):
        takeTurns()
    #TODO ShowEndResults()
    return None

if __name__ == "__main__":
    main()
