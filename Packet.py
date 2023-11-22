import pygame
from visualization.Node import Node


class Packet(Node):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, 40, (255, 0, 0))

    def receive(self, packet):
        print(f"Packet received: {packet.name}")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.size // 2, self.y - self.size // 2, self.size, self.size))
        self.draw_name(screen)

    def send(self, packet):
        print(f"Sending packet with name: {packet.name}")

    def connect(self, node):
        print("Connecting packet to another node")