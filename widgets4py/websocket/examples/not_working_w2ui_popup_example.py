import os
import webview
import time
from flask import Flask  # , url_for
from flask_socketio import SocketIO
from widgets4py.base import Page
from multiprocessing import Process
from widgets4py.websocket.w2ui.ui import Popup
from widgets4py.websocket.html5.app_ui import Button
from widgets4py.layouts import SimpleGridLayout


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)


class W2UIPage:

    pg = None
    pop = None
    bt_open = None
    sg = None

    def show_layout(self):
        self.pg = Page('pg', 'Popup Example')
        self.pop = Popup('pop', socketio, 'Test Title',
                         buttons='<input type="button" onclick="w2popup.close();" value="Close" />',
                         show_max=True, show_close=True, modal=True,
                         body='<span>This message for you to show in popup widow!</span>',
                         on_close_callback=self.pop_closed, on_keydown_callback=self.pop_key_pressed,
                         on_max_callback=self.pop_max, on_min_callback=self.pop_min,
                         on_open_callback=self.pop_open, on_toggle_callback=self.pop_toggled)
        self.bt_open = Button('bt_open', 'Open', socketio, click_callback=self.button_open)
        self.sg = SimpleGridLayout('sg', 1, 1)
        self.sg.add(self.bt_open)
        self.pg.add(self.pop)
        self.pg.add(self.sg)
        return self.pg.render()

    def pop_closed(self):
        print("Popup Closed!")

    def pop_key_pressed(self):
        print("Popup Key Pressed!")

    def pop_max(self):
        print("Popup Maximized!")

    def pop_min(self):
        print("Popup Minimized!")

    def pop_open(self):
        print("Popup Opened!")

    def pop_toggled(self):
        print("Popup Toggled!")

    def button_open(self, name, props):
        print('Opening...')
        self.pop.open()
        time.sleep(10)
        print('Closing...')
        self.pop.close()
        time.sleep(10)
        print('Opening again...')
        self.pop.open()
        time.sleep(10)
        print('Loading...')
        self.pop.load('https://google.com')
        time.sleep(10)
        print('Closing again...')
        self.pop.close()
        time.sleep(10)
        print('Opening again!')
        self.pop.open()
        time.sleep(10)
        print('Locking up')
        self.pop.lock("Popup Locked", True)
        time.sleep(10)
        print('Unlocking it')
        self.pop.unlock()
        time.sleep(10)
        print('Locking screen...')
        self.pop.lock_screen()
        time.sleep(10)
        print('Unlocking screen')
        self.pop.unlock_screen()
        time.sleep(10)
        print('Closing again...')
        self.pop.close()
        time.sleep(10)
        print('Opening again!')
        self.pop.open()
        time.sleep(10)
        print('Maximizing')
        self.pop.max()
        time.sleep(10)
        print('Minimizing')
        self.pop.min()
        time.sleep(10)
        print('Resizing')
        self.pop.resize(800, 800)
        print('Done!')


def start_app():
    p = W2UIPage()
    app.add_url_rule('/', 'index', p.show_layout)
    socketio.run(app, debug=True)


def start_web_view():
    webview.create_window("My Application", "http://localhost:5000", resizable=True)


if __name__ == "__main__":
    if os.uname().machine == 'aarch64':
        start_app()
    else:
        app_proc = Process(target=start_app)
        web_app = Process(target=start_web_view)
        app_proc.start()
        web_app.start()
        app_proc.join()
        web_app.join()
