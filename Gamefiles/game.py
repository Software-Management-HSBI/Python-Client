import pygame
import sys
import time

from Gamefiles.util import Util
from Visuals.render import Render
from Visuals.road import Road
from Visuals.spriteCreation import Sprites

import globals as gl

# Der Teil des Singleplayers, der alle anderen aktiviert: Hier werden Tasteneingaben überprüft und die Straße unendlich erweitert
class Game:

    # Erstellt den Bildschirm, startet das Generieren der Strasse, und beginnt das Spiel
    def __init__(self):
        gl.screen = pygame.display.set_mode((gl.width, gl.height))
        pygame.display.set_caption("Singleplayer")
        gl.player_sprites = pygame.sprite.Group()
        gl.background_sprites = pygame.sprite.Group()
        gl.lap_start_time = time.time()
        Road.reset_road()
        self.game_loop()

    # Loop des Spiels: Erstellt Spieler und Hintergrund, nimmt Inputs entgegen und ruft permanent die render- und update-Methode auf
    def game_loop(self):
        Sprites.create_player()
        Sprites.create_background()
        gl.background_sprites.draw(gl.screen)

        while True:
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

            Render.render()
            self.update(gl.STEP)
            pygame.display.update()

    # Hier wird anhand der Nutzereingaben die Steuerung des Autos geaendert
    def update(self, dt):
        start_position = gl.position

        gl.position = Util.increase(gl.position, dt * gl.speed, gl.trackLength)
        current_segment = Util.which_segment(gl.position + gl.playerZ)

        tilt = dt * 2 * (gl.speed / gl.maxSpeed)

        if gl.keyLeft:
            gl.playerX = gl.playerX - tilt
            if gl.speed > 0:
                gl.player.drive_left()
        elif gl.keyRight:
            gl.playerX = gl.playerX + tilt
            if gl.speed > 0:
                gl.player.drive_right()
        else:
            gl.player.drive_straight()

        gl.playerX -= tilt * (gl.speed / gl.maxSpeed) * current_segment.get("curve") * gl.centrifugal

        if gl.keyFaster:
            gl.speed = Util.accelerate(gl.speed, gl.accel, gl.DT)
        elif gl.keySlower:
            gl.speed = Util.accelerate(gl.speed, gl.breaking, gl.DT)
        else:
            gl.speed = Util.accelerate(gl.speed, gl.decel, gl.DT)

        if (gl.playerX < -1 or gl.playerX > 1) and (gl.speed > gl.offRoadLimit):
            gl.speed = Util.accelerate(gl.speed, gl.offRoadDecel, gl.DT)

        gl.playerX = Util.limit(gl.playerX, -2, 2)
        gl.speed = Util.limit(gl.speed, 0, gl.maxSpeed)

        # Fast alles bezueglich Zeit wurde jetzt nach Util verlagert
        Util.check_time(start_position)

        Util.update_time(gl.current_lap_time, gl.last_lap_time, gl.best_lap_time)
