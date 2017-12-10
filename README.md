# net_apps_final

To simulate current build:

1. run instance of bridge.py:       python3 bridge.py
2. run instance of game.py:         python3 game.py
3. run instance of client_beta.py:  python3 client_beta.py -u 'player1'
4. run instance of client_beta.py:  python3 client_beta.py -u 'player2'

Comment out checkIfPlayersConnected() and the publish methods to work on game.py

Fill in the necessary parameters.
bridgeip is the ip address of your machine running the bridge
For vhost, username, and password, you'll have to create the vhost on your rabbitmq server using rabbitmqctl.
Exchanges and queues are created within bridge.py.

### NEW BUILD PLAN ###
App has two states: Main Menu and Play Game.

Main Menu state:
- can query db for info and stats
- can login
- before playing match making system finds opponent
- moves to Play Game state when opponent is found

Play Game state:
- query for randomized game board
- each player deploys units
- enters while loop where possible moves are based on turns
- while loop breaks when one side loses
- can restart Play Game state or go to Main Menu

Server is in an eternal state of message consumption. Only reacts to consumed messages.
- every instance of a game is stored in a document containing all necessary info (i.e. map, users, unit location and vision, etc.)
- document is updated for every valid message from associated users
- keeps track of turns to remain in sync with apps
- essentially:
def on_message(ch, method, header, body):
  if  body #query from client:
    do stuff
  elif another condition:
    do other stuff

def main():
  start_consuming #consumes message eternally
