from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


class MyExample(Namespace):
    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        print("Receive count : %d" % (session['receive_count']))
        print("Message Received: " + message['data'])
        emit('my_response',
             {'data': 'Message Collected', 'count': session['receive_count']})

    def on_connect(self):
        print("Connected...")

    def on_disconnect(self):
        print('Client disconnected', request.sid)


socketio.on_namespace(MyExample('/test'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
