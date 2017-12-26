#!/usr/bin/env/python
import pika
import json
import getopt
import sys
import os
from rmq_params import rmq_params

cred = pika.PlainCredentials(rmq_params['username'], rmq_params['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_params['bridgeip'], virtual_host=rmq_params['vhost'], credentials=cred))
channel = connection.channel();
channel.exchange_declare(exchange='apptoserver', exchange_type='direct')
print("Connected to vhost'" + rmq_params["vhost"] + "' on RMQ server at 'localhost' as user'" + rmq_params["username"] + "'")

state = "mainMenu"
loggedIn = False
user = ""

def clearScreen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def logInPrompt():
    global loggedIn
    global user
    clearScreen()
    print("Login")
    print("To go back type 'back'")
    user = input("Username: ")
    if user == "back":
        return None
    pwd = input("Password: ")
    if pwd == "back":
        return None
    cred = json.dumps(["Login", {"Username": user, "Password": pwd}])
    channel.basic_publish(exchange="apptoserver", routing_key="server", body=cred)
    loggedIn = True

def createAccountPrompt():
    global loggedIn
    global user
    clearScreen()
    print("Create Account")
    print("To go back type 'back'")
    user = input("Username: ")
    if user == "back":
        return None
    pwd = input("Password: ")
    if pwd == "back":
        return None
    cred = json.dumps(["Create Account", {"Username": user, "Password": pwd}])
    channel.basic_publish(exchange="apptoserver", routing_key="server", body=cred)
    loggedIn = True

def logoutPrompt():
    global loggedIn
    clearScreen()
    while True:
        print("Are you sure you wish to logout?")
        text = input("Y/N: ")
        if text == "Y":
            loggedIn = False
            break;
        elif text == "N":
            break
        else: # text != "Y" or text != "N"
            print("Invalid choice: " + text)

while True:
    clearScreen()
    if state == "mainMenu":
        if not loggedIn:
            print("Login")
            print("Create Account")
            text = input("Choose: ")
            if text == "Login":
                logInPrompt()
                continue
            elif text == "Create Account":
                createAccountPrompt()
                continue
            else: # invalid text
                print("Invalid Choice: " + text)
                continue
        else: #loggedin
            print("User: " + user)
            print("Logout")
            print("Play")
            print("Settings")
            text = input("Choose: ")
            if text == "Logout":
                logoutPrompt()
                continue;
            elif text == "Play":
                state = "playGame"
                continue
            elif text == "Settings":
                state = "Settings"
                continue
            else:
                print("Invalid Choice: " + text)
                continue
    elif state == "playGame":
        print("Entered playGame state")
        text = input("Type anything to go back to main menu: ")
        state = "mainMenu"

    else: # state == "Settings"
        print("Entered Settings state")
        text = input("Type anything to go back to main menu: ")
        state = "mainMenu"
