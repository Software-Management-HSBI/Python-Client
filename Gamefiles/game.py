import pygame
import sys
import time

from Gamefiles.util import Util
from Visuals.render import Render
from Visuals.road import Road
from Visuals.spriteCreation import Sprites
from Gamefiles.carAI import AI
from Gamefiles.player import Player

import globals as gl

# Der Teil des Singleplayers, der alle anderen aktiviert: Hier werden Tasteneingaben überprüft und die Straße unendlich erweitert
class Game:

    # Erstellt den Bildschirm, startet das Generieren der Strasse, und beginnt das Spiel
    def __init__(self, sid = None, client = None):
        # Se receber um socket id (significa que estamos no multiplayer)
        self.players_data = [Player(sid, True)]
        self.sid = sid
        self.client = client
            
        gl.screen = pygame.display.set_mode((gl.width, gl.height))
        pygame.display.set_caption("Singleplayer")
        gl.player_sprites = pygame.sprite.Group()
        gl.background_sprites = pygame.sprite.Group()
        gl.lap_start_time = time.time()
        Road.reset_road()
        self.game_loop()
    
    def new_player(self, sid):
        self.players_data.append(Player(sid, False))
    
    def update_player(self, sid, x, z):
        for player in self.players_data:
            if player.sid == sid:
                player.x = x
                player.z = z
                player.update_car(z)

    # Loop des Spiels: Erstellt Spieler und Hintergrund, nimmt Inputs entgegen und ruft permanent die render- und update-Methode auf
    def game_loop(self):
        for player in self.players_data:
                player.start()
        Sprites.create_background()
        gl.background_sprites.draw(gl.screen)
        while True:
            for player in self.players_data:
                player.update()
            
            for event in pygame.event.get():
                # Outra pessoa se conectou
                if event.type == gl.PLAYER_ENTERED:
                    self.new_player(event["sid"])
                # Outra pessoa enviou movimento
                elif event.type == gl.PLAYER_MOVED:
                    self.update_player(event.data["sid"], event.data["x"], event.data["z"])

            Render.render()
            self.update(gl.STEP)
            pygame.display.flip()

            gl.clock.tick(gl.FPS)


    # Hier wird anhand der Nutzereingaben die Steuerung des Autos geaendert
    def update(self, dt):
        start_position = gl.position

        gl.position = Util.increase(gl.position, dt * gl.speed, gl.trackLength)
        current_segment = Util.which_segment(gl.position + gl.playerZ)

        tilt = dt * 2 * (gl.speed / gl.maxSpeed)

        if gl.keyLeft:
            gl.playerX = gl.playerX - tilt
            if gl.speed > 0:
                gl.player.drive_left()
        elif gl.keyRight:
            gl.playerX = gl.playerX + tilt
            if gl.speed > 0:
                gl.player.drive_right()
        else:
            gl.player.drive_straight()

        gl.playerX -= tilt * (gl.speed / gl.maxSpeed) * current_segment.get("curve") * gl.centrifugal

        if gl.keyFaster:
            gl.speed = Util.accelerate(gl.speed, gl.accel, gl.DT)
        elif gl.keySlower:
            gl.speed = Util.accelerate(gl.speed, gl.breaking, gl.DT)
        else:
            gl.speed = Util.accelerate(gl.speed, gl.decel, gl.DT)

        if (gl.playerX < -1 or gl.playerX > 1) and (gl.speed > gl.offRoadLimit):
            gl.speed = Util.accelerate(gl.speed, gl.offRoadDecel, gl.DT)

        AI.update_cars(dt, current_segment, gl.playerw)

        for car in current_segment.get("cars"):
            carW = car.get("z") * ((1/80) * 0.3)
            if gl.speed > car.get("speed"):
                if Util.overlap(gl.playerX, gl.playerw, car.get("offset"), carW, 0.8):
                    gl.speed = car.get("speed") * (car.get("speed") / gl.speed)
                    gl.position = Util.increase(car.get("z"), -gl.playerZ, gl.trackLength)
                    # Irgendwas hier funktioniert noch nicht richtig
                    break

        gl.playerX = Util.limit(gl.playerX, -2, 2)
        gl.speed = Util.limit(gl.speed, 0, gl.maxSpeed)

        for player in self.players_data:
            # Só envia atualizações caso o jogador esteja em movimento
            # E caso seja informação do jogador que eu controlo
            if self.sid == player.sid and gl.speed != 0:
                self.client.sio.emit('move', { "x": player.x, "y": player.y, "z": gl.position })

        # Fast alles bezueglich Zeit wurde jetzt nach Util verlagert
        Util.check_time(start_position)

        Util.update_time(gl.current_lap_time, gl.last_lap_time, gl.best_lap_time)

