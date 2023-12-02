import pygame
from Visuals.colors import Colors

pygame.init()

# Klasse fuer einen Knopf, der im Menu verwendet wird. Hat vorerst leider kein Hovern mehr drin, vielleicht spater nochmal hinzufuegen
class Button:
    def __init__(self, x, y, width, height, text, font_size=20, color=Colors.WHITE, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, Colors.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
