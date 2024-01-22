import pygame

from EndPoint import EndPoint
from Node import Node
from Packet import Packet

class HUB(Node):
    endPoints = []
    subHubs = []
    packetsOnTheWay = []
    recievedPackets = []

    def __init__(self, x, y, name, info = "", sysIndex = 0, drawer = None):
        super().__init__(x, y, name, 40, (0, 255, 0), info)
        self.text_bg_color = (200, 200, 200)
        self.img = pygame.image.load("hub.png")
        new_size = (50, 50)
        self.endPoints = []
        self.subHubs = []
        self.img = pygame.transform.scale(self.img, new_size)
        self.sysIndex = sysIndex
        self.drawer = drawer
        self.dragging = False
        self.recievedPackets = []

    def get_info(self):
        return f'Momentlne ma {len(self.recievedPackets)} neprecitanych sprav'

    def addEndPoint(self, node):
        self.endPoints.append(node)


    def addSubHub(self, hub):
        self.subHubs.append(hub)

    def recieve(self, packet):
        if(type(packet) != Packet):
            print(f"BLA")

        print(f"{self.name} {self.sysIndex} recieved a packet")
        self.recievedPackets.append(packet)
        self.send(packet)

    def send(self, packet):
        print(f"Sending packet from {self.name} {self.sysIndex}")
        for endPoint in self.endPoints:
            copyPacket = Packet(packet.x, packet.y,packet.name, packet.info)
            self.drawer.listOfPackets.append(copyPacket)
            self.packetsOnTheWay.append(copyPacket)
            self.packetsOnTheWay.append(endPoint)

        for subHub in self.subHubs:
            copyPacket = Packet(packet.x, packet.y,packet.name, packet.info)
            self.drawer.listOfPackets.append(copyPacket)
            self.packetsOnTheWay.append(copyPacket)
            self.packetsOnTheWay.append(subHub)
        self.drawer.listOfPackets.remove(packet)

    def updateSending(self):
        if(len(self.packetsOnTheWay) == 0): return
        for i in range(1,len(self.packetsOnTheWay),2):
            if i < len(self.packetsOnTheWay) :
                packet = self.packetsOnTheWay[i - 1]
                destination = self.packetsOnTheWay[i]
                if abs(packet.x - destination.x) < 0.5 and abs(packet.y - destination.y) < 0.5:
                    if type(destination) == HUB:
                        destination.recieve(packet)
                    elif type(destination) == EndPoint:
                        destination.recieve(packet)
                        self.drawer.listOfPackets.remove(packet)

                    self.packetsOnTheWay.remove(packet)
                    self.packetsOnTheWay.remove(destination)

                else:
                    self.move(packet, destination)

    def move(self, packet, node):
        if (type(packet) != Packet):
            print(f"BLA")
       # print(f"Moving packet")
        speed = 0.5
        direction = pygame.Vector2(node.x, node.y) - pygame.Vector2(packet.x, packet.y)
        velocity = direction.normalize() * speed
        packet.x += velocity.x
        packet.y += velocity.y
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