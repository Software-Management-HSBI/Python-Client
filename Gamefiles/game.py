import pygame
import sys
import time

from Gamefiles.util import Util
from Visuals.render import Render
from Visuals.road import Road
from Visuals.spriteCreation import Sprites
from Gamefiles.carAI import AI

import globals as gl


# Der Teil des Singleplayers, der alle anderen aktiviert:
# Hier werden Tasteneingaben und Kollisionen des Autos
# mit anderen Objekten ueberprueft sowie die gefahrene Zeit geupdated
class Game:

    def __init__(self):
        """Erstellt den Bildschirm, startet das Generieren der Strasse, und beginnt das Spiel"""
        gl.screen = pygame.display.set_mode((gl.width, gl.height))
        pygame.display.set_caption("Racing")
        gl.player_sprites = pygame.sprite.Group()
        gl.background_sprites = pygame.sprite.Group()
        gl.lap_start_time = time.time()
        Road.reset_road()
        #if not gl.singleplayer:
            #gl.client.start_game()
        self.game_loop()

    def game_loop(self):
        """Loop des Spiels: Erstellt Spieler und Hintergrund, nimmt Inputs entgegen und ruft permanent die render- und
        update-Methode auf"""
        Sprites.create_player()
        Sprites.create_background()
        Sprites.create_bots()
        gl.background_sprites.draw(gl.screen)
        # Sprites.create_server_cars()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if gl.client.sio.connected:
                        gl.client.disconnect()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        gl.keyLeft = True
                    if event.key == pygame.K_RIGHT:
                        gl.keyRight = True
                    if event.key == pygame.K_UP:
                        gl.keyFaster = True
                        gl.start_time = True
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

            Render.render()
            self.update(gl.STEP)
            pygame.display.flip()
            gl.clock.tick(gl.FPS)

    @staticmethod
    def update(dt):
        """Hier wird anhand der Nutzereingaben die Steuerung des Autos geaendert; Zeit- und NPC-Aktualisierung
        geschieht hier ebenfalls"""
        start_position = gl.position  # Position zum Start der Methode, nicht generelle 1. Position
        current_segment = Util.which_segment(gl.position + gl.playerZ)
        tilt = dt * 2 * (gl.speed / gl.maxSpeed)
        gl.position = Util.increase(gl.position, dt * gl.speed, gl.trackLength)

        AI.update_cars(dt, current_segment, gl.playerw)  # Hier werden die NPCs bewegt

        if gl.keyLeft:
            gl.playerX = gl.playerX - tilt
        elif gl.keyRight:
            gl.playerX = gl.playerX + tilt

        gl.playerX -= tilt * (gl.speed / gl.maxSpeed) * current_segment.get("curve") * gl.centrifugal

        if gl.keyFaster:
            gl.speed = Util.accelerate(gl.speed, gl.accel, gl.DT)
        elif gl.keySlower:
            gl.speed = Util.accelerate(gl.speed, gl.breaking, gl.DT)
        else:
            gl.speed = Util.accelerate(gl.speed, gl.decel, gl.DT)

        if gl.playerX < -1 or gl.playerX > 1:
            if gl.speed > gl.offRoadLimit:
                gl.speed = Util.accelerate(gl.speed, gl.offRoadDecel, gl.DT)

            Util.obstacle_collision(current_segment)  # Kollision mit Hindernissen

        Util.car_collision(current_segment)  # Kollision mit Autos

        gl.playerX = Util.limit(gl.playerX, -2, 2)
        gl.speed = Util.limit(gl.speed, 0, gl.maxSpeed)

        # Sendet Spieler-Daten an den Server, falls Multiplayer aktiv
        if gl.singleplayer is False:
            gl.client.ingame_pos(1, gl.playerZ + gl.position, gl.playerX)

        Util.check_time(start_position)  # Ueberprueft und Updatet die Zeit ueber Util
        Util.update_time(gl.current_lap_time, gl.last_lap_time, gl.best_lap_time)
