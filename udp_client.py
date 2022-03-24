import time
from socket import *
import asyncio
import time

class Sender:

    def __init__(self, serverIP = "192.168.123.12", port=13, delay=0.016):
        self.serverIP = serverIP
        self.port = port
        self.delay = delay
        self.mode = 0
        self.action = 0

    def send_date(self):
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(1)
        addr = (self.serverIP, self.port)
        while True:
            srr = f'{self.mode};{self.action}'
            clientSocket.sendto(srr.encode(), addr)
            print(srr)
            time.sleep(self.delay)

    def change_value(self, mode, action):
        self.mode = mode
        self.action = action


