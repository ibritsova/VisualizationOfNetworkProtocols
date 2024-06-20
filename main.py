import pygame
import sys
import time
from Levels.TransportLevel import TransportLevel
from Levels.PhysicalLevel import PhysicalLevel
from Levels.ApplicationLevel import ApplicationLevel

from EndPoint import EndPoint
from HUB import HUB
from InputBox import InputBox
from Node import Node
from Packet import Packet
from Button import Button

class Drawer:



    def __init__(self, buttons=[], hubs=[], packets=[], toDraw=[]):
        self.hubs = hubs
        self.listOfPackets = packets
        self.buttons = buttons
        self.InputBox = None
        self.activeNode = None
        self.destinationNode = None
        self.continueProcess = True
        self.mainButtonsBlocked = False
        self.level = TransportLevel()
        self.backgroundColor = (255,255,255)
        self.screen = None
        self.currentPacket = None
        self.buttonsBlocked = False
        self.previousButtonLevel = None

    def delete_everything(self):
        self.continueProcess = True
        self.hubs = []
        self.listOfPackets = []
        # self.buttons = buttons
        self.InputBox = None
        self.activeNode = None
        self.destinationNode = None
    def activate(self, newHub):
        if self.activeNode is not None:
            self.activeNode.name = "HUB " + str(self.hubs.index(self.activeNode))
            self.activeNode.img = self.level.nodeImg
            # self.activeNode.img = pygame.transform.scale(self.activeNode.img, (50, 50))
        newHub.name = "Active " + newHub.name
        newHub.img =self.level.activeNodeImg
        # newHub.img = pygame.transform.scale(newHub.img, (50, 50))
        self.activeNode = newHub

    def changeLevel(self, button):
        if self.previousButtonLevel is not None:
            self.previousButtonLevel.text_color = (255,255,255)
        button.text_color = (0,0,0)
        self.previousButtonLevel = button



    def draw_nodes(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 900))
        pygame.display.set_caption("Vizualization of network Protocols")

        clock = pygame.time.Clock()

        x = 170
        y = 190

        while True:

            for button in self.buttons:
                button.isMouseOver()
                button.drawButton(self.screen)
                pygame.display.flip()
            for event in pygame.event.get():
                # responsible for dragging elements
                for hub in self.hubs:
                    hub.update_position(event)
                    for endPoint in hub.endPoints:
                        endPoint.update_position(event)
                for packet in self.listOfPackets:
                    packet.update_position(event)

                if self.InputBox is not None:
                    self.InputBox.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    for button in self.buttons:

                        if button.rect.collidepoint(event.pos):
                            print(f'Button clicked: {button.text}')
                            if button.node_type == "Delete" and not self.buttonsBlocked:
                                self.delete_everything()
                        if button.isMouseOver():
                            if button.node_type == "HUB" and self.continueProcess:
                                if(not self.buttonsBlocked):
                                    newHub = HUB(x, y, f"HUB{len(self.hubs)}", self.level.nodeImg, "", len(self.hubs), self)
                                    if (len(self.hubs) > 0):
                                        self.activeNode.addSubHub(newHub)
                                        newHub.addSubHub(self.activeNode)
                                    self.hubs.append(newHub)

                                    self.activate(newHub)

                            elif button.node_type == "Packet" and self.continueProcess:

                                if (len(self.hubs) > 0 and not self.buttonsBlocked):
                                    packet = Packet(self.level.packetImage, self.activeNode.x, self.activeNode.y, "Packet", "")
                                    self.currentPacket = packet
                                    inputBox = packet.createInputBox()
                                    self.InputBox = inputBox
                                    self.buttons.append(Button(650, 760, 100, 50, "button.png", "Send", "Send", "buttonHover.png"))
                                    self.buttonsBlocked = True


                            elif button.node_type == "EndPoint" and self.continueProcess:
                                if(not self.buttonsBlocked):
                                    self.activeNode.addEndPoint(EndPoint(x, y, "EndPoint", self.level.endPointImg, ""))

                            elif button.node_type == "Quit":
                                pygame.quit()
                                sys.exit()

                            elif button.node_type == "Send":


                                inputBox.saveData()
                                check = self.level.sendData(self.activeNode, self.currentPacket)
                                for hub in self.hubs:
                                    if hub != self.activeNode:
                                        hub.img = self.level.nodeImg
                                    for endPoint in hub.endPoints:
                                        endPoint.setToDefaultColor()

                                if check == True:
                                    self.mainButtonsBlocked = False
                                    self.InputBox = None
                                    buttons.remove(button)
                                    self.buttonsBlocked = False
                                    for hub in self.hubs:
                                        if hub == self.activeNode:
                                            continue
                                        hub.setToDefaultColor()
                                        for endPoint in hub.endPoints:
                                            endPoint.setToDefaultColor()
                                else:
                                    self.InputBox.setErrorState()

                            elif button.node_type == "Physical Layer":
                                self.level = PhysicalLevel(self)
                                self.delete_everything()
                                self.backgroundColor = self.level.backColor
                                self.changeLevel(button)


                            elif button.node_type == "Application Layer":
                                self.level = ApplicationLevel()
                                self.delete_everything()
                                self.backgroundColor = self.level.backColor
                                self.changeLevel(button)
                            elif button.node_type == "Transport Layer":
                                self.level = TransportLevel()
                                self.delete_everything()
                                self.backgroundColor = self.level.backColor
                                self.changeLevel(button)
            self.screen.fill(self.backgroundColor)



            for hub in self.hubs:
                for endPoint in hub.endPoints:
                    if endPoint.isMouseOver() and self.continueProcess:
                        font = pygame.font.Font(None, 24)
                        macText = font.render("MAC:" + endPoint.MACadress, True, (0, 0, 0), endPoint.text_bg_color)
                        self.screen.blit(macText, (endPoint.x + endPoint.size // 2 + 10, endPoint.y - endPoint.size // 2))

                        ipText = font.render("IP:" + endPoint.ip_address, True, (0, 0, 0), endPoint.text_bg_color)
                        self.screen.blit(ipText, (endPoint.x + endPoint.size // 2 + 10, endPoint.y - endPoint.size // 2 + 20))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 3 and self.buttonsBlocked and not self.currentPacket.isDestinationIPSet():
                                self.currentPacket.destinationIP = endPoint.ip_address
                                endPoint.setToChosenColor()

                if hub.isMouseOver():
                    shift = 20
                    font = pygame.font.Font(None, 24)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.continueProcess:
                                for i in range(len(hub.recievedPackets)):
                                    messageText = font.render(f"{i + 1}." + hub.recievedPackets[i].getData(), True, (0, 0, 0), hub.text_bg_color)
                                    self.screen.blit(messageText, (hub.x + hub.size // 2 + 10, (hub.y - hub.size // 2 - 20) + shift * i))
                            elif hub != self.activeNode:
                                self.destinationNode = hub
                                print(self.destinationNode.name)
                        elif event.button == 3 and self.continueProcess:
                            if not self.buttonsBlocked:
                                self.activate(hub)
                            else:
                                if not self.currentPacket.isDestinationIPSet() and not hub == self.activeNode:
                                    self.currentPacket.destinationIP = hub.ip_address
                                    print("Address: " + self.currentPacket.destinationIP)
                                    # hub.setToChosenColor()
                                    hub.img = self.level.activeNodeImg




                    else:
                        macText = font.render("MAC:" + hub.MACadress, True, (0, 0, 0), hub.text_bg_color)
                        self.screen.blit(macText, (hub.x + hub.size // 2 + 10, hub.y - hub.size // 2))

                        ipText = font.render("IP:" + hub.ip_address, True, (0, 0, 0), hub.text_bg_color)
                        self.screen.blit(ipText, (hub.x + hub.size // 2 + 10, hub.y - hub.size // 2 + 20))

            # for hub in self.hubs:
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         if event.button == 3 and self.continueProcess:
            #             if not self.buttonsBlocked:
            #                 self.activate(hub)
            #             elif not self.currentPacket.isDestinationIPSet() and not hub == self.activeNode:
            #                 self.currentPacket.destinationIP = hub.ip_address
            #                 print("Address: " + self.currentPacket.destinationIP)
            #                 hub.setToChosenColor()





            for i in range(len(self.hubs)):
                self.hubs[i].draw(self.screen)
                self.hubs[i].connectToEndPoints(self.screen)
                for subHub in self.hubs[i].subHubs:
                    self.hubs[i].connect(self.screen, subHub)
                self.hubs[i].updateSending()

            for packet in self.listOfPackets:
                packet.draw(self.screen)




            for button in self.buttons:
                if button.node_type == "Start":
                    for hub in self.hubs:
                        if button.is_hub_in_area(hub) or self.mainButtonsBlocked:
                            self.continueProcess = False
                        else:
                            self.continueProcess = True
                # Draw green frame for the "Start" button
                if button.node_type == "Start":
                    pygame.draw.rect(self.screen, (0, 255, 0), button.rect, 2)
                button.drawButton(self.screen)
                if self.InputBox is not None:
                    self.InputBox.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    buttons = [
        Button(200, 50, 150, 100, "button.png", "Node", "HUB", "buttonHover.png"),
        Button(350, 50, 150, 100, "button.png", "Data", "Packet", "buttonHover.png"),
        Button(500, 50, 200, 100, "button.png", "EndPoint", "EndPoint", "buttonHover.png"),
        Button(700, 50, 250, 100, "button.png", "Delete all", "Delete", "buttonHover.png"),
        Button(880, 300, 150, 100, "button.png", "Quit", "Quit", "buttonHover.png"),
        Button(80, 150, 250, 100, "button.png", "", "Start", "buttonHover.png"),
        Button(780, 400, 250, 100, "button.png", "Physical Layer", "Physical Layer", "buttonHover.png"),
        Button(780, 500, 250, 100, "button.png", "Transport Layer", "Transport Layer", "buttonHover.png"),
        Button(780, 590, 270, 100, "button.png", "Application Layer", "Application Layer", "buttonHover.png")
    ]

    drawer = Drawer(buttons)
    drawer.draw_nodes()
