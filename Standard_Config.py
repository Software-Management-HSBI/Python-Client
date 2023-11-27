import pygame

fps = 60
step = 1/fps
width = 1024
height = 768
segments = []
screen = pygame.display.set_mode((width, height))
ctx = screen
background = None
sprites = None
resolution = None
roadWidth = 2000
segmentLength = 200
rumbleLenght = 3
trackLength = None
fov = 100
cameraHeight = 1000
cameraDepth = None
drawDistance = 300
playerX = 0
playerZ = None
fogDensity = 5
position = 0
speed = 0
maxSpeed = segmentLength/step
accel = maxSpeed/5
breaking = -maxSpeed
decel = -maxSpeed/5
offRoadDecel = -maxSpeed/2
offRoadLimit = maxSpeed/4

keyLeft = False
keyRight = False
keyFaster = False
keySlower = False