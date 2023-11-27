import Util
import Standard_Config
import Render
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Bringt hoffentlich das Auto zum Fahren
def update(dt):
    global position, playerX, speed

    position = Util.increase(position, dt * speed, Standard_Config.trackLength)

    dx = dt * 2 * (speed / Standard_Config.maxSpeed)  # at top speed, should be able to cross from left to right (-1 to 1) in 1 second

    if Standard_Config.keyLeft:
        playerX = playerX - dx
    elif Standard_Config.keyRight:
        playerX = playerX + dx

    if Standard_Config.keyFaster:
        speed = Util.accelerate(speed, Standard_Config.accel, dt)
    elif Standard_Config.keySlower:
        speed = Util.accelerate(speed, Standard_Config.breaking, dt)
    else:
        speed = Util.accelerate(speed, Standard_Config.decel, dt)

    if ((playerX < -1 or playerX > 1) and (speed > Standard_Config.offRoadLimit)):
        speed = Util.accelerate(speed, Standard_Config.offRoadDecel, dt)

    playerX = Util.limit(playerX, -2, 2)     # dont ever let player go too far out of bounds
    speed = Util.limit(speed, 0, Standard_Config.maxSpeed)   # or exceed maxSpeed

def render():
    global position, playerX, width, height, drawDistance, roadWidth, cameraHeight, cameraDepth, fogDensity, segments, trackLength, lanes, sprites, speed, maxSpeed, keyLeft, keyRight, playerZ, resolution

    baseSegment = findSegment(position)
    maxy = height

    Standard_Config.ctx.clearRect(0, 0, width, height)

    pygame.draw("assets/background/hills.png")
    pygame.draw("assets/background/sky.png")
    pygame.draw("assets/background/trees.png")

    for n in range(drawDistance):
        segment = segments[(baseSegment.index + n) % len(segments)]
        segment.looped = segment.index < baseSegment.index
        segment.fog = Util.exponentialFog(n / drawDistance, fogDensity)

        Util.project(segment.p1, (playerX * roadWidth), cameraHeight, position - (segment.looped and trackLength or 0), cameraDepth, width, height, roadWidth)
        Util.project(segment.p2, (playerX * roadWidth), cameraHeight, position - (segment.looped and trackLength or 0), cameraDepth, width, height, roadWidth)

        if segment.p1.camera.z <= cameraDepth or segment.p2.screen.y >= maxy:
            continue

        Render.segment(Standard_Config.ctx, width, lanes, segment.p1.screen.x, segment.p1.screen.y, segment.p1.screen.w, segment.p2.screen.x, segment.p2.screen.y, segment.p2.screen.w, segment.fog, segment.color)

        maxy = segment.p2.screen.y

    Render.player(Standard_Config.ctx, width, height, resolution, roadWidth, sprites, speed / maxSpeed, cameraDepth / playerZ, width / 2, height, speed * (-1 if keyLeft else 1 if keyRight else 0), 0)

def reset_road():
    global segments, trackLength, playerZ

    segments = []
    segmentLength = 200
    rumbleLength = 5

    for n in range(500):
        segment = {
            'index': n,
            'p1': {'world': {'z': n * segmentLength}, 'camera': {}, 'screen': {}},
            'p2': {'world': {'z': (n + 1) * segmentLength}, 'camera': {}, 'screen': {}},
            'color': BLACK if n // rumbleLength % 2 else WHITE
        }
        segments.append(segment)

    start_index = find_segment(playerZ).index + 2
    segments[start_index].color = COLORS['START']
    segments[start_index + 1]['color'] = COLORS['START']

    for n in range(rumbleLength):
        segments[-1 - n]['color'] = COLORS['FINISH']

    trackLength = len(segments) * segmentLength


def find_segment(z):
    return segments[z // Standard_Config.segmentLength % len(segments)]
