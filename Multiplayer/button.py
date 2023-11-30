import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


# Klasse fuer einen Knopf, ueber den gehovert werden kann.
# TODO: Muss noch fuer das Nutzen im Menu angepasst werden
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
                return True

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.active_color
            self.is_hovered = True
        else:
            self.current_color = self.inactive_color
            self.is_hovered = False

# Testmethode, um zu gucken, ob der Button an sich funktioniert
def main():
    # Fensterkonfiguration
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Button mit Pygame")

    # Button erstellen
    button = Button(300, 250, 200, 50, "Klick mich!")

    # Haupt-Event-Schleife
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            button.handle_event(event)

        # Hintergrund zeichnen
        screen.fill(BLACK)

        # Button zeichnen
        button.draw(screen)

        # Bildschirm aktualisieren
        pygame.display.flip()

if __name__ == "__main__":
    main()