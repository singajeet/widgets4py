from flask import Flask
from flask_socketio import SocketIO
from widgets4py.base import Page
from widgets4py.websocket.html5.app_ui import Button, TextBox, CheckBox, Color, Date, DateTimeLocal
from widgets4py.websocket.html5.app_ui import Image, Month, Number, Password, Radio, Range, Email
from widgets4py.websocket.html5.app_ui import File, Reset, Search, Submit, Telephone, Time, URL
from widgets4py.websocket.html5.app_ui import Week, Form, ListBox, Label
from widgets4py.layouts import SimpleGridLayout
from engineio.payload import Payload


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
Payload.max_decode_packets = 500
socketio = SocketIO(app, async_mode=None)


class PageTest:

    bt = None
    bt1 = None
    txt = None
    chk = None
    clr = None
    dt = None
    dtl = None
    eml = None
    fl = None
    img = None
    mth = None
    num = None
    pswd = None
    rd = None
    rng = None
    rst = None
    srch = None
    sbmt = None
    tel = None
    time = None
    url = None
    week = None
    frm = None
    frm_text = None
    lbox = None
    lbl = None

    def show_layout(self):
        pg = Page('pg', 'Websocket')
        sg = SimpleGridLayout('sg', 25, 2)
        self.bt = Button('bt', 'Button', socketio, click_callback=self.btn_clicked)
        self.bt1 = Button('bt1', 'Button 1', socketio, click_callback=self.btn1_clicked)
        self.txt = TextBox('txt', socketio, change_callback=self.txt_changed)
        self.chk = CheckBox('chk', socketio, title='My Checkbox', click_callback=self.chk_clicked)
        self.clr = Color('clr', socketio, change_callback=self.color_changed)
        self.dt = Date('dt', socketio, change_callback=self.dt_changed)
        self.dtl = DateTimeLocal('dtl', socketio, change_callback=self.dt_changed)
        self.eml = Email('eml', socketio, change_callback=self.txt_changed)
        self.fl = File('fl', socketio, change_callback=self.fl_changed, click_callback=self.fl_clicked)
        self.img = Image('img', '', socketio, click_callback=self.btn_clicked)
        self.mth = Month('mth', socketio, change_callback=self.dt_changed)
        self.num = Number('num', socketio, change_callback=self.txt_changed)
        self.pswd = Password('pswd', socketio, change_callback=self.txt_changed)
        self.rd = Radio('rd', socketio, click_callback=self.chk_clicked, title="My Radio")
        self.rng = Range('rng', socketio, min=0, max=100, change_callback=self.dt_changed)
        self.rst = Reset('rst', socketio, title='Cancel', click_callback=self.btn_clicked)
        self.srch = Search('srch', socketio, change_callback=self.txt_changed)
        self.sbmt = Submit('sbmt', socketio, title='Save', click_callback=self.btn_clicked)
        self.tel = Telephone('tel', socketio, change_callback=self.txt_changed)
        self.time = Time('time', socketio, change_callback=self.dt_changed)
        self.url = URL('url', socketio, change_callback=self.txt_changed)
        self.week = Week('week', socketio, change_callback=self.dt_changed)
        self.frm = Form('frm', socketio, use_fieldset=True, legend="My Form",
                        submit_callback=self.frm_submitted)
        self.frm_text = TextBox('frm_text', socketio)
        self.lbox = ListBox('lbox', socketio, change_callback=self.dd_changed, multiselect=True)
        self.lbox.add_option('abc', 'ABC', False)
        self.lbox.add_option('def', 'DEF', True)
        self.lbox.add_option('ghi', 'GHI', False)
        self.lbox.add_option('jkl', 'JKL', False)
        self.lbox.add_option('mno', 'MNO', False)
        self.lbox.add_option('pqr', 'PQR', False)
        self.lbl = Label('lbl', 'My Label', self.lbox, socketio)
        sg.add(Label('lb1', 'Button', self.bt, socketio))
        sg.add(self.bt)
        sg.add(Label('lb2', 'Button', self.bt1, socketio))
        sg.add(self.bt1)
        sg.add(Label('lb3', 'TextBox', self.txt, socketio))
        sg.add(self.txt)
        sg.add(Label('lb4', 'CheckBox', self.chk, socketio))
        sg.add(self.chk)
        sg.add(Label('lb5', 'Color', self.clr, socketio))
        sg.add(self.clr)
        sg.add(Label('lb6', 'Date', self.dt, socketio))
        sg.add(self.dt)
        sg.add(Label('lb7', 'DateTimeLocal', self.dtl, socketio))
        sg.add(self.dtl)
        sg.add(Label('lb8', 'Email', self.eml, socketio))
        sg.add(self.eml)
        sg.add(Label('lb9', 'File', self.fl, socketio))
        sg.add(self.fl)
        sg.add(Label('lb10', 'Image', self.img, socketio))
        sg.add(self.img)
        sg.add(Label('lb11', 'Month', self.mth, socketio))
        sg.add(self.mth)
        sg.add(Label('lb12', 'Number', self.num, socketio))
        sg.add(self.num)
        sg.add(Label('lb13', 'Password', self.pswd, socketio))
        sg.add(self.pswd)
        sg.add(Label('lb14', 'Radio', self.rd, socketio))
        sg.add(self.rd)
        sg.add(Label('lb15', 'Range', self.rng, socketio))
        sg.add(self.rng)
        sg.add(Label('lb16', 'Reset', self.rst, socketio))
        sg.add(self.rst)
        sg.add(Label('lb17', 'Search', self.srch, socketio))
        sg.add(self.srch)
        sg.add(Label('lb18', 'Submit', self.sbmt, socketio))
        sg.add(self.sbmt)
        sg.add(Label('lb19', 'Telephone', self.tel, socketio))
        sg.add(self.tel)
        sg.add(Label('lb20', 'Time', self.time, socketio))
        sg.add(self.time)
        sg.add(Label('lb21', 'URL', self.url, socketio))
        sg.add(self.url)
        sg.add(Label('lb22', 'Week', self.week, socketio))
        sg.add(self.week)
        sg.add(Label('lb23', 'Form', self.frm, socketio))
        self.frm.add(self.frm_text)
        sg.add(self.frm)
        sg.add(Label('lb24', 'ListBox', self.lbox, socketio))
        sg.add(self.lbox)
        sg.add(Label('lb25', 'Label', self.lbl, socketio))
        sg.add(self.lbl)
        pg.add(sg)
        return pg.render()

    def dd_changed(self, source, props):
        print("Dropdown Changed: " + str(props['value']))
        self.lbox.multiselect = not self.lbox.multiselect

    def frm_submitted(self, source, props):
        print("Form data: " + str(props['form']))

    def fl_changed(self, source, props):
        for fl in props['files']:
            print("Filename: " + str(fl.filename))

    def fl_clicked(self, source, props):
        print("File widget clicked")

    def dt_changed(self, source, props):
        print("Date changed: " + str(props['value']))

    def color_changed(self, source, props):
        print("Color changed to: " + str(props['value']))

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
