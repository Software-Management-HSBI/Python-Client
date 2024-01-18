import random


class Sprite:
    @staticmethod
    def get_car():
        i = random.randint(0, 5)
        if i == 0:
            car = {"asset": "assets/npc/car01.png", "width": 80, "height": 56}
        elif i == 1:
            car = {"asset": "assets/npc/car02.png", "width": 80, "height": 59}
        elif i == 2:
            car = {"asset": "assets/npc/car03.png", "width": 88, "height": 55}
        elif i == 3:
            car = {"asset": "assets/npc/car04.png", "width": 80, "height": 57}
        elif i == 4:
            car = {"asset": "assets/npc/semi.png", "width": 122, "height": 144}
        elif i == 5:
            car = {"asset": "assets/npc/truck.png", "width": 100, "height": 78}
        else:
            car = {"asset": "assets/npc/car01.png", "width": 80, "height": 56}

        return car

    @staticmethod
    def create_tree():
        i = random.randint(0, 8)
        if i == 0:
            tree = {"asset": "assets/tree/tree01.png", "width": 360, "height": 360}
        elif i == 1:
            tree = {"asset": "assets/tree/tree02.png", "width": 215, "height": 540}
        elif i == 2:
            tree = {"asset": "assets/tree/tree03.png", "width": 282, "height": 295}
        elif i == 3:
            tree = {"asset": "assets/tree/palm_tree.png", "width": 215, "height": 540}
        elif i == 4:
            tree = {"asset": "assets/tree/dead_tree1.png", "width": 135, "height": 332}
        elif i == 5:
            tree = {"asset": "assets/tree/boulder1.png", "width": 168, "height": 248}
        elif i == 6:
            tree = {"asset": "assets/tree/boulder2.png", "width": 298, "height": 140}
        elif i == 7:
            tree = {"asset": "assets/tree/dead_tree2.png", "width": 150, "height": 260}
        elif i == 8:
            tree = {"asset": "assets/tree/stump.png", "width": 195, "height": 140}
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

