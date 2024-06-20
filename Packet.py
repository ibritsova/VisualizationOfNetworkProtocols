
import pygame
import random
import socket
import struct
from InputBox import InputBox
from Node import Node


class Packet(Node):

    def __init__(self, img, x, y, name, data ="", destinationIP="", sourceIP=""):
        super().__init__(x, y, name, 40, (255, 0, 0), data)
        self.img = pygame.image.load("packet.png")
        self.destinationIP = destinationIP
        self.sourceIP = sourceIP
        self.text_bg_color = (200, 200, 200)
        self.img = img
        self.data = data
        new_size = (50, 50)
        self.img = pygame.transform.scale(self.img, (50,50))
        self.lastSender = None
        mac_digits = []
        for _ in range(6):
            mac_digits.append('%02x' % random.randint(0, 255))
        self.MACadress = ':'.join(mac_digits)
        ip_bytes = [random.randint(0, 255) for _ in range(4)]
        self.ip_address = socket.inet_ntoa(struct.pack('BBBB', *ip_bytes))
        self.infoAddress = "MAC: " + self.MACadress + "\n" + "IP: " + self.ip_address

    def receiveAndSendFurther(self, packet):
        print(f"Packet received: {packet.name}")

    def get_info(self):
        return f"{self.infoAddress}"


    def send(self, packet):
        print(f"Sending packet with name: {packet.name}")

    def connect(self, node):
        print("Connecting packet to another node")

    def getCopy(self):
        return Packet(self.img,self.x,self.y,self.name,self.data,self.destinationIP,self.sourceIP)

    def isMouseOver(self):
        return self.x - self.size // 2 < pygame.mouse.get_pos()[0] < self.x + self.size // 2 and \
            self.y - self.size // 2 < pygame.mouse.get_pos()[1] < self.y + self.size // 2

    def createInputBox(self):
        inputBox = InputBox(250, 650, 500, 100,"", self)
        return inputBox

    def putData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def getSize(self):
        return len(self.data)

    def isDestinationIPSet(self):
        return not self.destinationIP == ""