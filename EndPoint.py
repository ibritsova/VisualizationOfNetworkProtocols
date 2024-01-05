import pygame
import visualization
from visualization.Node import Node


class EndPoint(Node):
    def __init__(self, x, y, name, info = "", previousNode = None):
        super().__init__(x, y, name, 40, (0, 0, 255), info)
        self.text_bg_color = (200, 200, 200)
        self.img = pygame.image.load("endPoint.png")
        new_size = (50, 50)
        self.img = pygame.transform.scale(self.img, new_size)
        self.previousNode = previousNode

    def receive(self, packet):
        print(f"{self.name} received a packet")


    def send(self, packet):
        print(f"Sending packet from {self.name}")

    def connect(self, screen):
        line_color = (255, 0, 0)
        pygame.draw.line(screen, line_color, (self.x, self.y), (self.previousNode.x, self.previousNode.y), 2)
        # print(f"Coordinates: {(self.x, self.y)} -> {(self.previousNode.x, self.previousNode.y)}")

    def isMouseOver(self):
        # Проверка, находится ли мышь над узлом
        return self.x - self.size // 2 < pygame.mouse.get_pos()[0] < self.x + self.size // 2 and \
            self.y - self.size // 2 < pygame.mouse.get_pos()[1] < self.y + self.size // 2
