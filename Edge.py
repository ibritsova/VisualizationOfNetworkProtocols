import pygame


class Edge():
    def __init__(self, A, B, screen):
        line_color = (255, 0, 0)
        pygame.draw.line(screen, line_color, (A.x, A.y), (B.x, B.y), 2)
