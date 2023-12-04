import pygame
import math
import sys
import time

from Gamefiles.util import Util
from Visuals.player import Player
from Visuals.background import Background
from Visuals.road import Road
from Visuals.colors import Colors

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
    [25]
    [100, -3, -40]
]

# Der Teil des Singleplayers, der alle anderen aktiviert: Hier werden Tasteneingaben überprüft und die Straße unendlich erweitert
class Game:

    pygame.init()
    # Sowohl in Python als auch in JavaScript sorgt das Veraedern der FPS fuer Probleme beim Spielverhalten
    FPS = 60
    STEP = 1/FPS
    DT = STEP

    width = 1024
    height = 768

    segments = []

    screen = None
    background = None
    sprites = None
    resolution = None

    # roadWidth bestimmt, wie breit die gesamte Strasse (alle Spuren) sein soll
    roadWidth = 2000
    segmentLength = 200
    rumbleLength = 3
    trackLength = 0
    # lanes bestimmt, wie viele Spuren es auf der Straße geben soll (je breiter die Straße, desto mehr Spuren können realistisch genutzt werden)
    lanes = 3

    fov = 100
    cameraHeight = 1000
    cameraDepth = 1 / math.tan((fov / 2) * math.pi / 180)
    drawDistance = 300
    playerX = 0
    playerZ = cameraHeight * cameraDepth
    fogDensity = 10

    position = 0
    speed = 0
    maxSpeed = segmentLength/STEP
    accel = maxSpeed/5 - 10
    breaking = -maxSpeed
    decel = -maxSpeed/5
    offRoadDecel = -maxSpeed/2
    offRoadLimit = maxSpeed/4

    # Beeinflusst das Verhalten des Autos in der Kurve; Je groesser der Wert, desto schwieriger die Lenkung
    centrifugal = 0.3
    # Falls wir V4 vom JavaScript machen wollen, werden die NPC-Autos in diesem Array gespeichert
    cars = []
    keyLeft = False
    keyRight = False
    keyFaster = False
    keySlower = False

    current_lap_time = 0
    last_lap_time = 0
    best_lap_time = float('inf')
    font = pygame.font.SysFont(None, 36)
    lap_start_time = 0

    # Erstellt den Bildschirm, startet das Generieren der Strasse, und beginnt das Spiel
    def __init__(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Singleplayer")
        self.player_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.lap_start_time = time.time()
        self.reset_road()
        self.game_loop()

    # Loop des Spiels: Erstellt Spieler und Hintergrund, nimmt Inputs entgegen und ruft permanent die render- und update-Methode auf
    def game_loop(self):
        self.create_player()
        self.create_background()
        self.background_sprites.draw(self.screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.keyLeft = True
                    if event.key == pygame.K_RIGHT:
                        self.keyRight = True
                    if event.key == pygame.K_UP:
                        self.keyFaster = True
                    if event.key == pygame.K_DOWN:
                        self.keySlower = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.keyLeft = False
                    if event.key == pygame.K_RIGHT:
                        self.keyRight = False
                    if event.key == pygame.K_UP:
                        self.keyFaster = False
                    if event.key == pygame.K_DOWN:
                        self.keySlower = False

            self.render()
            self.update(self.STEP)
            pygame.display.update()

    # Hier wird anhand der Nutzereingaben die Steuerung des Autos geaendert
    def update(self, dt):
        start_position = self.position

        self.position = Util.increase(self.position, dt * self.speed, self.trackLength)
        current_segment = self.which_segment(self.position + self.playerZ)

        tilt = dt * 2 * (self.speed / self.maxSpeed)

        if self.keyLeft:
            self.playerX = self.playerX - tilt
            if self.speed > 0:
                self.player.drive_left()
        elif self.keyRight:
            self.playerX = self.playerX + tilt
            if self.speed > 0:
                self.player.drive_right()
        else:
            self.player.drive_straight()

        self.playerX -= tilt * (self.speed / self.maxSpeed) * current_segment.get("curve") * self.centrifugal

        if self.keyFaster:
            self.speed = Util.accelerate(self.speed, self.accel, self.DT)
        elif self.keySlower:
            self.speed = Util.accelerate(self.speed, self.breaking, self.DT)
        else:
            self.speed = Util.accelerate(self.speed, self.decel, self.DT)

        if (self.playerX < -1 or self.playerX > 1) and (self.speed > self.offRoadLimit):
            self.speed = Util.accelerate(self.speed, self.offRoadDecel, self.DT)

        self.playerX = Util.limit(self.playerX, -2, 2)
        self.speed = Util.limit(self.speed, 0, self.maxSpeed)

        # Das alles hier ist die Lap-Berechnung, ich hab versucht, alles in eine andere Methode zu verschieben,
        # allerdings wird dann keine neue Runde registriert. Daher muss die Ueberpruefung erstmal hier bleiben.

        # Ueberprueft, ob Runde gefahren wurde
        if self.position > self.playerZ:
            if self.current_lap_time and (start_position < self.playerZ):
                self.last_lap_time = self.current_lap_time
                self.current_lap_time = 0

                self.lap_start_time = time.time()
                # Checkt nach Bestzeit
                if self.last_lap_time < self.best_lap_time:
                    self.best_lap_time = self.last_lap_time
            else:
                # Laesst die Zeit weiterlaufen.
                current_time = time.time()
                self.current_lap_time = current_time - self.lap_start_time

        self.update_time(self.current_lap_time, self.last_lap_time, self.best_lap_time)

    # Zeigt aktuelle, letzte und beste Zeit an
    def update_time(self, current_lap_time, last_lap_time, best_lap_time):
        best_time_text = self.font.render(f"Noch keine Runde gefahren", True, Colors.RED)
        timer_text = self.font.render(f"Aktuelle Runde: {int(current_lap_time)} Sekunden", True, Colors.BLACK)
        last_time_text = self.font.render(f"Letzte Runde: {int(last_lap_time)} Sekunden", True, Colors.BLUE)
        if not math.isinf(self.best_lap_time):
            best_time_text = self.font.render(f"Beste Runde: {int(best_lap_time)} Sekunden", True, Colors.RED)
        self.screen.blit(timer_text, (10, 10))
        self.screen.blit(last_time_text, (10, 50))
        self.screen.blit(best_time_text, (10, 90))
        
    # Liest das Strassen-Array aus und markiert Start-/Ziellinie
    def reset_road(self):

        self.read_road()

        self.segments[self.which_segment(self.playerZ)["index"] + 2]["color"] = Colors.get_start()
        self.segments[self.which_segment(self.playerZ)["index"] + 3]["color"] = Colors.get_start()
        for n in range(self.rumbleLength):
            self.segments[len(self.segments)-1-n]["color"] = Colors.get_finish()

        self.trackLength = len(self.segments) * self.segmentLength
    
    # Hier wird das hinzuzufuegende Segment anhand von Kurven- und Huegel-Parametern angepasst
    def add_segment(self, curve, y):
        n = len(self.segments)
        # Diese Werte muessen (hoffentlich) nicht mehr geaendert werden, jetzt wo Kurven (curve-Parameter) und Huegel (y-Parameter) benutzt werden
        self.segments.append(
                {
                    'index': n,
                    'p1':
                        {'world': {
                            'x': None,
                            'y': self.lastY(),
                            'z': n * self.segmentLength
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
                            'z': (n + 1) * self.segmentLength
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
        endY = startY + (int(y)*self.segmentLength)
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
        if len(self.segments) == 0:
            return 0
        return self.segments[len(self.segments)-1].get("p2").get("world").get("y")

    # Hilfsmethode, um zu gucken, welche Farbe das aktuelle Strassenstueck haben muss
    def which_road(self, n):
         if (n / self.rumbleLength) % 2 == 0:
              return Colors.get_light()
         else:
              return Colors.get_dark()

    # Hilfsmethode, um das derzeit notwendige Segment auszuwaehlen
    def which_segment(self, n):
         return self.segments[math.floor(n / self.segmentLength) % len(self.segments)]
    
    # Setzt ab einem bestimmten Punkt die Distanz der Strecke zurueck (?) und zeichnet Strecke, Nebel und Spieler auf den Bildschirm
    def render(self):
        base = self.which_segment(self.position)
        base_percent = Util.percent_remaining(self.position, self.segmentLength)
        current_segment = self.which_segment(self.position + self.playerZ)
        current_percent = Util.percent_remaining(self.position + self.playerZ, self.segmentLength)
        playerY = Util.interpolate(current_segment.get("p1").get("world").get("y"), current_segment.get("p2").get("world").get("y"), current_percent)

        dx = -(base.get("curve") * base_percent)
        x = 0
        maxY = self.height

        self.background_sprites.draw(self.screen)

        for n in range(self.drawDistance):
            segment = self.segments[(base.get("index") + n) % len(self.segments)]
            segment_looped = segment.get("index") < base.get("index")
            segment_fog = Util.exponential_fog(n / self.drawDistance, self.fogDensity)
            segment["clip"] = maxY

            if segment_looped:
                segment_looped_value = self.trackLength
            else:
                segment_looped_value = 0

            segment["p1"] = Util.project(
                segment.get("p1"),
                (self.playerX * self.roadWidth) - x,
                playerY + self.cameraHeight,
                self.position - segment_looped_value,
                self.cameraDepth,
                self.width, self.height,
                self.roadWidth)

            segment["p2"] = Util.project(
                segment.get("p2"),
                (self.playerX * self.roadWidth) -x - dx,
                playerY + self.cameraHeight,
                self.position - segment_looped_value,
                self.cameraDepth,
                self.width, self.height,
                self.roadWidth)
            
            x += dx
            dx += segment.get("curve")

            if (segment.get("p1").get("camera").get("z") <= self.cameraDepth) or (
                    segment.get("p2").get("screen").get("y") >= maxY) or (
                    segment.get("p2").get("screen").get("y") >= segment.get("p1").get("screen").get("y")):
                continue

            Util.segment(self.screen, self.width, self.lanes,
                        segment.get("p1").get("screen").get("x"),
                        segment.get("p1").get("screen").get("y"),
                        segment.get("p1").get("screen").get("w"),
                        segment.get("p2").get("screen").get("x"),
                        segment.get("p2").get("screen").get("y"),
                        segment.get("p2").get("screen").get("w"),
                        segment.get("color"), segment_fog)

            maxY = segment.get("p1").get("screen").get("y")

            self.player_sprites.draw(self.screen)   

    # Erstellt mit einer Hilfsklasse die einzelnen Hintergrundschichten
    def create_background(self):
        surface_sky = Background(0, pygame.image.load("assets/sky.png"))
        surface_hills = Background(0, pygame.image.load("assets/hills.png"))
        surface_trees = Background(0, pygame.image.load("assets/trees.png"))

        self.background_sprites.add(surface_sky)
        self.background_sprites.add(surface_hills)
        self.background_sprites.add(surface_trees)

    # Platziert den Spieler in der Mitte der Strecke und ordnet ihm die Auto-Sprites zu
    def create_player(self):
        self.player = Player(self.screen.get_width() / 2 - 30, self.screen.get_height() - 100)
        self.player_sprites.add(self.player)

    # Liest das Strassen-Array aus und entscheidet je nach Menge an Werten, ob Kurven oder Huegel zum Segment gehoeren
    def read_road(self):
        for x in road:
            if len(x) == 1:
                self.add_street(x[0])
            elif len(x) == 2:
                self.add_street(x[0], x[1])
            elif len(x) == 3:
                self.add_street(x[0], x[1], x[2])