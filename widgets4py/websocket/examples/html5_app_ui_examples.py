from flask import Flask
from flask_socketio import SocketIO
from widgets4py.base import Page
from widgets4py.websocket.html5.app_ui import Button, TextBox, CheckBox


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)


class PageTest:

    bt = None
    bt1 = None
    txt = None
    chk = None

    def show_layout(self):
        pg = Page('pg', 'Websocket')
        self.bt = Button('bt', 'Button', socketio, click_callback=self.btn_clicked)
        self.bt1 = Button('bt1', 'Button 1', socketio, click_callback=self.btn1_clicked)
        self.txt = TextBox('txt', socketio, change_callback=self.txt_changed)
        self.chk = CheckBox('chk', socketio, title='My Checkbox', click_callback=self.chk_clicked)
        pg.add(self.bt)
        pg.add(self.bt1)
        pg.add(self.txt)
        pg.add(self.chk)
        return pg.render()

    def chk_clicked(self, source, props):
        print("Checked changed to: " + str(props['checked']))
        self.txt.readonly = not self.txt.readonly

    def txt_changed(self, source, props):
        print("Txt changed: " + props['text'])

    def btn_clicked(self, source, props):
        self.bt1.disabled = not self.bt1.disabled
        if self.bt1.disabled:
            self.bt1.title = 'Disabled Button 1'
        else:
            self.bt1.title = 'Button 1'
        self.txt.disabled = not self.txt.disabled

    def btn1_clicked(self, source, props):
        self.bt.disabled = not self.bt.disabled
        if self.bt.disabled:
            self.bt.title = 'Disabled Button'
        else:
            self.bt.title = 'Button'
        self.chk.disabled = not self.chk.disabled


def start_app():
    p = PageTest()
    app.add_url_rule('/', 'index', p.show_layout)
    # socketio.on_namespace(p.bt)
    socketio.run(app, debug=True)


if __name__ == '__main__':
    start_app()
