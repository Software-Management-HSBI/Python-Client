import math
import random

import globals as gl
import pygame

from Visuals.player import Player
from Visuals.background import Background
from Gamefiles.util import Util
from Visuals.sprites import Sprite


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

    @staticmethod
    def create_obstacles():
        for i in range(0, len(gl.segments), 100):
            Sprites.add_sprite(i, Sprite.create_tree(), -1)
            Sprites.add_sprite(i, Sprite.create_billboard(), -1)


    @staticmethod
    def create_bots():
        for n in range(gl.car_amount):
            offset = random.random() * Util.random_choice([-0.5, 0.5])
            z = math.floor(random.random() * len(gl.segments) * gl.segmentLength)
            sprite = Sprite.get_car()
            speed = gl.maxSpeed / 4 + random.random() * gl.maxSpeed / 2
            car = {"offset": offset, "z": z, "sprite": sprite, "speed": speed, "percent": 0}
            segment = Util.which_segment(z)
            segment["cars"].append(car)
            gl.cars.append(car)


    @staticmethod
    def add_sprite(n, sprite, offset):
        gl.segments[n]["sprites"].append({"source": sprite, "offset": offset})
