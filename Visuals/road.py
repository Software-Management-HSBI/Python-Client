import globals as gl
from Gamefiles.util import Util
from Visuals.colors import Colors
from Visuals.spriteCreation import Sprites


class Road:

    # Liest das Strassen-Array aus und markiert Start-/Ziellinie
    @staticmethod
    def reset_road():

        gl.segments = []

        Road.read_road()
        Sprites.create_bots()
        Sprites.create_obstacles(gl.segments)

        gl.segments[Util.which_segment(gl.playerZ)["index"] + 2]["color"] = Colors.get_start()
        gl.segments[Util.which_segment(gl.playerZ)["index"] + 3]["color"] = Colors.get_start()
        for n in range(gl.rumbleLength):
            gl.segments[len(gl.segments) - 1 - n]["color"] = Colors.get_finish()

        gl.trackLength = len(gl.segments) * gl.segmentLength

    # Hier wird das hinzuzufuegende Segment anhand von Kurven- und Huegel-Parametern angepasst
    @staticmethod
    def add_segment(curve, y):
        n = len(gl.segments)
        gl.segments.append(
            {
                'index': n,
                'p1':
                    {'world': {
                        'x': None,
                        'y': Road.lastY(),
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
                "sprites": [],
                "color": Road.which_road(n)
            }
        )

    # Fuegt Strassenteile an das Segment-Array hinzu
    @staticmethod
    def add_road(enter, hold, leave, curve, y=0):
        startY = Road.lastY()
        endY = startY + (int(y) * gl.segmentLength)
        total = int(enter) + int(hold) + int(leave)

        for n in range(int(enter)):
            Road.add_segment(Util.easeIn(0, curve, n / enter), Util.easeInOut(startY, endY, n / total))

        for n in range(int(hold)):
            Road.add_segment(curve, Util.easeInOut(startY, endY, (enter + n) / total))

        for n in range(int(leave)):
            Road.add_segment(Util.easeInOut(0, curve, n / enter),
                             Util.easeInOut(startY, endY, (enter + hold + n) / total))

    # Ueberprueft, ob Werte des Straßenmoduls leer ist
    @staticmethod
    def add_street(num=None, curve=None, height=None):
        if num is None:
            num = Road.length().get("medium")
        if curve is None:
            curve = Road.curve().get("none")
        if height is None:
            height = Road.hill().get("none")

        Road.add_road(num, num, num, curve, height)

    # Gibt die letzte Y-Koordinate aus, um einen glatten Huegel zu modellieren
    @staticmethod
    def lastY():
        if len(gl.segments) == 0:
            return 0
        return gl.segments[len(gl.segments) - 1].get("p2").get("world").get("y")

    # Hilfsmethode, um zu gucken, welche Farbe das aktuelle Strassenstueck haben muss
    @staticmethod
    def which_road(n):
        if (n / gl.rumbleLength) % 2 == 0:
            return Colors.get_light()
        else:
            return Colors.get_dark()

    # Liest das Strassen-Array aus und entscheidet je nach Menge an Werten, ob Kurven oder Huegel zum Segment gehoeren
    @staticmethod
    def read_road():
        for x in gl.road:
            if len(x) == 1:
                Road.add_street(x[0])
            elif len(x) == 2:
                Road.add_street(x[0], x[1])
            elif len(x) == 3:
                Road.add_street(x[0], x[1], x[2])

    @staticmethod
    def length():
        road = {
            "none": 0,
            "short": 25,
            "medium": 50,
            "long": 100
        }
        return road

    @staticmethod
    def curve():
        curve = {
            "none": 0,
            "easy": 2,
            "medium": 4,
            "hard": 6
        }
        return curve

    @staticmethod
    def hill():
        hill = {
            "none": 0,
            "low": 20,
            "medium": 40,
            "high": 60
        }
        return hill
