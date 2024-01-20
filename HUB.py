import pygame
from visualization.Node import Node
from visualization.EndPoint import EndPoint


class HUB(Node):
    endPoints = []
    subHubs = []
    packetsOnTheWay = []
    recievedPackets = []

    def __init__(self, x, y, name, info = ""):
        super().__init__(x, y, name, 40, (0, 255, 0), info)
        self.text_bg_color = (200, 200, 200)
        self.img = pygame.image.load("hub.png")
        new_size = (50, 50)
        self.endPoints = []
        self.subHubs = []
        self.img = pygame.transform.scale(self.img, new_size)

    def addEndPoint(self, node):
        self.endPoints.append(node)


    def addSubHub(self, hub):
        self.subHubs.append(hub)

    def receive(self, packet):
        self.recievedPackets.append(packet)
        self.send(packet)
        print(f"{self.name} received a packet")

    def send(self, packet):
        for endPoint in self.endPoints:
            self.packetsOnTheWay.append((packet, endPoint))
        for subHub in self.subHubs:
            self.packetsOnTheWay.append((packet, subHub))
        print(f"Sending packet from {self.name}")

    def updateSending(self):
        for tuple in self.packetsOnTheWay:
            if tuple[0].x == tuple[1].x and tuple[0].y == tuple[1].y:
                if type(tuple[1]) == HUB:
                    tuple[1].recieve(tuple[0])
            else:
                self.move(tuple[0], tuple[1])

    def move(self, packet, node):
         # TODO: implements

    def connect(self, screen, nodeToConnect):
        line_color = (255, 0, 0)
        pygame.draw.line(screen, line_color, (self.x, self.y), (nodeToConnect.x, nodeToConnect.y), 2)

    def connectToEndPoints(self, screen):
        line_color = (255, 0, 0)
        for endPoint in self.endPoints:
            endPoint.draw(screen)
            pygame.draw.line(screen, line_color, (self.x, self.y), (endPoint.x, endPoint.y), 2)

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