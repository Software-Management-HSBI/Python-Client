import pygame
import math

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

player = None
player_sprites = None
background_sprites = None

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