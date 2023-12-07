import pygame
import math
import sys
import time

from Gamefiles.util import Util
from Visuals.player import Player
from Visuals.background import Background
from Visuals.colors import Colors
from Visuals.render import Render
from Visuals.roadCreation import Road

import globals as gl

# Der Teil des Singleplayers, der alle anderen aktiviert: Hier werden Tasteneingaben überprüft und die Straße unendlich erweitert
class Game:

    pygame.init()
    # Sowohl in Python als auch in JavaScript sorgt das Veraedern der FPS fuer Probleme beim Spielverhalten

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
        self.create_player()
        self.create_background()
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

        # Das alles hier ist die Lap-Berechnung, ich hab versucht, alles in eine andere Methode zu verschieben,
        # allerdings wird dann keine neue Runde registriert. Daher muss die Ueberpruefung erstmal hier bleiben.

        # Ueberprueft, ob Runde gefahren wurde
        if gl.position > gl.playerZ:
            if gl.current_lap_time and (start_position < gl.playerZ):
                gl.last_lap_time = gl.current_lap_time
                gl.current_lap_time = 0

                gl.lap_start_time = time.time()
                # Checkt nach Bestzeit
                if gl.last_lap_time < gl.best_lap_time:
                    gl.best_lap_time = gl.last_lap_time
            else:
                # Laesst die Zeit weiterlaufen.
                current_time = time.time()
                gl.current_lap_time = current_time - gl.lap_start_time

        self.update_time(gl.current_lap_time, gl.last_lap_time, gl.best_lap_time)

    # Zeigt aktuelle, letzte und beste Zeit an
    def update_time(self, current_lap_time, last_lap_time, best_lap_time):
        best_time_text = gl.font.render(f"Noch keine Runde gefahren", True, Colors.RED)
        timer_text = gl.font.render(f"Aktuelle Runde: {int(current_lap_time)} Sekunden", True, Colors.BLACK)
        last_time_text = gl.font.render(f"Letzte Runde: {int(last_lap_time)} Sekunden", True, Colors.BLUE)
        if not math.isinf(gl.best_lap_time):
            best_time_text = gl.font.render(f"Beste Runde: {int(best_lap_time)} Sekunden", True, Colors.RED)
        gl.screen.blit(timer_text, (10, 10))
        gl.screen.blit(last_time_text, (10, 50))
        gl.screen.blit(best_time_text, (10, 90))
        
    # Liest das Strassen-Array aus und markiert Start-/Ziellinie


    # Erstellt mit einer Hilfsklasse die einzelnen Hintergrundschichten
    def create_background(self):
        surface_sky = Background(0, pygame.image.load("assets/sky.png"))
        surface_hills = Background(0, pygame.image.load("assets/hills.png"))
        surface_trees = Background(0, pygame.image.load("assets/trees.png"))

        gl.background_sprites.add(surface_sky)
        gl.background_sprites.add(surface_hills)
        gl.background_sprites.add(surface_trees)

    # Platziert den Spieler in der Mitte der Strecke und ordnet ihm die Auto-Sprites zu
    def create_player(self):
        gl.player = Player(gl.screen.get_width() / 2 - 30, gl.screen.get_height() - 100)
        gl.player_sprites.add(gl.player)
