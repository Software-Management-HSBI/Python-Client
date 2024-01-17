import socketio

import globals as gl
from Gamefiles.carAI import AI
from Visuals.spriteCreation import Sprites


# Client fuer die Socket.io-Verbindung. Muss erweitert werden
class SocketIOClient:
    def __init__(self):
        self.server_address = "http://ec2-18-159-61-52.eu-central-1.compute.amazonaws.com:3000"
        self.sio = socketio.Client(logger=True)

        self.sio.on('connection_success', self.on_connection_success)
        self.sio.on('load_level', self.on_load_level)
        self.sio.on('wait_for_start', self.on_wait_for_start)
        self.sio.on('update', self.on_update_position)
        self.sio.on('client_ingame', self.on_client_ingame)

        self.new_cars = []
        self.olddata = 0

    def on_connection_success(self):
        print("Connection established")

    def on_load_level(self, data):
        if self.sio.connected:
            if data != '':
                pass

    def ready(self):
        if self.sio.connected:
            self.sio.emit("ready")

    def not_ready(self):
        if self.sio.connected:
            self.sio.emit("not_ready")

    def on_wait_for_start(self, data):
        if self.sio.connected:
            for n in data:
                gl.player_cars.append(n)
            Sprites.create_server_cars()

    # Client erhaelt Positionen anderer Spieler
    def on_update_position(self, data):
        print("klappt")
        self.new_cars.clear()
        for n in data:
            self.new_cars.append(n)

        AI.update_player_cars()

    # Uebergibt dem Server die aktuelle Position des Clients
    def ingame_pos(self, position, offset):
        if self.olddata != position:
            data = {"offset": offset, "position": position}
            self.olddata = position
            self.sio.emit("update", data)

    # Verbindet sich ueber die angegebene Adresse mit dem Server
    def connect(self):
        try:
            if not self.sio.connected:
                self.sio.connect(self.server_address)
        except ConnectionRefusedError:
            print("Connection-Error")

    # Diese Methode wird genutzt, um den Spieler von der Lobby ins Spiel zu werfen, d. h. das muss der Server ausführen
    def on_client_ingame(self):
        if self.sio.connected:
            self.sio.emit("client_ingame")

    def disconnect(self):
        try:
            self.sio.disconnect()
        except ConnectionRefusedError:
            print("Not connected in the first place")
