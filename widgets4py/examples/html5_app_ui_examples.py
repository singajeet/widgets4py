import os
import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
from widgets4py.layouts import SimpleGridLayout
from widgets4py.html5.app_ui import Button, TextBox, CheckBox
from multiprocessing import Process


app = Flask(__name__)


class W2UIPage:

    pg = None
    btn_btn = None
    btn_enb_dsbl = None
    btn_title = None
    txt = None
    btn_txt_rd = None
    btn_txt_enb_dsbl = None
    chk = None
    btn_chk_dsbl = None
    btn_chk = None

    def show_layout(self):
        self.pg = Page('pg', 'Forms')
        sg1 = SimpleGridLayout('sg1', 1, 3)
        self.btn_btn = Button('btn_btn', 'My Button', onclick_callback=self.btn_clicked, app=app)
        self.btn_enb_dsbl = Button('btn_enb_dsbl', 'Toggle Enable/Disable', onclick_callback=self.btn_clicked, app=app)
        self.btn_title = Button('btn_title', 'Change Title', onclick_callback=self.btn_clicked, app=app)
        sg1.add(self.btn_btn)
        sg1.add(self.btn_enb_dsbl)
        sg1.add(self.btn_title)
        sg2 = SimpleGridLayout('sg2', 1, 3)
        self.txt = TextBox('txt', app=app, onchange_callback=self.text_changed)
        self.btn_txt_rd = Button('btn_txt_rd', 'Toggle ReadOnly', app=app, onclick_callback=self.btn_clicked)
        self.btn_txt_enb_dsbl = Button('btn_txt_enb_dsbl', 'Toggle Enable/Disable', app=app,
                                       onclick_callback=self.btn_clicked)
        sg2.add(self.txt)
        sg2.add(self.btn_txt_rd)
        sg2.add(self.btn_txt_enb_dsbl)
        sg3 = SimpleGridLayout('sg3', 1, 3)
        self.chk = CheckBox('chk', 'CheckBox', value="checkit", onclick_callback=self.chk_clicked, app=app)
        self.btn_chk = Button('btn_chk', 'Toggle Checked', app=app, onclick_callback=self.btn_clicked)
        self.btn_chk_dsbl = Button('btn_chk_dsbl', 'Toggle Disabled', app=app, onclick_callback=self.btn_clicked)
        sg3.add(self.chk)
        sg3.add(self.btn_chk)
        sg3.add(self.btn_chk_dsbl)
        self.pg.add(sg1)
        self.pg.add(sg2)
        self.pg.add(sg3)
        return self.pg.render()

    def chk_clicked(self, source, props):
        print(source + "'s clicked: " + props['checked'] + ", " + props['value'])

    def text_changed(self, source, props):
        print(source + "'s Text Changed: " + props['text'])

    def btn_clicked(self, source, props):
        if source == 'btn_btn':
            print("My button clicked")
        elif source == 'btn_enb_dsbl':
            self.btn_btn.disabled = not self.btn_btn.disabled
        elif source == 'btn_title':
            if self.btn_btn.title == 'My Button':
                self.btn_btn.title = 'Your Button'
            else:
                self.btn_btn.title = 'My Button'
        elif source == 'btn_txt_rd':
            self.txt.readonly = not self.txt.readonly
        elif source == 'btn_txt_enb_dsbl':
            self.txt.disabled = not self.txt.disabled
        elif source == 'btn_chk':
            self.chk.checked = not self.chk.checked
        elif source == 'btn_chk_dsbl':
            self.chk.disabled = not self.chk.disabled


def start_app():
    p = W2UIPage()
    app.add_url_rule('/', 'index', p.show_layout)
    app.run(host='127.0.0.1', port=5000)


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
