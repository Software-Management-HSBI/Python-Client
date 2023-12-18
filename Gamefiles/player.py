import math
import random

import sys
import pygame
import globals as gl

from Gamefiles.util import Util
from Visuals.spriteCreation import Sprites

class Player:
    def __init__(self, sid = None, local = True):
        self.sid = sid
        self.local = local
        self.offset = 0
        self.z = 0
        self.x = (gl.screen.get_width()) / 2 - 30
        self.y = gl.screen.get_height() - 100


    def start(self):
        if self.local:
            Sprites.create_player()
        else:
            Sprites.create_remote_player()
            z = math.floor(random.random() * len(gl.segments) * gl.segmentLength)
            car = {"offset": self.offset, "z": z, "percent": 0, "sid": self.sid}
            segment = Util.which_segment(z)
            segment["players"].append(car)

    # Aqui é uma tentativa de atualizar o "Z" do jogador remoto para conseguirmos exibir ele com profundidade e escala corretos
    def update_car(self, z):
        self.z = z
        base = Util.which_segment(gl.position)
        for n in range(gl.drawDistance -1, 0, -1):
            segment = gl.segments[(base.get("index") + n) % len(gl.segments)]
            for i in range(len(segment.get("players"))):
                car = segment.get("players")[i]
                car["z"] = z
    
    def update(self):
        # Não executar o código caso não seja o jogador local
        if not self.local: 
            return

        self.x = gl.playerX

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gl.keyLeft = True
                if event.key == pygame.K_RIGHT:
                    gl.keyRight = True
                if event.key == pygame.K_UP:
                    gl.keyFaster = True
                if event.key == pygame.K_DOWN:
                    gl.keySlower = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    gl.keyLeft = False
                if event.key == pygame.K_RIGHT:
                    gl.keyRight = False
                if event.key == pygame.K_UP:
                    gl.keyFaster = False
                if event.key == pygame.K_DOWN:
                    gl.keySlower = False

