import pygame

# Hilfsklasse, um dem Spieler-Auto die richtigen Bilder zum richtigen Zeitpunkt zuzuweisen
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("assets/player_straight.png").convert_alpha()

        self.straight = pygame.image.load("assets/player_straight.png")
        self.right = pygame.image.load("assets/player_right.png")
        self.left = pygame.image.load("assets/player_left.png")

        self.rect = self.image.get_rect()
        self.rect.center = (x - self.rect.width, y - self.rect.height)


    def drive_straight(self):
        self.image = self.straight
        self.scale()

    def drive_right(self):
        self.image = self.right
        self.scale()

    def drive_left(self):
        self.image = self.left
        self.scale()

    def scale(self):
        self.image = pygame.transform.scale_by(self.image, 4)