#This file serves as a command line based client
#As we approach the final iteration, we'll be implementing this
#in the Android environment
import sys
import getopt
def getRMQ_server_address():
    global RMQ_server_address
    
    #Get RMQ_server_address
    try:
        opts, args = getopt.getopt(sys.argv[1:],"s:")
    except getopt.GetoptError:
            print("bridge.py -s <RMQ_SERVER_ADDRESS>")
            sys.exit(2)
    if(len(opts) < 1):
        print("Usage:")
        print("bridge.py -s <RMQ_SERVER_ADDRESS>")
    for opt, arg in opts:
            if opt == "-s":
                    RMQ_server_address = arg
def main():
    #TODO
    #Get RMQ server address
    #print and get login info
    #connect to rmq
    #print command line (accepting only 'play') ~!concept of a main menu.
    #connect to game exchange
    #wait for other player to connect to game
    #print board
    #deploy
    #print board
if __name__ == "__main__":
    main()
