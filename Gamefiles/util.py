import math
import random

import pygame
import time

import globals as gl
from Visuals.colors import Colors


class Util:
    """Die Util-Klasse besitzt hauptsaechlich die Mathematik hinter dem Spiel.
        Ein grosser Teil der Methoden wurde aus dem JavaScript-Original in Python umgeschrieben"""

    @staticmethod
    def increase(start, increment, maximum):
        """Increase veraendert die Position des Spielers abhaengig von seiner Geschwindigkeit"""
        result = start + increment
        while result >= maximum:
            result -= maximum
        while result < 0:
            result += maximum
        return result

    @staticmethod
    def accelerate(v, accel, dt):
        """Beschleunigt das Auto abhaengig von der accel-Klassenvariable des Spiels"""
        return v + (accel * dt)

    @staticmethod
    def limit(value, minimum, maximum):
        """Gibt ein Limit eines Wertes an"""
        return max(minimum, min(value, maximum))

    @staticmethod
    def project(p, camx, camy, camz, camdepth, width, height, roadwidth):
        """Methode aus dem JavaScript, um die Kamera zu bewegen"""
        worldx = Util._if_none(p.get("world").get("x"))
        worldy = Util._if_none(p.get("world").get("y"))
        worldz = Util._if_none(p.get("world").get("z"))

        p.get("camera")["x"] = worldx - camx
        p.get("camera")["y"] = worldy - camy
        p.get("camera")["z"] = worldz - camz

        p.get("screen")["scale"] = camdepth / Util._if_zero(p.get("camera").get("z"))

        p.get("screen")["x"] = round(
            (width / 2) + (p.get("screen").get("scale") * p.get("camera").get("x") * width / 2))

        p.get("screen")["y"] = round(
            (height / 2) - (p.get("screen").get("scale") * p.get("camera").get("y") * height / 2))

        p.get("screen")["w"] = round((p.get("screen").get("scale") * roadwidth * width / 2))
        return p

    @staticmethod
    def _if_none(value):
        if value is not None:
            return value
        else:
            return 0

    @staticmethod
    def _if_zero(value):
        if value == 0:
            return 1
        else:
            return value

    @staticmethod
    def which_segment(n):
        """Hilfsmethode, um das derzeit notwendige Segment auszuwaehlen"""
        return gl.segments[math.floor(n / gl.segmentLength) % len(gl.segments)]

    @staticmethod
    def segment(screen, width, lanes, x1, y1, w1, x2, y2, w2, color, fog):
        """Methode aus dem JavaScript, die die einzelnen Strassenteile modelliert und den Nebel hinzufuegt"""
        r1 = Util.rumble_width(w1, lanes)
        r2 = Util.rumble_width(w2, lanes)
        l1 = Util.lane_marker_width(w1, lanes)
        l2 = Util.lane_marker_width(w2, lanes)
        lane = 1

        Util.gras(screen, color.get("grass"), 0, y2, width, y1 - y2)

        Util.polygon(screen, x1 - w1 - r1, y1, x1 - w1, y1, x2 - w2, y2, x2 - w2 - r2, y2, color.get("rumble"))
        Util.polygon(screen, x1 + w1 + r1, y1, x1 + w1, y1, x2 + w2, y2, x2 + w2 + r2, y2, color.get("rumble"))
        Util.polygon(screen, x1 - w1, y1, x1 + w1, y1, x2 + w2, y2, x2 - w2, y2, color.get("road"))

        lanew1 = w1 * 2 / lanes
        lanew2 = w2 * 2 / lanes
        lanex1 = x1 - w1 + lanew1
        lanex2 = x2 - w2 + lanew2

        while lane < lanes:
            Util.polygon(screen, lanex1 - l1 / 2, y1, lanex1 + l1 / 2, y1, lanex2 + l2 / 2, y2, lanex2 - l2 / 2,
                         y2,
                         color.get("lane"))
            lanex1 += lanew1
            lanex2 += lanew2
            lane = lane + 1

        Util.fog(screen, 0, y1, width, y1 - y2, fog)

    @staticmethod
    def fog(screen, x, y, width, height, fog):
        """Etwas umformulierte Variante des JavaSript-Nebels, nutzt eine Methode namens 'draw_polygon_alpha',
         um den Nebel richtig darzustellen"""
        if fog < 1:
            Util.draw_polygon_alpha(screen, (0, 81, 8, int((1 - fog) * 255)),
                                    [(x, y - 1), (x + width, y - 1), (x + width, y + height), (x, y + height)])

    @staticmethod
    def draw_polygon_alpha(surface, color, points):
        """Hilfsmethode fuer den Nebel"""
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
        surface.blit(shape_surf, target_rect)

    @staticmethod
    def gras(screen, color, x, y, width, height):
        pygame.draw.polygon(screen, color, [(x, y), (x + width, y), (x + width, y + height), (x, y + height)])

    @staticmethod
    def rumble_width(projectedroadwidth, lanes):
        return projectedroadwidth / max(6, 2 * lanes)

    @staticmethod
    def lane_marker_width(projectedroadwidth, lanes):
        return projectedroadwidth / max(32, 8 * lanes)

    @staticmethod
    def polygon(screen, x1, y1, x2, y2, x3, y3, x4, y4, color):
        pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

    @staticmethod
    def exponential_fog(distance, density):
        return 1 / (math.pow(math.e, (distance * distance * density)))

    @staticmethod
    def sprite(screen: pygame.Surface, width, road_width, sprite, sprite_scale, destX, destY, offset_x, offset_y,
               clip_y):
        """Aus dem JavaScript-Code, wird benutzt, um die Sprites (also Autos und Hindernisse) darzustellen"""
        dest_w = (sprite.get("width") * sprite_scale * width / 2) * (((1 / 80) * 0.3) * road_width)
        dest_h = (sprite.get("height") * sprite_scale * width / 2) * (((1 / 80) * 0.3) * road_width)

        if offset_x is None:
            offset_x = 0
        if offset_y is None:
            offset_y = 0

        destX += dest_w * offset_x
        destY += dest_h * offset_y

        if clip_y is None:
            clip_h = 0
        else:
            clip_h = max(0, destY + dest_h - clip_y)

        if clip_h < dest_h and (dest_w <= (sprite.get("width") * 5) or (dest_h <= (sprite.get("height") * 5))):
            img = pygame.image.load(sprite.get("asset")).convert()
            hill = pygame.transform.scale(img, (dest_w, dest_h))
            hill = pygame.transform.chop(hill, (
                0, hill.get_height() - (hill.get_height() * clip_h / dest_h), 0, sprite.get("height")))
            screen.blit(hill, [destX, destY])

    # Alle 3 ease-Methoden sind fuer die Kurvenmodellierung
    @staticmethod
    def easeIn(a, b, percent):
        return a + (b - a) * math.pow(percent, 2)

    @staticmethod
    def easeOut(a, b, percent):
        return a + (b - a) * (1 - math.pow(1 - percent, 2))

    @staticmethod
    def easeInOut(a, b, percent):
        return a + (b - a) * ((-math.cos(percent * math.pi) / 2) + 0.5)

    @staticmethod
    def percent_remaining(n, total):
        return (n % total) / total

    @staticmethod
    def interpolate(a, b, percent):
        return a + (b - a) * percent

    @staticmethod
    def random_int(min, max):
        return round(Util.interpolate(min, max, random.random()))

    @staticmethod
    def random_choice(options):
        return options[Util.random_int(0, len(options) - 1)]

    @staticmethod
    def check_time(start_position):
        """Ueberprueft, ob Runde gefahren wurde"""
        if gl.position > gl.playerZ:
            if gl.current_lap_time and (start_position < gl.playerZ):
                gl.last_lap_time = gl.current_lap_time
                gl.total_time += gl.current_lap_time
                gl.current_lap_time = 0

                #  Erhoeht die Rundenzahl
                gl.laps += 1
                if gl.laps >= gl.max_laps:
                    gl.maxSpeed = 0.1
                    gl.timer_active = False

                gl.lap_start_time = time.time()
                # Checkt nach Bestzeit
                if gl.last_lap_time < gl.best_lap_time:
                    gl.best_lap_time = gl.last_lap_time
            else:
                # Laesst die Zeit weiterlaufen.
                current_time = time.time()
                gl.current_lap_time = current_time - gl.lap_start_time

    @staticmethod
    def update_time(current_lap_time, last_lap_time, best_lap_time):
        """Zeigt aktuelle, letzte und beste Zeit an"""
        if gl.timer_active:
            formatted_time = "{:.1f}".format(current_lap_time)
            best_time_text = gl.font.render(f"Noch keine Runde gefahren", True, Colors.RED)
            timer_text = gl.font.render(f"Aktuelle Runde: {formatted_time} Sekunden", True, Colors.BLACK)
            last_time_text = gl.font.render(f"Letzte Runde: {int(last_lap_time)} Sekunden", True, Colors.BLUE)
            lap_count_text = gl.font.render(f"Runden: {gl.laps}", True, Colors.LIGHT_BLUE)
            if not math.isinf(gl.best_lap_time):
                best_time_text = gl.font.render(f"Beste Runde: {int(best_lap_time)} Sekunden", True, Colors.RED)
            speed_text = gl.font.render(f"Geschwindigkeit: {int(gl.speed / gl.FPS)} km/h", True, Colors.BLACK)
            gl.screen.blit(timer_text, (10, 10))
            gl.screen.blit(last_time_text, (10, 50))
            gl.screen.blit(best_time_text, (10, 90))
            gl.screen.blit(lap_count_text, (400, 10))
            gl.screen.blit(speed_text, (575, 10))
        else:
            total_time = gl.font.render(f"Gesamtzeit: {gl.total_time:.2f} Sekunden", True, Colors.BLACK)
            gl.screen.blit(total_time, (300, 400))

    @staticmethod
    def overlap(x1, w1, x2, w2, percent=None):
        if percent is None:
            percent = 1
        half = percent / 2
        min1 = x1 - (w1 * half)
        max1 = x1 + (w1 * half)
        min2 = x2 - (w2 * half)
        max2 = x2 + (w2 * half)
        return not ((max1 < min2) or (min1 > max2))

    @staticmethod
    def obstacle_collision(current_segment):
        """Ueberprueft Kollision mit Objekten seitlich der Straße und haelt das Auto bei Kollision komplett an"""
        for n in range(len(current_segment.get("sprites"))):
            sprite = current_segment.get("sprites")[n]
            sprite_w = sprite.get("source").get("width") * (gl.playerw * 1/80)
            h = 0
            if sprite.get("offset") > 0:
                h = 1
            if Util.overlap(gl.playerX, gl.playerw, sprite.get("offset") + sprite_w / 2 * h, sprite_w):
                gl.speed = gl.maxSpeed / 5
                gl.position = Util.increase(current_segment.get("p1").get("world").get("z"),
                                            -gl.playerZ, gl.trackLength)

    @staticmethod
    def car_collision(current_segment):
        """Ueberprueft Kollision mit anderen Autos und verlangsamt den Spieler, falls notwendig"""
        for n in range(len(current_segment.get("cars"))):
            car = current_segment.get("cars")[n]
            car_w = car.get("sprite").get("width") * (gl.playerw * 1/80)
            if gl.speed > car.get("speed"):
                if Util.overlap(gl.playerX, gl.playerw, car.get("offset"), car_w, 0.8):
                    gl.speed = car.get("speed") * (car.get("speed") / gl.speed)
                    gl.position = Util.increase(car.get("z"), -gl.playerZ, gl.trackLength)
                    break
