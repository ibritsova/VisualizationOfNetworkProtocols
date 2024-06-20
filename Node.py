
import pygame
import sys




class Node:
    def __init__(self, x, y, name, size, color, info):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.info = info
        self.name = name
        self.size = size
        self.color = color
        self.prev_node = None
        self.dragging = False
        self.acknowImg = self.nodeImg = pygame.image.load("acknowledgment.png")

    def update_position(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.isMouseOver():
                self.dragging = True
                self.offset_x = self.x - event.pos[0]
                self.offset_y = self.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif (event.type == pygame.MOUSEMOTION and self.dragging):
            self.x = event.pos[0] + self.offset_x
            self.y = event.pos[1] + self.offset_y

    def get_info(self):
        return f"{self.info}"

    def receiveAndSendFurther(self, packet):
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

    def draw(self, screen):
        screen.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))
        self.draw_name(screen)

    def drawAcknowledgment(self, screen):
        screen.blit(self.acknowImg, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))






