
import json
import time
from uuid import uuid4
from random import randint
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['debug'] = True
socketio = SocketIO(app)

players = []
rooms = []


@socketio.on('game:register:request')
def register_player(request):
    if len(players) == 2:  # noqa stupid
        return
    player_id = str(uuid4())
    players.append(player_id)
    emit('game:register:success', {'player_id': player_id})
    print 'In game: ', len(players)


@socketio.on('game:join')
def join_player(request):
    player_id = request.get('playerid')
    if player_id not in players:
        players.append(player_id)
    emit('game:join:success', {'player_id': player_id})
    print 'In game: ', len(players)


@socketio.on('game:request_opponent')
def request_opponent(request):
    player_id = request.get('playerid')
    opponent = get_opponent(player_id)
    if opponent:
        emit('game:request_opponent:ready', {'opponent_id': opponent})
    else:
        emit('game:request_opponent:fail', {})


def get_opponent(player_id):
    try:
        if players.index(player_id) == 0:
            return players[1]
        return players[0]
    except (IndexError, ValueError):
        return None


@socketio.on('message:shoot')
def handle_relay(request):
    # player = request.get('player')
    opponent = request.get('opponent')
    time.sleep(randint(10, 100))
    emit(
        'message:pass',
        {'message': request.get('message'),
         'target': opponent},
        broadcast=True)


@socketio.on('game:opponent:sendstack')
def relay_stack(request):
    emit('game:opponent:sendstack:ack', request)


@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)
