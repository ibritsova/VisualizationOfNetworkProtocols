import pygame
import sys
import visualization



class Node:
    def __init__(self, x, y, name, size, color):
        self.x = x
        self.y = y
        self.name = name
        self.size = size
        self.color = color
        self.prev_node = None

    def receive(self, packet):
        pass

    def draw(self, screen):
        pass

    def send(self, packet):
        pass

    def connect(self, node):
        pass

    def connect_with_previous(self, screen):
        if self.prev_node and type(self.prev_node) == type(self):
            pygame.draw.line(screen, (0, 0, 0), (self.prev_node.x, self.prev_node.y), (self.x, self.y), 2)

    def draw_name(self, screen):
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (self.x - 20, self.y - self.size - 10))





