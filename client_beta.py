#!/usr/bin/env/python
import pika
import json
import getopt
import sys
import os
import curses
from rmq_params import rmq_params
from enum import Enum

cred = pika.PlainCredentials(rmq_params['username'], rmq_params['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_params['bridgeip'], virtual_host=rmq_params['vhost'], credentials=cred))
channel = connection.channel();
print("Connected to vhost'" + rmq_params["vhost"] + "' on RMQ server at 'localhost' as user'" + rmq_params["username"] + "'")

state = "mainMenu"
loggedIn = False
user = ""
selector = 0
mainMenu = ["Login", "Play", "Settings"]

def mainMenu(stdscr):
    attributes = {}
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    attributes['highlighted'] = curses.color_pair(2)

    c = 0
    option = 0
    while c != 10:
        stdscr.erase()
        stdscr.addstr("What is your class?\n", curses.A_UNDERLINE)
        for i in range(len(mainMenu)):
            if i == option:
                attr = attributesw['highlighted']
            else:
                attr = attributes['normal']
            stdscr.addstr("{0}. ".format(i + 1))
            stdscr.addstr(mainMenu[i] + '\n', attr)
        c = stdscr.getch()
        if c == curses.KEY_UP and option > 0:
            option -= 1
        elif c == curses.KEY_DOWN and option < len(mainMenu) - 1:
            option += 1
    stdscr.addstr("You chose {0}".format(mainMenu[option]))
    stdscr.getch()

while True:
    clear = lambda: os.system('cls')
    clear()
    if state == "mainMenu":
        curses.wrapper(mainMenu)
    elif state == "playGame":
        continue;
    else: # state == "settings"
        continue;
