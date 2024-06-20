import threading
from functools import partial

import pygame
import sys
import time
import random
import socket
import struct
from EndPoint import EndPoint
from Node import Node
from Packet import Packet

class HUB(Node):
    endPoints = []
    subHubs = []
    packetsOnTheWay = []
    recievedPackets = []

    def __init__(self, x, y, name,img, info = "", sysIndex = 0, drawer = None):
        super().__init__(x, y, name, 40, (0, 255, 0), info)
        self.text_bg_color = (200, 200, 200)
        self.img = img
        new_size = (50, 50)
        self.endPoints = []
        self.subHubs = []
        self.sysIndex = sysIndex
        self.drawer = drawer
        self.dragging = False
        self.acknowImg = pygame.image.load("acknowledgment.png")
        self.acknowImg = pygame.transform.scale( self.acknowImg, (30, 30))
        self.acknowNode = self
        self.shouldShowAcknow = False
        self.isChosenColor = False
        self.recievedPackets = []


        mac_digits = []
        for _ in range(6):
            mac_digits.append('%02x' % random.randint(0, 255))
        self.MACadress = ':'.join(mac_digits)
        ip_bytes = [random.randint(0, 255) for _ in range(4)]
        self.ip_address = socket.inet_ntoa(struct.pack('BBBB', *ip_bytes))
        self.info = "MAC: " + self.MACadress + "\n" + "IP: " + self.ip_address




    def addEndPoint(self, node):
        self.endPoints.append(node)


    def addSubHub(self, hub):
        self.subHubs.append(hub)

    def recieveAndSendFurther(self, packet):
        print(f"{self.name} {self.sysIndex} recieved a packet")
        print("Recieve Data: " + packet.getData())
        self.recievedPackets.append(packet)
        self.send(packet)

    def send(self, packet):
        print(f"Sending packet from {self.name} {self.sysIndex}")
        print("Send Data: " + packet.getData())
        for endPoint in self.endPoints:
            copyPacket =  packet.getCopy()
            self.drawer.listOfPackets.append(copyPacket)
            self.packetsOnTheWay.append(copyPacket)
            self.packetsOnTheWay.append(endPoint)
        for subHub in self.subHubs:
            if subHub == packet.lastSender:
                continue
            copyPacket = packet.getCopy()
            copyPacket.lastSender = self
            print("Pacadd :" + copyPacket.destinationIP)

            self.drawer.listOfPackets.append(copyPacket)
            self.packetsOnTheWay.append(copyPacket)
            self.packetsOnTheWay.append(subHub)
                # time.sleep(1)
        if packet in self.drawer.listOfPackets:
           self.drawer.listOfPackets.remove(packet)

    def updateSending(self):
        self.tryShowAcknowledgment(self.drawer.screen)
        for endPoint in self.endPoints:
            endPoint.tryShowAcknowledgment(self.drawer.screen)
        if(len(self.packetsOnTheWay) == 0): return
        for i in range(1,len(self.packetsOnTheWay),2):
            if i < len(self.packetsOnTheWay) :
                packet = self.packetsOnTheWay[i - 1]
                destination = self.packetsOnTheWay[i]
                if abs(packet.x - destination.x) < 1 and abs(packet.y - destination.y) < 1:
                    if type(destination) == HUB:
                        destination.recieveAndSendFurther(packet)
                        if(packet.destinationIP == destination.ip_address):
                            self.shouldShowAcknow = True
                            self.acknowNode = destination
                            threading.Timer(2, self.stopAcknow).start()
                    elif type(destination) == EndPoint:
                        destination.recieve(packet)
                        if(packet.destinationIP == destination.ip_address):
                            destination.startAcknow()
                        self.drawer.listOfPackets.remove(packet)

                    self.packetsOnTheWay.remove(packet)
                    self.packetsOnTheWay.remove(destination)

                else:
                    self.move(packet, destination)

    def move(self, packet, node):
        if (type(packet) != Packet):
            print(f"BLA")
        speed = 2
        direction = pygame.Vector2(node.x, node.y) - pygame.Vector2(packet.x, packet.y)
        velocity = direction.normalize() * speed
        packet.x += velocity.x
        packet.y += velocity.y

    def connect(self, screen, nodeToConnect):
        line_color = (255, 0, 0)
        pygame.draw.line(screen, line_color, (self.x, self.y), (nodeToConnect.x, nodeToConnect.y), 2)

    def connectToEndPoints(self, screen):
        line_color = (255, 0, 0)
        for endPoint in self.endPoints:
            endPoint.draw(screen)
            pygame.draw.line(screen, line_color, (self.x, self.y), (endPoint.x, endPoint.y), 2)

    def onMouseOver(self, mouse_pos, screen):

        if self.isMouseOver(mouse_pos):

            info_surface = pygame.Surface((200, 50))
            info_surface.fill((255, 0, 0))
            font = pygame.font.Font(None, 24)
            text = font.render(self.info, True, (0, 0, 0), self.text_bg_color)
            info_surface.blit(text, (5, 5))


            screen.blit(info_surface, (self.x - 100, self.y - 75))

    def isMouseOver(self):
        return self.x - self.size // 2 < pygame.mouse.get_pos()[0] < self.x + self.size // 2 and \
               self.y - self.size // 2 < pygame.mouse.get_pos()[1] < self.y + self.size // 2
    def getMessage(self):
        message = ""
        for packet in self.recievedPackets:
            message += packet.info
            message += '\n'
        return message

    def getIPinfo(self):
        return "IP:" + self.ip_address

    def getMACinfo(self):
        return "MAC:" + self.MACadress

    def setToChosenColor(self):
        target_color = (0, 122, 0)
        print("FUCK")
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
            screen.blit(self.acknowImg, (self.acknowNode.x - self.img.get_width() // 2, self.acknowNode.y - self.img.get_height() // 2 - 10))


    def stopAcknow(self):
        self.shouldShowAcknow = False