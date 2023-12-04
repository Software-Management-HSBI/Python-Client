import pygame

# Hilfsklasse zum Erstellen des Spiel-Hintergrunds
class Background(pygame.sprite.Sprite):
    def __init__(self, x, img):
        super().__init__()
        self.image = img.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.top = x
        self.image = pygame.transform.scale_by(self.image, 1.6)
