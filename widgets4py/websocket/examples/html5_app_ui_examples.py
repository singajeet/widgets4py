import time
from flask import Flask
from flask_socketio import SocketIO
from widgets4py.base import Page
from widgets4py.websocket.html5.app_ui import Button

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)


class PageTest:

    bt = None

    def show_layout(self):
        pg = Page('pg', 'Websocket')
        self.bt = Button('bt', 'Button', app, socketio, click_callback=self.btn_clicked)
        pg.add(self.bt)
        return pg.render()

    def btn_clicked(self, source, props):
        self.bt.disabled = True
        self.bt.title = 'Disabled Button'
        time.sleep(5)
        self.bt.disabled = False
        self.bt.title = 'Button'


def start_app():
    p = PageTest()
    app.add_url_rule('/', 'index', p.show_layout)
    # socketio.on_namespace(p.bt)
    socketio.run(app, debug=True)


if __name__ == '__main__':
    start_app()
