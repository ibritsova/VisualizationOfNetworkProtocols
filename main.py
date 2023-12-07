
import pygame
import sys

from visualization.EndPoint import EndPoint
from visualization.HUB import HUB
from visualization.Packet import Packet

class Button:
    def __init__(self, x, y, width, height, color, text, node_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.node_type = node_type

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - text.get_height() // 2))

    def isMouseOver(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

def draw_nodes(nodes, buttons):
    pygame.init()

    screen = pygame.display.set_mode((1000, 900))
    pygame.display.set_caption("Nodes on Pygame")

    clock = pygame.time.Clock()


    x = 80
    y = 150
    previous = None
    first = True

    while True:
        for event in pygame.event.get():
            for node in nodes:
                node.update_position(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.node_type == "Delete":
                            nodes = []
                            previous = None
                            current = None
                            x = 80
                            y = 150
                    if button.isMouseOver():
                        if button.node_type == "HUB":
                           x += 100
                           if first:
                               first = False
                               previous = HUB(x, y, "HUB", "Pridame neskor")
                               nodes.append(previous)
                           else:
                               current = HUB(x, y, "HUB", "Pridame neskor", previous)
                               nodes.append(current)
                               previous = current



                        elif button.node_type == "Packet":
                            x += 100
                            nodes.append(Packet(x, y, "Packet", "Pridame neskor"))


                        elif button.node_type == "EndPoint":
                            y += 100

                            if first:
                                first = False
                                previous = EndPoint(x, y, "EndPoint", "Pridame neskor")
                                nodes.append(previous)
                            else:
                                current = EndPoint(x, y, "EndPoint", "Pridame neskor", previous)
                                nodes.append(current)
                                # previous = current





        screen.fill((255, 255, 255))

        for node in nodes:
            if node.isMouseOver():
                font = pygame.font.Font(None, 24)
                text = font.render(node.get_info(), True, (0, 0, 0), node.text_bg_color)
                screen.blit(text, (node.x - node.size // 2, node.y - node.size // 2 - 20))

        for node in nodes:
            if isinstance(node, HUB) or isinstance(node, EndPoint):
                node.draw(screen)
                if node.previousNode is not None:
                    node.connect(screen)
            else:
                node.draw(screen)




        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    nodes = []
    buttons = [
        Button(200, 50, 100, 50, (0, 0, 0), "HUB", "HUB"),
        Button(350, 50, 100, 50, (0, 0, 0), "Packet", "Packet"),
        Button(500, 50, 150, 50, (0, 0, 0), "EndPoint", "EndPoint"),
        Button(700, 50, 200, 50, (0, 0, 0), "Delete all", "Delete")
    ]
    draw_nodes(nodes, buttons)
