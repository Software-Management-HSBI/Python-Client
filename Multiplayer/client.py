import socketio


# Client fuer die Socket.io-Verbindung. Muss erweitert werden
class Client:
    def __init__(self):
        self.server_address = ""
        self.sio = socketio.Client(logger=True)

        self.sio.on('connection_successful', self.on_connection_success)

    def on_connection_success(self):
        print("Connection established")
