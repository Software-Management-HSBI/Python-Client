import globals as gl
from Gamefiles.util import Util
from Visuals.colors import Colors
from Visuals.road import Road as R

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

class Road:
    
    # Liest das Strassen-Array aus und markiert Start-/Ziellinie
    @staticmethod
    def reset_road():

        Road.read_road()

        gl.segments[Util.which_segment(gl.playerZ)["index"] + 2]["color"] = Colors.get_start()
        gl.segments[Util.which_segment(gl.playerZ)["index"] + 3]["color"] = Colors.get_start()
        for n in range(gl.rumbleLength):
            gl.segments[len(gl.segments)-1-n]["color"] = Colors.get_finish()

        gl.trackLength = len(gl.segments) * gl.segmentLength
    
    # Hier wird das hinzuzufuegende Segment anhand von Kurven- und Huegel-Parametern angepasst
    @staticmethod
    def add_segment(curve, y):
        n = len(gl.segments)
        # Diese Werte muessen (hoffentlich) nicht mehr geaendert werden, jetzt wo Kurven (curve-Parameter) und Huegel (y-Parameter) benutzt werden
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
                    "color": Road.which_road(n)
                }
            )

    # Fuegt Strassenteile an das Segment-Array hinzu
    @staticmethod
    def add_road(enter, hold, leave, curve, y=0):
        startY = Road.lastY()
        endY = startY + (int(y)*gl.segmentLength)
        total = int(enter) + int(hold) + int(leave)
        
        for n in range(int(enter)):
            Road.add_segment(Util.easeIn(0, curve, n / enter), Util.easeInOut(startY, endY, n / total))
        
        for n in range(int(hold)):
            Road.add_segment(curve, Util.easeInOut(startY, endY, (enter + n) / total))

        for n in range(int(leave)):
            Road.add_segment(Util.easeInOut(0, curve, n / enter), Util.easeInOut(startY, endY, (enter + hold + n) / total))

    # Ueberprueft, ob Werte des Straßenmoduls leer ist
    @staticmethod
    def add_street(num=None, curve=None, height=None):
        if num is None:
            num = R.length().get("medium")
        if curve is None:
            curve = R.curve().get("none")
        if height is None:
            height = R.hill().get("none")

        Road.add_road(num, num, num, curve, height)

    # Gibt die letzte Y-Koordinate aus, um einen glatten Huegel zu modellieren
    @staticmethod
    def lastY():
        if len(gl.segments) == 0:
            return 0
        return gl.segments[len(gl.segments)-1].get("p2").get("world").get("y")

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
        for x in road:
            if len(x) == 1:
                Road.add_street(x[0])
            elif len(x) == 2:
                Road.add_street(x[0], x[1])
            elif len(x) == 3:
                Road.add_street(x[0], x[1], x[2])