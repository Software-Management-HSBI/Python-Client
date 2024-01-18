import globals as gl
from Gamefiles.util import Util


# Zustaendig fuer das Verhalten der NPC-Autos; Hier werden sie innerhalb und ausserhalb des Sichtfelds geupdated
class AI:

    # Updatet die NPC-Autos in dem Sichtfeld des Spielers (groesstenteils wie in JS)
    @staticmethod
    def update_cars(dt, player_segment, playerw):
        for n in range(len(gl.cars)):
            car = gl.cars[n]
            old_segment = Util.which_segment(car.get("z"))
            hel = AI.update_offset(car, old_segment, player_segment, playerw)
            if hel is None:
                hel = 0

            car["offset"] = car.get("offset") + hel
            car["z"] = Util.increase(car.get("z"), dt * car.get("speed"), gl.trackLength)
            car["percent"] = Util.percent_remaining(car.get("z"), gl.segmentLength)
            new_segment = Util.which_segment(car.get("z"))
            if old_segment != new_segment:
                index = old_segment.get("cars").index(car)
                old_segment.get("cars").pop(index)
                new_segment.get("cars").append(car)

    # Updated die Autos, wenn sie nicht im Sichtfeld des Spielers sind
    @staticmethod
    def update_offset(car, car_segment, player_segment, playerw):
        ahead = 20
        carw = gl.playerw

        if (car_segment.get("index") - player_segment.get("index")) > gl.drawDistance:
            return 0
        for i in range(1, ahead):
            segment = gl.segments[(car_segment.get("index") + i) % len(gl.segments)]

            if ((segment == player_segment) and (car.get("speed") > gl.speed) and
                    (Util.overlap(gl.playerX, playerw, car.get("offset"), carw, 1.2))):
                if gl.playerX > 0.5:
                    direction = -1
                elif gl.playerX < -0.5:
                    direction = 1
                else:
                    if car.get("offset") > gl.playerX:
                        direction = 1
                    else:
                        direction = -1
                return direction * 1/i * (car.get("speed") - gl.speed) / gl.maxSpeed

            for j in range(len(segment.get("cars"))):
                other_car = segment.get("cars")[j]
                other_car_w = other_car.get("sprite").get("width") * ((1/80) * 0.3)
                if (car.get("speed") > other_car.get("speed")) and Util.overlap(car.get("offset"), carw, other_car.get("offset"), other_car_w, 1.2):

                    if other_car.get("offset") > 0.5:
                        direction = -1
                    elif other_car.get("offset") < -0.5:
                        direction = 1
                    else:
                        if car.get("offset") > other_car.get("offset"):
                            direction = 1
                        else:
                            direction = -1
                    return direction * 1 / i * (car.get("speed") - other_car.get("speed")) / gl.maxSpeed

    @staticmethod
    def update_player_cars(position, offset):
        for car in gl.cars:
            old_segment = car.get("segment")
            car["offset"] = offset
            car["z"] = position
            car["segment"] = Util.which_segment(car.get("z"))

            new_segment = car.get("segment")
            if old_segment != new_segment:
                index = old_segment.get("cars").index(car)
                old_segment.get("cars").pop(index)
                new_segment.get("cars").append(car)
