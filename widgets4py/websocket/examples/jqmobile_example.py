from widgets4py.base import Page
from widgets4py.websocket.jqmobile.ui import MPage, Button, ButtonStyle
from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)


class MobileExample:

    _pg = None
    _mpg = None

    def show_layout(self):
        self._pg = Page('pg', 'Mobile Example')
        self._mpg1 = MPage('mpg1', 'Page1 Example', socketio)
        self._mpg2 = MPage('mpg2', 'Page2 Example', socketio)
        self._btn = Button('btn', socketio, btn_styles=[ButtonStyle.ROUND_CORNERS, ButtonStyle.ICON_LEFT],
                           title="My Button", icon='ui-icon-delete', click_callback=self.btn_clicked)
        self._mpg1.add(self._btn)
        self._pg.add(self._mpg1)
        self._pg.add(self._mpg2)
        return self._pg.render()

    def btn_clicked(self, source, props):
        if self._btn.icon == 'ui-icon-delete':
            self._btn.icon = 'ui-icon-alert'
        else:
            self._btn.icon = 'ui-icon-delete'


def start_app():
    p = MobileExample()
    app.add_url_rule('/', 'index', p.show_layout)
    # socketio.on_namespace(p.bt)
    socketio.run(app, debug=True)


if __name__ == '__main__':
    start_app()
