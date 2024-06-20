import threading

import pygame
import random
import socket
import struct
from Node import Node
class EndPoint(Node):
    def __init__(self, x, y, name, img , info = ""):
        super().__init__(x, y, name, 40, (0, 0, 255), info)
        self.text_bg_color = (200, 200, 200)
        self.img = img
        new_size = (50, 50)
        self.img = pygame.transform.scale(self.img, new_size)
        self.dragging = False
        self.recievedPackets = []
        self.isChosenColor = False
        self.acknowImg = pygame.image.load("acknowledgment.png")
        self.acknowImg = pygame.transform.scale(self.acknowImg, (30, 30))
        self.acknowNode = self
        self.shouldShowAcknow = False
        mac_digits = []
        for _ in range(6):
            mac_digits.append('%02x' % random.randint(0, 255))
        self.MACadress = ':'.join(mac_digits)
        ip_bytes = [random.randint(0, 255) for _ in range(4)]
        self.ip_address = socket.inet_ntoa(struct.pack('BBBB', *ip_bytes))
        self.info = "MAC: " + self.MACadress + "\n" + "IP: " + self.ip_address

    def get_info(self):
        return f'{self.info}'
    def recieve(self, packet):
        self.recievedPackets.append(packet)
        print(f"{self.name} recieved a packet")
    def send(self, packet):
        print(f"Sending packet from {self.name}")

    def startAcknow(self):
        self.shouldShowAcknow = True
        self.acknowNode = self
        threading.Timer(3, self.stopAcknow).start()


    def connect(self, screen):
        line_color = (255, 0, 0)
        pygame.draw.line(screen, line_color, (self.x, self.y), (self.previousNode.x, self.previousNode.y), 2)


    def isMouseOver(self):

        return self.x - self.size // 2 < pygame.mouse.get_pos()[0] < self.x + self.size // 2 and \
            self.y - self.size // 2 < pygame.mouse.get_pos()[1] < self.y + self.size // 2

    def setToChosenColor(self):
        target_color = (0, 122, 0)
        if(self.isChosenColor):
            return
        for x in range(self.img.get_width()):
            for y in range(self.img.get_height()):

                current_color = self.img.get_at((x, y))
                if current_color.a != 0:
                    new_color = current_color
                    if(new_color[1] + target_color[1] > 255):
                        new_color[1] = 255
                    else:
                        new_color[1] += target_color[1]
                    self.isChosenColor = True
                    self.img.set_at((x, y), new_color)

    def setToDefaultColor(self):
        if not self.isChosenColor:
            return
        target_color = (0, 122, 0)
        for x in range(self.img.get_width()):
            for y in range(self.img.get_height()):
                current_color = self.img.get_at((x, y))
                if current_color.a != 0:
                    new_color = current_color
                    if(new_color[1] - target_color[1] < 0):
                        new_color[1] = 0
                    else:
                        new_color[1] -= target_color[1]

                    self.isChosenColor = False
                    self.img.set_at((x, y), new_color)

    def tryShowAcknowledgment(self, screen):
        if self.shouldShowAcknow:
            screen.blit(self.acknowImg,
                        (self.acknowNode.x - self.img.get_width() // 2, self.acknowNode.y - self.img.get_height() // 2 - 10))

    def stopAcknow(self):
        self.shouldShowAcknow = False