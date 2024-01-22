import pygame
import sys
from EndPoint import EndPoint
from HUB import HUB
from InputBox import InputBox
from Packet import Packet
class Button:
    def __init__(self, x, y, width, height, color, text, node_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.outLineColor = color
        self.node_type = node_type

    def draw(self, screen):
        pygame.draw.rect(screen, self.outLineColor, self.rect, 2)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def isMouseOver(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_hub_in_area(self, hub):
        # Check if the hub's coordinates are within the bounding box of the start area
        return self.rect.collidepoint(hub.x, hub.y)


class Drawer:

    def __init__(self, buttons=[], hubs=[], listOfPackets=[]):
        self.hubs = hubs
        self.listOfPackets = listOfPackets
        self.buttons = buttons

    def draw_nodes(self):
        pygame.init()

        screen = pygame.display.set_mode((1000, 900))
        pygame.display.set_caption("Nodes on Pygame")

        clock = pygame.time.Clock()
        inputBox1 = InputBox(0, 100, 100, 100)
        inputBox1.draw(screen)

        x = 170
        y = 190

        inputBox = None

        continueProcess = True

        while True:
            for event in pygame.event.get():
                # responsible for dragging elements
                for hub in self.hubs:
                    hub.update_position(event)
                    for endPoint in hub.endPoints:
                        endPoint.update_position(event)
                for packet in self.listOfPackets:
                    packet.update_position(event)

                if inputBox is not None:
                    inputBox.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.node_type == "Delete":
                                self.hubs = []
                                self.listOfPackets = []
                                continueProcess = True
                        if button.isMouseOver():
                            if button.node_type == "HUB" and continueProcess:
                                newHub = HUB(x, y, f"HUB{len(self.hubs)}", "Pridame neskor", len(self.hubs), self)
                                if (len(self.hubs) > 0):
                                    self.hubs[-1].addSubHub(newHub)
                                self.hubs.append(newHub)
                            elif button.node_type == "Packet" and continueProcess:
                                # TODO: fix inputBox
                                # if inputBox is None:
                                #     inputBox = InputBox(100, 700, 200, 30)
                                #
                                # inputBox.active = True
                                # if (inputBox == None):
                                #     inputBox = InputBox(event.pos[0], event.pos[1], 200, 30)
                                packet = Packet(self.hubs[0].x, self.hubs[0].y, "Packet", "Pridame neskor")
                                self.listOfPackets.append(packet)
                                self.hubs[0].recieve(packet)


                            elif button.node_type == "EndPoint" and continueProcess:
                                hub = self.hubs[-1]
                                hub.addEndPoint(EndPoint(x, y, "EndPoint", "Pridame neskor"))

                            elif button.node_type == "Quit":
                                pygame.quit()
                                sys.exit()

            screen.fill((255, 255, 255))

            for hub in self.hubs:
                for endPoint in hub.endPoints:
                    if endPoint.isMouseOver() and continueProcess:
                        font = pygame.font.Font(None, 24)
                        text = font.render(endPoint.get_info(), True, (0, 0, 0), endPoint.text_bg_color)
                        screen.blit(text, (endPoint.x - endPoint.size // 2, endPoint.y - endPoint.size // 2 - 20))
                if hub.isMouseOver() and continueProcess:
                    font = pygame.font.Font(None, 24)
                    text = font.render(hub.get_info(), True, (0, 0, 0), hub.text_bg_color)
                    screen.blit(text, (hub.x - hub.size // 2, hub.y - hub.size // 2 - 20))

            for i in range(len(self.hubs)):
                self.hubs[i].draw(screen)
                self.hubs[i].connectToEndPoints(screen)
                if (i > 0):
                    self.hubs[i].connect(screen, self.hubs[i - 1])
                self.hubs[i].updateSending()

            for packet in self.listOfPackets:
                packet.draw(screen)

            # if continueProcess and len(hubs) > 2:
            #     hubs[-1].draw(screen)
            #     hubs[-1].connect(screen, hubs[-2])
            #     hubs[-1].connectToEndPoints(screen)
            # elif not continueProcess and len(hubs) > 0:
            #     hubs[-1].draw(screen)

            for button in self.buttons:
                if button.node_type == "Start":
                    for hub in self.hubs:
                        if button.is_hub_in_area(hub):
                            continueProcess = False
                        else:
                            continueProcess = True
                button.draw(screen)

            pygame.display.flip()


if __name__ == "__main__":
    buttons = [
        Button(200, 50, 100, 50, (0, 0, 0), "HUB", "HUB"),
        Button(350, 50, 100, 50, (0, 0, 0), "Packet", "Packet"),
        Button(500, 50, 150, 50, (0, 0, 0), "EndPoint", "EndPoint"),
        Button(700, 50, 200, 50, (0, 0, 0), "Delete all", "Delete"),
        Button(900, 300, 100, 50, (0, 0, 0), "Quit", "Quit"),
        Button(80, 150, 200, 80, (255, 0, 0), "Start Position", "Start")
    ]
    drawer = Drawer(buttons)
    drawer.draw_nodes()
