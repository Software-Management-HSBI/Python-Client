# Hilfsklasse fuer die Strassenfarben
class Colors:
    def get_finish():
        c = {
            "road": "#000000",
            "grass": "#000000",
            "rumble": "#000000",
            "lane": "#000000"
        }
        return c

    def get_light():
        c = {
            "road": "#6B6B6B",
            "grass": "#10AA10",
            "rumble": "#555555",
            "lane": "#CCCCCC"
        }
        return c

    def get_start():
        c = {
            "road": "#FFFFFF",
            "grass": "#FFFFFF",
            "rumble": "#FFFFFF",
            "lane": "#FFFFFF"
        }
        return c

    def get_dark():
        c = {
            "road": "#696969",
            "grass": "#009A00",
            "rumble": "#BBBBBB",
            "lane": "#696969"
        }
        return c