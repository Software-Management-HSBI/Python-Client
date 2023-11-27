import math

class Util:
    @staticmethod
    def timestamp():
        return int(round(time.time() * 1000))

    @staticmethod
    def toInt(obj, default):
        if obj is not None:
            try:
                return int(obj)
            except ValueError:
                pass
        return Util.toInt(default, 0)

    @staticmethod
    def toFloat(obj, default):
        if obj is not None:
            try:
                return float(obj)
            except ValueError:
                pass
        return Util.toFloat(default, 0.0)

    @staticmethod
    def limit(value, minimum, maximum):
        return max(minimum, min(value, maximum))

    @staticmethod
    def randomInt(minimum, maximum):
        return round(Util.interpolate(minimum, maximum, random.random()))

    @staticmethod
    def randomChoice(options):
        return options[Util.randomInt(0, len(options) - 1)]

    @staticmethod
    def percentRemaining(n, total):
        return (n % total) / total

    @staticmethod
    def accelerate(v, accel, dt):
        return v + (accel * dt)

    @staticmethod
    def interpolate(a, b, percent):
        return a + (b - a) * percent

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
    def exponentialFog(distance, density):
        return 1 / (math.pow(math.e, (distance * distance * density)))

    @staticmethod
    def increase(start, increment, maximum):
        result = start + increment
        while result >= maximum:
            result -= maximum
        while result < 0:
            result += maximum
        return result

    @staticmethod
    def project(p, cameraX, cameraY, cameraZ, cameraDepth, width, height, roadWidth):
        p.camera.x = (p.world.x or 0) - cameraX
        p.camera.y = (p.world.y or 0) - cameraY
        p.camera.z = (p.world.z or 0) - cameraZ
        p.screen.scale = cameraDepth / p.camera.z
        p.screen.x = round((width / 2) + (p.screen.scale * p.camera.x * width / 2))
        p.screen.y = round((height / 2) - (p.screen.scale * p.camera.y * height / 2))
        p.screen.w = round((p.screen.scale * roadWidth * width / 2))

    @staticmethod
    def overlap(x1, w1, x2, w2, percent=1):
        half = percent / 2
        min1 = x1 - (w1 * half)
        max1 = x1 + (w1 * half)
        min2 = x2 - (w2 * half)
        max2 = x2 + (w2 * half)
        return not (max1 < min2 or min1 > max2)
