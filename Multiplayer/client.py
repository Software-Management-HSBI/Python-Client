import socketio
import globals as gl


# Client fuer die Socket.io-Verbindung. Muss erweitert werden
class Client:
    def __init__(self):
        self.server_address = ""
        self.sio = socketio.Client(logger=True)

        # Reaktionen auf verschiedene Ereignisse
        self.sio.on('connection_successful', self.on_connection_success)
        self.sio.on('load_level', self.on_load_level)
        self.sio.on('updated_positions', self.on_updated_positions)

    def on_connection_success(self):
        print("Connection established")

    def on_load_level(self, data):
        if self.sio.connected:
            if data != '':
                gl.road = data
                gl.singleplayer = False

    def connect(self):
        try:
            self.sio.connect(self.server_address, transports=['websocket'])
        except ConnectionError:
            print("Error while connecting")

    def disconnect(self):
        if self.sio.connected:
            self.sio.disconnect()

    def on_updated_positions(self, data):
        pass

    def ingame_pos(self, position, offset):
        if gl.position != position:
            data = {
                "offset": offset,
                "position": position
            }
            gl.position = position
            self.sio.emit("ingame_position", data)
