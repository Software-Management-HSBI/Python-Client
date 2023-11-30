
class Road:

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