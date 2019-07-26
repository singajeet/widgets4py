from flask import Flask
from flask_socketio import SocketIO
from widgets4py.base import Page
from widgets4py.websocket.html5.app_ui import Button


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)


class PageTest:

    bt = None
    bt1 = None

    def show_layout(self):
        pg = Page('pg', 'Websocket')
        self.bt = Button('bt', 'Button', app, socketio, click_callback=self.btn_clicked)
        self.bt1 = Button('bt1', 'Button 1', app, socketio, click_callback=self.btn1_clicked)
        pg.add(self.bt)
        pg.add(self.bt1)
        return pg.render()

    def btn_clicked(self, source, props):
        self.bt1.disabled = not self.bt1.disabled
        if self.bt1.disabled:
            self.bt1.title = 'Disabled Button 1'
        else:
            self.bt1.title = 'Button 1'

    def btn1_clicked(self, source, props):
        self.bt.disabled = not self.bt.disabled
        if self.bt.disabled:
            self.bt.title = 'Disabled Button'
        else:
            self.bt.title = 'Button'


def start_app():
    p = PageTest()
    app.add_url_rule('/', 'index', p.show_layout)
    # socketio.on_namespace(p.bt)
    socketio.run(app, debug=True)


if __name__ == '__main__':
    start_app()
