import random

class Sprite:

    @staticmethod
    def get_car():
        i = random.randint(0, 3)
        if i == 0:
            car = {"asset": "assets/npc/car01.png", "width": 80, "height": 56}
        elif i == 1:
            car = {"asset": "assets/npc/car02.png", "width": 80, "height": 56}
        elif i == 2:
            car = {"asset": "assets/npc/car03.png", "width": 80, "height": 56}
        elif i == 3:
            car = {"asset": "assets/npc/car04.png", "width": 80, "height": 56}
        else:
            car = {"asset": "assets/npc/car01.png", "width": 80, "height": 56}

        return car
