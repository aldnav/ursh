
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['debug'] = True
socketio = SocketIO(app)


@socketio.on('message')
def handle_message(message):
    send(message)


@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)


@socketio.on('message:shoot')
def handle_message(request):
    print request


@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)
