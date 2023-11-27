import socketio


class SocketIOClient:
    def __init__(self):
        self.server_address = ""

        self.sio = socketio.Client(logger=True)

        self.sio.on('connection_success', self.connection_succes)
    

    def connection_succes(self):
        print("Connection established")


    def connect(self):
        try:
            self.sio.connect()
        except ConnectionError:
            print("Couldn't connect")


