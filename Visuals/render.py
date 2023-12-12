import globals as gl
from Gamefiles.util import Util


class Render:

    @staticmethod
    def render():
        base = Util.which_segment(gl.position)
        base2 = Util.which_segment(gl.position2)
        base_percent = Util.percent_remaining(gl.position, gl.segmentLength)
        base_percent_2 = Util.percent_remaining(gl.position2, gl.segmentLength)
        current_segment = Util.which_segment(gl.position + gl.playerZ)
        current_segment2 = Util.which_segment(gl.position2 + gl.playerZ2)
        current_percent = Util.percent_remaining(gl.position + gl.playerZ, gl.segmentLength)
        current_percent2 = Util.percent_remaining(gl.position2 + gl.playerZ2, gl.segmentLength)
        playerY = Util.interpolate(current_segment.get("p1").get("world").get("y"),
                                   current_segment.get("p2").get("world").get("y"), current_percent)
        playerY2 = Util.interpolate(current_segment2.get("p1").get("world").get("y"),
                                    current_segment2.get("p2").get("world").get("y"), current_percent2)

        dx = -(base.get("curve") * base_percent)
        dx2 = -(base2.get("curve") * base_percent_2)
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
                (gl.playerX * gl.roadWidth) - x - dx,
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

            gl.player_sprites.draw(gl.screen)
            gl.player_sprites2.draw(gl.screen)

