import pygame
class Button:
    def __init__(self, x, y, width, height, image, text, node_type, imageHover=None):
        self.text = text
        self.node_type = node_type
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.text_color = (255,255,255)

        if self.node_type == "Start":
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))

        self.imageHover = pygame.image.load(imageHover)
        self.imageHover = pygame.transform.scale(self.imageHover, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.isHovered = False

    def drawButton(self, screen):

        if self.node_type != "Start":

            self.isMouseOver()
            current_image = self.imageHover if self.isHovered else self.image
            screen.blit(current_image, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)


        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def isMouseOver(self):
        self.isHovered = self.rect.collidepoint(pygame.mouse.get_pos())
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.isHovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def is_hub_in_area(self, hub):
        return self.rect.collidepoint(hub.x, hub.y)

    # Method to set transparency
    def set_transparency(self, transparency):
        self.transparency = transparency