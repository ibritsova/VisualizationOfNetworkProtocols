import pygame
from visualization.Node import Node


class HUB(Node):


    def __init__(self, x, y, name, info = "", previousNode = None):
        super().__init__(x, y, name, 40, (0, 255, 0), info)
        self.text_bg_color = (200, 200, 200)
        self.img = pygame.image.load("hub.png")
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