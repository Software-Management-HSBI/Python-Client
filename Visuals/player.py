import pygame


class Player(pygame.sprite.Sprite):
    """Hilfsklasse, um dem Spieler-Auto die richtigen Bilder zum richtigen Zeitpunkt zuzuweisen"""
    start_x = 0
    start_y = 0
    uphill_offset = 18

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("assets/player_straight.png").convert_alpha()

        self.straight = pygame.image.load("assets/player_straight.png")
        self.straight_uphill = pygame.image.load("assets/player_uphill_straight.png")

        self.right = pygame.image.load("assets/player_right.png")
        self.right_uphill = pygame.image.load("assets/player_uphill_right.png")

        self.left = pygame.image.load("assets/player_left.png")
        self.left_uphill = pygame.image.load("assets/player_uphill_left.png")

        self.rect = self.image.get_rect()
        self.start_x = x - self.rect.width - 47
        self.start_y = y - self.rect.height - 44
        self.rect.center = (x - self.rect.width, y - self.rect.height)

    def drive_straight(self, uphill):
        if uphill:
            self.image = self.straight_uphill
            self.rect.center = (self.start_x, self.start_y - self.uphill_offset)
        else:
            self.image = self.straight
            self.rect.center = (self.start_x, self.start_y)
        self.scale()

    def drive_right(self, uphill):
        if uphill:
            self.image = self.right_uphill
            self.rect.center = (self.start_x, self.start_y - self.uphill_offset)
        else:
            self.image = self.right
            self.rect.center = (self.start_x, self.start_y)
        self.scale()

    def drive_left(self, uphill):
        if uphill:
            self.image = self.left_uphill
            self.rect.center = (self.start_x, self.start_y - self.uphill_offset)
        else:
            self.image = self.left
            self.rect.center = (self.start_x, self.start_y)
        self.scale()

    def scale(self):
        self.image = pygame.transform.scale_by(self.image, 5)

    def bounce(self, bounce):
        self.rect.center = (self.rect.centerx, self.rect.centery - bounce)
