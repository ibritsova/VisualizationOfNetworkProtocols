import pygame
import sys

from visualization.EndPoint import EndPoint
from visualization.HUB import HUB
from visualization.Packet import Packet
from visualization.InputBox import InputBox


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


def draw_nodes(hubs, buttons):
    pygame.init()

    screen = pygame.display.set_mode((1000, 900))
    pygame.display.set_caption("Nodes on Pygame")

    clock = pygame.time.Clock()
    inputBox1 = InputBox(0, 100, 100, 100)
    inputBox1.draw(screen)

    x = 80
    y = 150

    first = True
    inputBox = None

    while True:
        for event in pygame.event.get():
            # responsible for dragging elements
            for hub in hubs:
                hub.update_position(event)
                for endPoint in hub.endPoints:
                    endPoint.update_position(event)

            if inputBox is not None:
                inputBox.handle_event(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.node_type == "Delete":
                            hubs = []
                            x = 80
                            y = 150
                    if button.isMouseOver():
                        if button.node_type == "HUB":
                            x += 100
                            newHub = HUB(x, y, "HUB", "Pridame neskor")
                            hubs.append(newHub)
                            if(len(hubs) > 0):
                                hubs[-1].addSubHub(newHub)





                        elif button.node_type == "Packet":
                            x += 100
                            # TODO: fix inputBox
                            # if inputBox is None:
                            #     inputBox = InputBox(100, 700, 200, 30)
                            #
                            # inputBox.active = True
                            # if (inputBox == None):
                            #     inputBox = InputBox(event.pos[0], event.pos[1], 200, 30)

                            packet = Packet(x, y, "Packet", "Pridame neskor")
                            packet.draw(screen)


                        elif button.node_type == "EndPoint":
                            y += 100
                            hub = hubs[-1]
                            hub.addEndPoint(EndPoint(x,y, "EndPoint", "Pridame neskor"))

                        elif button.node_type == "Quit":
                            pygame.quit()
                            sys.exit()

        screen.fill((255, 255, 255))

        for hub in hubs:
            if hub.isMouseOver():
                font = pygame.font.Font(None, 24)
                text = font.render(hub.get_info(), True, (0, 0, 0), hub.text_bg_color)
                screen.blit(text, (hub.x - hub.size // 2, hub.y - hub.size // 2 - 20))

        for i in range(len(hubs)):
            hubs[i].draw(screen)
            hubs[i].connectToEndPoints(screen)
            if(i > 0):
                hubs[i].connect(screen, hubs[i - 1])


        for button in buttons:
            button.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    hubs = []
    buttons = [
        Button(200, 50, 100, 50, (0, 0, 0), "HUB", "HUB"),
        Button(350, 50, 100, 50, (0, 0, 0), "Packet", "Packet"),
        Button(500, 50, 150, 50, (0, 0, 0), "EndPoint", "EndPoint"),
        Button(700, 50, 200, 50, (0, 0, 0), "Delete all", "Delete"),
        Button(900, 300, 100, 50, (0, 0, 0), "Quit", "Quit")
    ]
    draw_nodes(hubs, buttons)
