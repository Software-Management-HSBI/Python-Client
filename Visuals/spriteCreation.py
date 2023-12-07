import globals as gl
import pygame

from Visuals.player import Player
from Visuals.background import Background

class Sprites:
     # Erstellt mit einer Hilfsklasse die einzelnen Hintergrundschichten
    @staticmethod
    def create_background():
        surface_sky = Background(0, pygame.image.load("assets/sky.png"))
        surface_hills = Background(0, pygame.image.load("assets/hills.png"))
        surface_trees = Background(0, pygame.image.load("assets/trees.png"))

        gl.background_sprites.add(surface_sky)
        gl.background_sprites.add(surface_hills)
        gl.background_sprites.add(surface_trees)

    # Platziert den Spieler in der Mitte der Strecke und ordnet ihm die Auto-Sprites zu
    @staticmethod
    def create_player():
        gl.player = Player(gl.screen.get_width() / 2 - 30, gl.screen.get_height() - 100)
        gl.player_sprites.add(gl.player)