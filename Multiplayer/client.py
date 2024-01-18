import socketio

import globals as gl
from Gamefiles.carAI import AI
from Visuals.spriteCreation import Sprites


class SocketIOClient:
    """Client fuer die Socket.io-Verbindung."""
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

    def on_update_position(self, data):
        """Client erhaelt Positionen anderer Spieler"""
        pos = data.get("pos")
        offset = data.get("offset")

        AI.update_player_cars(pos, offset)

    def ingame_pos(self, player, position, x):
        """Uebergibt dem Server die aktuelle Position des Clients"""
        if self.olddata != position:
            data = {"player": player, "position": position, "x": x}
            self.sio.emit("update", data)

    def connect(self):
        """Verbindet sich ueber die angegebene Adresse mit dem Server"""
        try:
            if not self.sio.connected:
                self.sio.connect(self.server_address)
        except ConnectionRefusedError:
            print("Connection-Error")

    def on_client_ingame(self):
        """Diese Methode wird genutzt, um den Spieler von der Lobby ins Spiel zu werfen,
         d. h. das muss der Server ausführen"""
        if self.sio.connected:
            self.sio.emit("client_ingame")

    def disconnect(self):
        try:
            self.sio.disconnect()
        except ConnectionRefusedError:
            print("Not connected in the first place")
