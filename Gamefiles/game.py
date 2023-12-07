import pygame
import math
import sys
import time

from Gamefiles.util import Util
from Visuals.player import Player
from Visuals.background import Background
from Visuals.road import Road
from Visuals.colors import Colors
from Visuals.render import Render

import globals as gl

# Hiermit bildet man die Strasse. Es wird wahrscheinlich wichtig sein, dass dieses Array genauso auch beim Java-Client aufgebaut ist.
# 1. Variable ist Strassenlaenge, die kann man so einstellen wie man will, passt
# 2. Variable gibt an, wie scharf eine Kurve ist, alle Werte davon muessen am Ende 0 ergeben
# 3. Variable gibt an, wie steil ein Huegel ist, alle Werte davon muessen am Ende 0 ergeben
# TODO: Gemeinsame Speicherloesung finden
road = [
    [100, 0, 60],
    [50],
    [100, 0, -60],
    [90, 4],
    [50],
    [90, -4],
    [75, 3, 40],
    [25],
    [100, -3, -40]
]

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
        self.reset_road()
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
    def reset_road(self):

        self.read_road()

        gl.segments[Util.which_segment(gl.playerZ)["index"] + 2]["color"] = Colors.get_start()
        gl.segments[Util.which_segment(gl.playerZ)["index"] + 3]["color"] = Colors.get_start()
        for n in range(gl.rumbleLength):
            gl.segments[len(gl.segments)-1-n]["color"] = Colors.get_finish()

        gl.trackLength = len(gl.segments) * gl.segmentLength
    
    # Hier wird das hinzuzufuegende Segment anhand von Kurven- und Huegel-Parametern angepasst
    def add_segment(self, curve, y):
        n = len(gl.segments)
        # Diese Werte muessen (hoffentlich) nicht mehr geaendert werden, jetzt wo Kurven (curve-Parameter) und Huegel (y-Parameter) benutzt werden
        gl.segments.append(
                {
                    'index': n,
                    'p1':
                        {'world': {
                            'x': None,
                            'y': self.lastY(),
                            'z': n * gl.segmentLength
                        },
                            'camera': {
                                'x': 0,
                                'y': 0,
                                'z': 0
                            },
                            'screen': {
                                "scale": 0,
                                'x': 0,
                                'y': 0,
                            },
                        },
                    'p2':
                        {'world': {
                            'x': None,
                            'y': y,
                            'z': (n + 1) * gl.segmentLength
                        },
                            'camera': {
                                'x': 0,
                                'y': 0,
                                'z': 0
                            },
                            'screen': {
                                "scale": 0,
                                'x': 0,
                                'y': 0,
                            },
                        },
                        "curve": curve,
                        "cars": [],
                        "clip": 0,
                    "color": self.which_road(n)
                }
            )

    # Fuegt Strassenteile an das Segment-Array hinzu
    def add_road(self, enter, hold, leave, curve, y=0):
        startY = self.lastY()
        endY = startY + (int(y)*gl.segmentLength)
        total = int(enter) + int(hold) + int(leave)
        
        for n in range(int(enter)):
            self.add_segment(Util.easeIn(0, curve, n / enter), Util.easeInOut(startY, endY, n / total))
        
        for n in range(int(hold)):
            self.add_segment(curve, Util.easeInOut(startY, endY, (enter + n) / total))

        for n in range(int(leave)):
            self.add_segment(Util.easeInOut(0, curve, n / enter), Util.easeInOut(startY, endY, (enter + hold + n) / total))

    # Ueberprueft, ob Werte des Straßenmoduls leer ist
    def add_street(self, num=None, curve=None, height=None):
        if num is None:
            num = Road.length().get("medium")
        if curve is None:
            curve = Road.curve().get("none")
        if height is None:
            height = Road.hill().get("none")

        self.add_road(num, num, num, curve, height)

    # Gibt die letzte Y-Koordinate aus, um einen glatten Huegel zu modellieren
    def lastY(self):
        if len(gl.segments) == 0:
            return 0
        return gl.segments[len(gl.segments)-1].get("p2").get("world").get("y")

    # Hilfsmethode, um zu gucken, welche Farbe das aktuelle Strassenstueck haben muss
    def which_road(self, n):
         if (n / gl.rumbleLength) % 2 == 0:
              return Colors.get_light()
         else:
              return Colors.get_dark()


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

    # Liest das Strassen-Array aus und entscheidet je nach Menge an Werten, ob Kurven oder Huegel zum Segment gehoeren
    def read_road(self):
        for x in road:
            if len(x) == 1:
                self.add_street(x[0])
            elif len(x) == 2:
                self.add_street(x[0], x[1])
            elif len(x) == 3:
                self.add_street(x[0], x[1], x[2])