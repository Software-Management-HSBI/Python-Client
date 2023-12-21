import pygame
import sys
import time

from Gamefiles.util import Util
from Visuals.render import Render
from Visuals.road import Road
from Visuals.spriteCreation import Sprites
from Gamefiles.carAI import AI

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
            pygame.display.flip()

            gl.clock.tick(gl.FPS)

    # Hier wird anhand der Nutzereingaben die Steuerung des Autos geaendert
    def update(self, dt):
        sprite_scale = ((1 / 80) * 0.3)

        start_position = gl.position

        current_segment = Util.which_segment(gl.position + gl.playerZ)

        tilt = dt * 2 * (gl.speed / gl.maxSpeed)

        AI.update_cars(dt, current_segment, gl.playerw)

        gl.position = Util.increase(gl.position, dt * gl.speed, gl.trackLength)

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

        if gl.playerX < -1 or gl.playerX > 1:
            if gl.speed > gl.offRoadLimit:
                gl.speed = Util.accelerate(gl.speed, gl.offRoadDecel, gl.DT)

            # TODO: Klappt noch nicht so richtig, der findet wohl "width" nicht.
            for obstacle in current_segment.get("sprites"):
                obstacleW = 250 * sprite_scale # 250 ist jetzt hier, weil obstacle.get() irgendwie nicht klappen wollte
                if Util.overlap(gl.playerX, gl.playerw, obstacle.get("offset") + obstacleW/2 * (1 if obstacle.get("offset") > 0 else -1), obstacleW):
                    gl.speed = gl.maxSpeed / 5
                    gl.position = Util.increase(current_segment.get("p1").get("world").get("z"), -gl.playerZ, gl.trackLength)

        for car in current_segment.get("cars"):
            carW = car.get("z") * sprite_scale
            if gl.speed > car.get("speed"):
                if Util.overlap(gl.playerX, gl.playerw, car.get("offset"), carW, 0.8):
                    gl.speed = gl.maxSpeed / 5
                    gl.position = Util.increase(car.get("z"), -gl.playerZ, gl.trackLength)
                    # Irgendwas hier funktioniert noch nicht richtig
                    break

        gl.playerX = Util.limit(gl.playerX, -2, 2)
        gl.speed = Util.limit(gl.speed, 0, gl.maxSpeed)

        # Fast alles bezueglich Zeit wurde jetzt nach Util verlagert
        Util.check_time(start_position)

        Util.update_time(gl.current_lap_time, gl.last_lap_time, gl.best_lap_time)
