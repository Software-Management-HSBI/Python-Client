import eventlet
import socketio

sio = socketio.Server()

players_list = {}

@sio.event
def connect(sid, env, data):
    # Adiciona jogador à lista de jogadores e envia para os que já estão conectados
    players_list.update({sid: { "sid": sid, "x": 0, "y": 0 }})
    sio.emit('player_entered', players_list[sid])

@sio.on('move')
def move(sid, data):
    players_list[sid] = {
        "sid": sid,
        "x": data["x"],
        "y": data["y"],
        "z": data["z"]
    }

    sio.emit('player_moved', players_list[sid])

app = socketio.WSGIApp(sio)

eventlet.wsgi.server(eventlet.listen(('', 3000)), app)