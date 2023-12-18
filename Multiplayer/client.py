from Gamefiles.util import Util
import globals as gl
import socketio
import pygame

sio = socketio.Client(logger=True)


# Client fuer die Socket.io-Verbindung. Muss erweitert werden
class Client:
    def init(self, game_class):
        self.server_address = "http://localhost:3000"
        self.Game = game_class
        self.sio = sio
        sio.on('connect', self.on_connection_success)
        sio.on('disconnect', self.on_disconnect)

        
        try:
            sio.connect(self.server_address)
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def on_connection_success(self):
        connected_ev = pygame.event.Event(gl.CONNECTED)
        pygame.event.post(connected_ev)

    @sio.on('*')
    def catch_all(event, data):
        print(data)

    @sio.on('player_moved')
    def player_moved(data):
        # Ignorar caso o pacote seja meu próprio
        if data["sid"] != sio.sid:
            ev = pygame.event.Event(gl.PLAYER_MOVED, data)
            pygame.event.post(ev)

    @sio.on('player_entered')
    def player_entered(data):
        if data["sid"] != sio.sid:
            # Novo jogador entrou
            other_connected_ev = pygame.event.Event(gl.PLAYER_ENTERED, { "sid": data["sid"] })
            pygame.event.post(other_connected_ev)


    def on_disconnect(self):
        print("Disconnected from the server")

    def disconnect_from_server(self):
        sio.disconnect()