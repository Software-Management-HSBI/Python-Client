import globals as gl
from Gamefiles.util import Util

class Render:

    @staticmethod
    def render():
        base = Util.which_segment(gl.position)
        base_percent = Util.percent_remaining(gl.position, gl.segmentLength)
        current_segment = Util.which_segment(gl.position + gl.playerZ)
        current_percent = Util.percent_remaining(gl.position + gl.playerZ, gl.segmentLength)
        playerY = Util.interpolate(current_segment.get("p1").get("world").get("y"), current_segment.get("p2").get("world").get("y"), current_percent)

        dx = -(base.get("curve") * base_percent)
        x = 0
        maxY = gl.height

        gl.background_sprites.draw(gl.screen)

        for n in range(gl.drawDistance):
            segment = gl.segments[(base.get("index") + n) % len(gl.segments)]
            segment_looped = segment.get("index") < base.get("index")
            segment_fog = Util.exponential_fog(n / gl.drawDistance, gl.fogDensity)
            segment["clip"] = maxY

            if segment_looped:
                segment_looped_value = gl.trackLength
            else:
                segment_looped_value = 0

            segment["p1"] = Util.project(
                segment.get("p1"),
                (gl.playerX * gl.roadWidth) - x,
                playerY + gl.cameraHeight,
                gl.position - segment_looped_value,
                gl.cameraDepth,
                gl.width, gl.height,
                gl.roadWidth)

            segment["p2"] = Util.project(
                segment.get("p2"),
                (gl.playerX * gl.roadWidth) -x - dx,
                playerY + gl.cameraHeight,
                gl.position - segment_looped_value,
                gl.cameraDepth,
                gl.width, gl.height,
                gl.roadWidth)
            
            x += dx
            dx += segment.get("curve")

            if (segment.get("p1").get("camera").get("z") <= gl.cameraDepth) or (
                    segment.get("p2").get("screen").get("y") >= maxY) or (
                    segment.get("p2").get("screen").get("y") >= segment.get("p1").get("screen").get("y")):
                continue

            Util.segment(gl.screen, gl.width, gl.lanes,
                        segment.get("p1").get("screen").get("x"),
                        segment.get("p1").get("screen").get("y"),
                        segment.get("p1").get("screen").get("w"),
                        segment.get("p2").get("screen").get("x"),
                        segment.get("p2").get("screen").get("y"),
                        segment.get("p2").get("screen").get("w"),
                        segment.get("color"), segment_fog)

            maxY = segment.get("p1").get("screen").get("y")

        for n in range(gl.drawDistance -1, 0, -1):
            segment = gl.segments[(base.get("index") + n) % len(gl.segments)]
            Render.render_cars(segment)

        gl.player_sprites.draw(gl.screen)

    @staticmethod
    def render_cars(segment):
        for i in range(len(segment.get("cars"))):
            car = segment.get("cars")[i]
            sprite = car.get("sprite")
            car["percent"] = Util.percent_remaining(car.get("z"), gl.segmentLength)

            sprite_scale = Util.interpolate(segment.get("p1").get("screen").get("scale"),
                                            segment.get("p2").get("screen").get("scale"), car.get("percent"))

            sprite_x = Util.interpolate(segment.get("p1").get("screen").get("x"),
                                        segment.get("p2").get("screen").get("x"), car.get("percent")) + (
                               sprite_scale * car.get("offset") * gl.roadWidth * (gl.width / 2))

            sprite_y = Util.interpolate(segment.get("p1").get("screen").get("y"),
                                        segment.get("p2").get("screen").get("y"), car.get("percent"))

            Util.sprite(gl.screen, gl.width, gl.roadWidth, sprite, sprite_scale, sprite_x,
                        sprite_y, -0.5, -1, segment.get("clip"))
