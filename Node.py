import pygame
import sys
import visualization



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

    # def update_position(self, event):
    #     if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
    #         mouse_x, mouse_y = event.pos
    #         self.prev_x = self.x
    #         self.prev_y = self.y
    #         self.x = mouse_x
    #         self.y = mouse_y
    def update_position(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.isMouseOver():
                self.dragging = True
                self.offset_x = self.x - event.pos[0]
                self.offset_y = self.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.x = event.pos[0] + self.offset_x
            self.y = event.pos[1] + self.offset_y

    def get_info(self):
        return f"Info: {self.info}"

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

    def draw(self, screen):
        screen.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))
        self.draw_name(screen)





