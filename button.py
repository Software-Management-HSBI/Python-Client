import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Super toller Racer")
font = pygame.font.Font(None, 18)

background_image = pygame.image.load("assets/BetterCallSus.jpg")

class Button:
    def __init__(self, x, y, width, height, text, font_size=20, inactive_color=GRAY, active_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.current_color = inactive_color
        self.is_hovered = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                # Hier kannst du deine Aktion für den Button-Klick einfügen
                print("Button wurde geklickt!")

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.active_color
            self.is_hovered = True
        else:
            self.current_color = self.inactive_color
            self.is_hovered = False