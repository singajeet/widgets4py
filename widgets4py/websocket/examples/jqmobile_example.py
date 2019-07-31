from widgets4py.base import Page
from widgets4py.websocket.jqmobile.ui import MPage, Button, ButtonStyle, FormButton, CheckBox
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
        self._mpg1 = MPage('mpg1', 'Page1 Example', socketio, footer_title="Footer")
        self._mpg2 = MPage('mpg2', 'Page2 Example', socketio, footer_title="Footer")
        self._btn = Button('btn', socketio, btn_styles=[ButtonStyle.ROUND_CORNERS, ButtonStyle.ICON_LEFT],
                           title="My Button", icon='ui-icon-delete', click_callback=self.btn_clicked)
        self._btn1 = FormButton('btn1', socketio, title="Form Button", icon='ui-icon-delete',
                                btn_styles=[ButtonStyle.ROUND_CORNERS, ButtonStyle.ICON_LEFT],
                                click_callback=self.btn_clicked)
        self._chkbox = CheckBox('chkbox', socketio, is_group=True, orientation="vertical",
                                icon_position="right", legend="My Checkboxes",
                                click_callback=self.chk_clicked)
        self._chkbox.add_item('item1', 'Item1')
        self._chkbox.add_item('item2', 'Item2')
        self._chkbox.add_item('item3', 'Item3')
        self._chkbox.add_item('item4', 'Item4')
        self._mpg1.add(self._btn)
        self._mpg1.add(self._btn1)
        self._mpg1.add(self._chkbox)
        self._pg.add(self._mpg1)
        self._pg.add(self._mpg2)
        return self._pg.render()

    def chk_clicked(self, source, status, items):
        print("Check Clicked: " + source + ", " + str(status))

    def btn_clicked(self, source, props):
        if self._btn.icon == 'ui-icon-delete':
            self._btn.icon = 'ui-icon-alert'
            self._btn.remove_style(ButtonStyle.ICON_LEFT)
            self._btn.add_style(ButtonStyle.ICON_RIGHT)
        else:
            self._btn.remove_style(ButtonStyle.ICON_RIGHT)
            self._btn.add_style(ButtonStyle.ICON_LEFT)
            self._btn.icon = 'ui-icon-delete'


def start_app():
    p = MobileExample()
    app.add_url_rule('/', 'index', p.show_layout)
    # socketio.on_namespace(p.bt)
    socketio.run(app, debug=True)


if __name__ == '__main__':
    start_app()
