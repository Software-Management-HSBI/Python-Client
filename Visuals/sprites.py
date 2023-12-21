import random


class Sprite:

    @staticmethod
    def get_car():
        i = random.randint(0, 3)
        if i == 0:
            car = {"asset": "assets/npc/car01.png", "width": 80, "height": 56}
        elif i == 1:
            car = {"asset": "assets/npc/car02.png", "width": 80, "height": 59}
        elif i == 2:
            car = {"asset": "assets/npc/car03.png", "width": 88, "height": 55}
        elif i == 3:
            car = {"asset": "assets/npc/car04.png", "width": 80, "height": 57}
        else:
            car = {"asset": "assets/npc/car01.png", "width": 80, "height": 56}

        return car

    @staticmethod
    def create_tree():
        i = random.randint(0, 2)
        if i == 0:
            tree = {"asset": "assets/tree/tree01.png", "width": 360, "height": 360}
        elif i == 1:
            tree = {"asset": "assets/tree/tree02.png", "width": 215, "height": 540}
        elif i == 2:
            tree = {"asset": "assets/tree/tree03.png", "width": 282, "height": 295}
        else:
            tree = {"asset": "assets/tree/tree01.png", "width": 360, "height": 360}

        return tree

    @staticmethod
    def create_billboard():
        i = random.randint(0, 8)
        if i == 0:
            billboard = {"asset": "assets/billboard/BetterCallSus.jpg", "width": 360, "height": 360, "offset": -1}
        elif i == 1:
            billboard = {"asset": "assets/billboard/billboard02.png", "width": 360, "height": 360, "offset": 1}
        elif i == 2:
            billboard = {"asset": "assets/billboard/billboard03.png", "width": 360, "height": 360, "offset": -1}
        elif i == 3:
            billboard = {"asset": "assets/billboard/billboard04.png", "width": 360, "height": 360, "offset": 1}
        elif i == 4:
            billboard = {"asset": "assets/billboard/billboard05.png", "width": 360, "height": 360, "offset": -1}
        elif i == 5:
            billboard = {"asset": "assets/billboard/billboard06.png", "width": 360, "height": 360, "offset": 1}
        elif i == 6:
            billboard = {"asset": "assets/billboard/billboard07.png", "width": 360, "height": 360, "offset": -1}
        elif i == 7:
            billboard = {"asset": "assets/billboard/billboard08.png", "width": 360, "height": 360, "offset": 1}
        elif i == 8:
            billboard = {"asset": "assets/billboard/billboard09.png", "width": 360, "height": 360, "offset": -1}
        else:
            billboard = {"asset": "assets/billboard/BetterCallSus.jpg", "width": 360, "height": 360, "offset": 1}

        return billboard

