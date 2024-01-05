import pygame
from visualization.Node import Node


class Packet(Node):
    all_packets = []
    destinationIP = ""
    sourceIP = ""
    protocol = ""
    totalLength = ""

    def __init__(self, x, y, name,info = "", destinationIP="", sourceIP="", protocol="", totalLength=""):
        super().__init__(x, y, name, 40, (255, 0, 0), info)
        Packet.all_packets.append(self)
        self.destinationIP = destinationIP
        self.sourceIP = sourceIP
        self.protocol = protocol
        self.totalLength = totalLength
        self.text_bg_color = (200, 200, 200)
        self.img = pygame.image.load("packet.png")
        new_size = (50, 50)
        self.img = pygame.transform.scale(self.img, new_size)

    def receive(self, packet):
        print(f"Packet received: {packet.name}")


    def send(self, packet):
        print(f"Sending packet with name: {packet.name}")

    def connect(self, node):
        print("Connecting packet to another node")

    def isMouseOver(self):
        # Проверка, находится ли мышь над узлом
        return self.x - self.size // 2 < pygame.mouse.get_pos()[0] < self.x + self.size // 2 and \
            self.y - self.size // 2 < pygame.mouse.get_pos()[1] < self.y + self.size // 2