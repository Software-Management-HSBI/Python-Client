import math
import random

import globals as gl
import pygame

from Visuals.player import Player
from Visuals.background import Background
from Gamefiles.util import Util
from Visuals.sprites import Sprite


class Sprites:

    @staticmethod
    def create_background():
        """Erstellt mit einer Hilfsklasse die einzelnen Hintergrundschichten"""
        surface_sky = Background(0, pygame.image.load("assets/sky.png"))
        surface_hills = Background(0, pygame.image.load("assets/hills.png"))
        surface_trees = Background(0, pygame.image.load("assets/trees.png"))

        gl.background_sprites.add(surface_sky)
        gl.background_sprites.add(surface_hills)
        gl.background_sprites.add(surface_trees)

    @staticmethod
    def create_player():
        """Platziert den Spieler in der Mitte der Strecke und ordnet ihm die Auto-Sprites zu"""
        gl.player = Player(gl.screen.get_width() / 2 - 30, gl.screen.get_height() - 100)
        gl.player_sprites.add(gl.player)

    @staticmethod
    def create_obstacles(segments):
        """Erstellt Trees und Billboards in zufaelligen Abstaenden"""
        for i in range(0, len(segments), random.choice([25, 35, 45, 55])):
            direction = random.choice([1, -1])
            Sprites.add_sprite(segments, i, Sprite.create_tree(), direction)
            Sprites.add_sprite(segments, i, Sprite.create_billboard(), -direction)

    @staticmethod
    def create_bots():
        """Erstellt die NPC-Autos und gibt ihnen zufaellige Position,
         zufaellige Sprites und zufaellige Geschwindigkeit"""
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
    def add_sprite(segments, n, sprite, offset):
        """Hilfsmethode, um Strassenhindernisse einfacher hinzuzufuegen"""
        segments[n]["sprites"].append({"source": sprite, "offset": offset})

    @staticmethod
    def create_server_cars():
        for player in gl.cars:
            segment = Util.which_segment(player.get("pos"))
            car = {"offset": player.get("offset"), "z": 5, "sprite": Sprite.get_car(),
                   "speed": 0, "percent": 0}
            if car not in segment.get("cars"):
                segment["cars"].append(car)
                gl.cars.append(car)
