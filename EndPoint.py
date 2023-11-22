import pygame
import visualization
from visualization.Node import Node


class EndPoint(Node):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, 40, (0, 0, 255))

    def receive(self, packet):
        print(f"{self.name} received a packet")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.size // 2, self.y - self.size // 2, self.size, self.size))
        self.draw_name(screen)

    def send(self, packet):
        print(f"Sending packet from {self.name}")

    def connect(self, node):
        print(f"Connecting {self.name} to another node")
