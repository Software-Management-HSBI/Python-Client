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
        gl.player_sprites2 = pygame.sprite.Group()
        gl.background_sprites = pygame.sprite.Group()
        gl.lap_start_time = time.time()
        Road.reset_road()
        self.game_loop()

    # Loop des Spiels: Erstellt Spieler und Hintergrund, nimmt Inputs entgegen und ruft permanent die render- und update-Methode auf
    def game_loop(self):
        Sprites.create_player()
        Sprites.create_player2()
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

                if event.type == pygame.K_s:
                    if event.key == pygame.K_LEFT:
                        gl.keyLeft2 = True
                    if event.key == pygame.K_d:
                        gl.keyRight2 = True
                    if event.key == pygame.K_UP:
                        gl.keyFaster2 = True
                    if event.key == pygame.K_DOWN:
                        gl.keySlower2 = True
                if event.type == pygame.K_w:
                    if event.key == pygame.K_a:
                        gl.keyLeft2 = False
                    if event.key == pygame.K_RIGHT:
                        gl.keyRight2 = False
                    if event.key == pygame.K_UP:
                        gl.keyFaster2 = False
                    if event.key == pygame.K_DOWN:
                        gl.keySlower2 = False

            self.update(gl.STEP)

            pygame.draw.rect(gl.screen, (255, 0, 0), gl.player1_rect)
            pygame.draw.rect(gl.screen, (0, 0, 255), gl.player2_rect)

            Render.render()

            pygame.display.flip()

            gl.clock.tick(gl.FPS)


    # Hier wird anhand der Nutzereingaben die Steuerung des Autos geaendert
    def update(self, dt):
        start_position = gl.position

        gl.position = Util.increase(gl.position, dt * gl.speed, gl.trackLength)
        gl.position2 = Util.increase(gl.position2, dt * gl.speed, gl.trackLength)
        current_segment = Util.which_segment(gl.position + gl.playerZ)
        current_segment2 = Util.which_segment(gl.position2 + gl.playerZ)

        tilt = dt * 2 * (gl.speed / gl.maxSpeed)
        tilt2 = dt * 2 * (gl.speed2 / gl.maxSpeed)

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

        if gl.keyLeft2:
            gl.playerX2 = gl.playerX2 - tilt2
            if gl.speed2 > 0:
                gl.player2.drive_left()
        elif gl.keyRight2:
            gl.playerX2 = gl.playerX2 + tilt
            if gl.speed2 > 0:
                gl.player2.drive_right()
        else:
            gl.player2.drive_straight()

        gl.playerX2 -= tilt2 * (gl.speed2 / gl.maxSpeed) * current_segment.get("curve") * gl.centrifugal

        if gl.keyFaster2:
            print("klappt")
            gl.speed2 = Util.accelerate(gl.speed2, gl.accel, gl.DT)
        elif gl.keySlower2:
            gl.speed2 = Util.accelerate(gl.speed2, gl.breaking, gl.DT)
        else:
            gl.speed2 = Util.accelerate(gl.speed2, gl.decel, gl.DT)

        if (gl.playerX2 < -1 or gl.playerX2 > 1) and (gl.speed2 > gl.offRoadLimit):
            gl.speed2 = Util.accelerate(gl.speed2, gl.offRoadDecel, gl.DT)

        gl.playerX = Util.limit(gl.playerX, -2, 2)
        gl.speed = Util.limit(gl.speed, 0, gl.maxSpeed)

        gl.playerX2 = Util.limit(gl.playerX2, -2, 2)
        gl.speed2 = Util.limit(gl.speed2, 0, gl.maxSpeed)

        # Fast alles bezueglich Zeit wurde jetzt nach Util verlagert
        Util.check_time(start_position)

        Util.update_time(gl.current_lap_time, gl.last_lap_time, gl.best_lap_time)
