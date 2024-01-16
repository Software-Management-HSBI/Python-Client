import socketio

import globals as gl
from Gamefiles.carAI import AI


# Client fuer die Socket.io-Verbindung. Muss erweitert werden
class SocketIOClient:
    def __init__(self):
        self.server_address = "ec2-18-159-61-52.eu-central-1.compute.amazonaws.com:3000"
        self.sio = socketio.Client(logger=True)

        self.sio.on('connection_successful', self.on_connection_success)
        self.sio.on('load_level', self.on_load_level)
        self.sio.on('wait_for_start', self.on_wait_for_start)
        self.sio.on('update_position', self.on_update_position)
        self.sio.on('client_ingame', self.on_client_ingame)

        self.ready = False
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
            self.ready = True

    def not_ready(self):
        if self.sio.connected:
            self.sio.emit("not_ready")
            self.ready = False

    def on_wait_for_start(self, data):
        if self.sio.connected:
            for n in data:
                gl.player_cars.append(n)

    def on_update_position(self, data):
        self.new_cars.clear()
        for n in data:
            self.new_cars.append(n)

        AI.update_player_cars()

    def ingame_pos(self, offset, position):
        if self.olddata != position:
            data = {"offset": offset, "position": position}
            self.olddata = position
            self.sio.emit("ingame_pos", data)

    def connect(self):
        try:
            self.sio.connect(self.server_address, transports=['websocket'])
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
