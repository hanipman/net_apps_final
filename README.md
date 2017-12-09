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
