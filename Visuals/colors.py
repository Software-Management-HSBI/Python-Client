# Hilfsklasse fuer die Strassenfarben
class Colors:

    # In der Colors-Klasse werden jetzt auch RGB-Arrays fuer andere Dateien gespeichert
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    LIGHT_RED = (255, 100, 100)  # Gehoverte Rot-Version
    LIGHT_GREEN = (100, 255, 100)  # Gehoverte Grün-Version
    LIGHT_BLUE = (100, 100, 255)  # Gehoverte Blau-Version
    LIGHT_YELLOW = (255, 255, 100)  # Gehoverte Gelb-Version
    LIGHT_GRAY = (200, 200, 200)

    @staticmethod
    def get_finish():
        c = {
            "road": "#000000",
            "grass": "#000000",
            "rumble": "#000000",
            "lane": "#000000"
        }
        return c

    @staticmethod
    def get_light():
        c = {
            "road": "#6B6B6B",
            "grass": "#10AA10",
            "rumble": "#555555",
            "lane": "#CCCCCC"
        }
        return c

    @staticmethod
    def get_start():
        c = {
            "road": "#FFFFFF",
            "grass": "#FFFFFF",
            "rumble": "#FFFFFF",
            "lane": "#FFFFFF"
        }
        return c

    @staticmethod
    def get_dark():
        c = {
            "road": "#696969",
            "grass": "#009A00",
            "rumble": "#BBBBBB",
            "lane": "#696969"
        }
        return c
