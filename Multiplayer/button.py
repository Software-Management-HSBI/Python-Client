import pygame
from Visuals.colors import Colors

pygame.init()

# Klasse fuer einen Knopf, der im Menu verwendet wird. Hat vorerst leider kein Hovern mehr drin, vielleicht spater nochmal hinzufuegen
class Button:
    def __init__(self, x, y, width, height, text, font_size=20, color=Colors.WHITE, hover_color=Colors.LIGHT_GRAY,
                 action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, self.font_size)
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        # Check if the mouse is over the button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_x, mouse_y)

        # Change color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color

        # Draw the button
        pygame.draw.rect(screen, current_color, self.rect)

        # Render and draw the text
        text_surface = self.font.render(self.text, True, Colors.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
