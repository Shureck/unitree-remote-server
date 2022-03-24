# We will need the following module to generate randomized lost packets
import random
from socket import *
import nltk_c

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('0.0.0.0', 1233))

while True:
    message, address = serverSocket.recvfrom(1024)
    text = message.decode('utf-8','ignore')
    nltk_c.commands_indentify(text)
    print(address, message.decode('utf-8','ignore'))