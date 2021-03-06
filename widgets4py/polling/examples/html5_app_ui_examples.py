import os
import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
from widgets4py.layouts import SimpleGridLayout
from widgets4py.polling.html5.app_ui import Button, TextBox, CheckBox, Color, Date, DateTimeLocal, Email, File
from widgets4py.polling.html5.app_ui import Image, Month, Number, Password, Radio, Reset, Range, Search, Submit
from widgets4py.polling.html5.app_ui import Telephone, Time, URL, Week, Label, Form, DropDown
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
    clr = None
    btn_clr_dsbl = None
    dt = None
    btn_dt_dsbl = None
    btn_dt_rd = None
    btn_dt_min = None
    btn_dt_max = None
    dtl = None
    btn_dtl_dsbl = None
    btn_dtl_rd = None
    btn_dtl_min = None
    btn_dtl_max = None
    _file = None
    btn_fl_dsbl = None
    btn_fl_multi = None
    img = None
    mth = None
    num = None
    password = None
    rd = None
    rset = None
    rng = None
    srch = None
    sbmt = None
    tlph = None
    time = None
    url = None
    week = None
    dd = None

    def show_layout(self):
        self.pg = Page('pg', 'Forms')
        sg1 = SimpleGridLayout('sg1', 1, 3)
        self.btn_btn = Button('btn_btn', 'My Button', onclick_callback=self.btn_clicked, app=app)
        self.btn_enb_dsbl = Button('btn_enb_dsbl', 'Toggle Enable/Disable', onclick_callback=self.btn_clicked, app=app)
        self.btn_title = Button('btn_title', 'Change Title', onclick_callback=self.btn_clicked, app=app)
        sg1.add(self.btn_btn)
        sg1.add(self.btn_enb_dsbl)
        sg1.add(self.btn_title)
        sg2 = SimpleGridLayout('sg2', 1, 4)
        self.txt = TextBox('txt', app=app, onchange_callback=self.text_changed)
        self.btn_txt_rd = Button('btn_txt_rd', 'Toggle ReadOnly', app=app, onclick_callback=self.btn_clicked)
        self.btn_txt_enb_dsbl = Button('btn_txt_enb_dsbl', 'Toggle Enable/Disable', app=app,
                                       onclick_callback=self.btn_clicked)
        sg2.add(Label('lbl_txt', 'Text', self.txt))
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
        sg4 = SimpleGridLayout('sg4', 1, 2)
        self.clr = Color('clr', app=app, onchange_callback=self.clr_changed)
        self.btn_clr_dsbl = Button('btn_clr_dsbl', "Toggle Disabled", app=app, onclick_callback=self.btn_clicked)
        sg4.add(self.clr)
        sg4.add(self.btn_clr_dsbl)
        sg5 = SimpleGridLayout('sg5', 1, 6)
        self.dt = Date('dt', app=app, onchange_callback=self.dt_changed)
        self.btn_dt_dsbl = Button('btn_dt_dsbl', 'Toggle Disable', app=app, onclick_callback=self.btn_clicked)
        self.btn_dt_rd = Button('btn_dt_rd', 'Toggle Readonly', app=app, onclick_callback=self.btn_clicked)
        self.btn_dt_min = Button('btn_dt_min', 'Change Min', app=app, onclick_callback=self.btn_clicked)
        self.btn_dt_max = Button('btn_dt_max', 'Change Max', app=app, onclick_callback=self.btn_clicked)
        sg5.add(Label('lbl_sg5', 'Date', self.dt))
        sg5.add(self.dt)
        sg5.add(self.btn_dt_dsbl)
        sg5.add(self.btn_dt_rd)
        sg5.add(self.btn_dt_min)
        sg5.add(self.btn_dt_max)
        sg6 = SimpleGridLayout('sg6', 1, 6)
        self.dtl = DateTimeLocal('dtl', app=app, onchange_callback=self.dt_changed)
        self.btn_dtl_dsbl = Button('btn_dtl_dsbl', 'Toggle Disable', app=app, onclick_callback=self.btn_clicked)
        self.btn_dtl_rd = Button('btn_dtl_rd', 'Toggle Readonly', app=app, onclick_callback=self.btn_clicked)
        self.btn_dtl_min = Button('btn_dtl_min', 'Change Min', app=app, onclick_callback=self.btn_clicked)
        self.btn_dtl_max = Button('btn_dtl_max', 'Change Max', app=app, onclick_callback=self.btn_clicked)
        sg6.add(Label('lbl_sg6', 'DateTimeLocal', self.dtl))
        sg6.add(self.dtl)
        sg6.add(self.btn_dtl_dsbl)
        sg6.add(self.btn_dtl_rd)
        sg6.add(self.btn_dtl_min)
        sg6.add(self.btn_dtl_max)
        sg7 = SimpleGridLayout('sg7', 1, 4)
        self.email = Email('email', app=app, onchange_callback=self.text_changed)
        self.btn_eml_rd = Button('btn_eml_rd', 'Toggle ReadOnly', app=app, onclick_callback=self.btn_clicked)
        self.btn_eml_enb_dsbl = Button('btn_eml_enb_dsbl', 'Toggle Enable/Disable', app=app,
                                       onclick_callback=self.btn_clicked)
        sg7.add(Label('lbl_email', 'Email', self.email))
        sg7.add(self.email)
        sg7.add(self.btn_eml_rd)
        sg7.add(self.btn_eml_enb_dsbl)
        sg8 = SimpleGridLayout('sg8', 1, 3)
        self._file = File('_file', app=app, onchange_callback=self.file_changed)
        self.btn_fl_dsbl = Button('btn_fl_dsbl', 'Toggle Disable', app=app, onclick_callback=self.btn_clicked)
        self.btn_fl_multi = Button('btn_fl_multi', 'Toggle Multiple', app=app, onclick_callback=self.btn_clicked)
        sg8.add(self._file)
        sg8.add(self.btn_fl_dsbl)
        sg8.add(self.btn_fl_multi)
        sg9 = SimpleGridLayout('sg9', 14, 2)
        self.img = Image('img', 'src', app=app)
        self.mth = Month('mth', app=app)
        self.num = Number('num', app=app)
        self.password = Password('password', app=app)
        self.rd = Radio('rd', 'Radio', app=app)
        self.rset = Reset('rset', 'Reset', app=app)
        self.rng = Range('rng', app=app)
        self.srch = Search('srch', app=app)
        self.sbmt = Submit('sbmt', 'Submit', app=app)
        self.tlph = Telephone('tlph', app=app)
        self.time = Time('time', app=app)
        self.url = URL('url', app=app)
        self.week = Week('week', app=app)
        self.dd = DropDown('dd', app=app)
        self.dd.add_option('abc', 'ABC', True)
        self.dd.add_option('def', 'DEF')
        self.dd.add_option('ghi', 'GHI')
        sg9.add(Label('lbl', 'Image', self.img))
        sg9.add(self.img)
        sg9.add(Label('lbl1', 'Month', self.mth))
        sg9.add(self.mth)
        sg9.add(Label('lbl', 'Number', self.num))
        sg9.add(self.num)
        sg9.add(Label('lbl', 'Password', self.password))
        sg9.add(self.password)
        sg9.add(Label('lbl', 'Radio', self.rd))
        sg9.add(self.rd)
        sg9.add(Label('lbl', 'Reset', self.rset))
        sg9.add(self.rset)
        sg9.add(Label('lbl', 'Range', self.rng))
        sg9.add(self.rng)
        sg9.add(Label('lbl', 'Search', self.srch))
        sg9.add(self.srch)
        sg9.add(Label('lbl', 'Submit', self.sbmt))
        sg9.add(self.sbmt)
        sg9.add(Label('lbl', 'Telephone', self.tlph))
        sg9.add(self.tlph)
        sg9.add(Label('lbl', 'Time', self.time))
        sg9.add(self.time)
        sg9.add(Label('lbl', 'Url', self.url))
        sg9.add(self.url)
        sg9.add(Label('lbl', 'Week', self.week))
        sg9.add(self.week)
        sg9.add(Label('dd_lbl', 'DropDown', self.dd))
        sg9.add(self.dd)
        self.frm = Form('frm', app=app, use_fieldset=True, legend="Form", on_form_submit=self.form_submitted)
        self.frm.add(sg9)
        self.pg.add(sg1)
        self.pg.add(sg2)
        self.pg.add(sg3)
        self.pg.add(sg4)
        self.pg.add(sg5)
        self.pg.add(sg6)
        self.pg.add(sg7)
        self.pg.add(sg8)
        self.pg.add(self.frm)
        return self.pg.render()

    def form_submitted(self, source, form_data):
        print("Form Submitted: " + str(form_data))

    def file_changed(self, source, props):
        print(props['filename'] + " file has been loaded to path: " + props['upload_path'])

    def dt_changed(self, source, props):
        print(source + "'s date changed: " + props['value'] + ", " + props['min'] + ", " + props['max'])

    def clr_changed(self, source, props):
        print(source + "'s color changed: " + props['value'])

    def chk_clicked(self, source, props):
        print(source + "'s clicked: " + props['checked'] + ", " + props['value'])

    def text_changed(self, source, props):
        print(source + "'s Text Changed: " + props['text'])

    def btn_clicked(self, source, props):   # noqa
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
        elif source == 'btn_clr_dsbl':
            self.clr.disabled = not self.clr.disabled
        elif source == 'btn_dt_dsbl':
            self.dt.disabled = not self.dt.disabled
        elif source == 'btn_dt_rd':
            self.dt.readonly = not self.dt.readonly
        elif source == 'btn_dt_min':
            self.dt.min = "1980-12-03"
        elif source == 'btn_dt_max':
            self.dt.max = "2050-12-03"
        elif source == 'btn_dtl_dsbl':
            self.dtl.disabled = not self.dtl.disabled
        elif source == 'btn_dtl_rd':
            self.dtl.readonly = not self.dtl.readonly
        elif source == 'btn_dtl_min':
            self.dtl.min = "1980-12-03"
        elif source == 'btn_dtl_max':
            self.dtl.max = "2050-12-03"
        elif source == 'btn_eml_rd':
            self.email.readonly = not self.email.readonly
        elif source == 'btn_eml_enb_dsbl':
            self.email.disabled = not self.email.disabled
        elif source == 'btn_fl_dsbl':
            self._file.disabled = not self._file.disabled
        elif source == 'btn_fl_multi':
            self._file.multiple = not self._file.multiple


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
        print("Starting Webview and the Application")
        app_proc = Process(target=start_app)
        web_app = Process(target=start_web_view)
        app_proc.start()
        web_app.start()
        app_proc.join()
        web_app.join()
