import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
# from widgets4py.layouts import SimpleGridLayout
from widgets4py.app_ui import TextBox  # , Button, CheckBox, Color, Date
# from widgets4py.app_ui import DateTimeLocal, Email, File, Image, Month
# from widgets4py.app_ui import Number, Password, Radio, Range
from widgets4py.app_ui import Form, Label, DropDown
from multiprocessing import Process


app = Flask(__name__)


class PageTest:

    txt = None
    # btn = None
    # btn1 = None
    # clr = None
    # chk = None
    # dt = None
    # dtl = None
    # eml = None
    # fl = None
    # img = None
    # mth = None
    # num = None
    # passwd = None
    # rd = None
    # rng = None
    lbl1 = None
    lbl2 = None
    dd = None
    frm = None

    def show_layout(self):
        pg = Page('myPage', 'My Page')
        self.frm = Form('frm', app=app, submit_callback=self.form_submitted)
        # sg = SimpleGridLayout("Grid", 8, 2)
        # self.btn = Button('btn', 'Push', app=app, onclick_callback=self.change_btn_title)
        # self.btn1 = Button('btn1', 'Populate', app=app, onclick_callback=self.populate_text)
        self.txt = TextBox('txt', app=app, onchange_callback=self.text_changed)
        # self.chk = CheckBox('chk', "Checkbox text", app=app, onclick_callback=self.checkbox_clicked)
        # self.clr = Color('clr', app=app, onchange_callback=self.color_changed)
        # self.dt = Date('dt', min="2019-01-01", max="2020-12-31", app=app, onchange_callback=self.date_changed)
        # self.dtl = DateTimeLocal('dtl', app=app, onchange_callback=self.datetime_changed)
        # self.eml = Email('eml', app=app, onchange_callback=self.email_changed)
        # self.fl = File('fl', app=app, onchange_callback=self.file_changed)
        # self.img = Image('img', url_for('static', filename='images.jpeg'), app=app,
        # onclick_callback=self.image_clicked)
        # self.mth = Month('mth', app=app, onchange_callback=self.month_changed)
        # self.num = Number('num', app=app, onchange_callback=self.numb_changed)
        # self.passwd = Password('passwd', app=app, onchange_callback=self.pass_changed)
        # self.rd = Radio('rd', "Radio Text", app=app, onclick_callback=self.radio_clicked)
        # self.rng = Range('rng', app=app, onchange_callback=self.range_changed)
        # sg.add(self.btn)
        # sg.add(self.btn1)
        # sg.add(self.txt)
        # sg.add(self.chk)
        # sg.add(self.clr)
        # sg.add(self.dt)
        # sg.add(self.dtl)
        # sg.add(self.eml)
        # sg.add(self.fl)
        # sg.add(self.img)
        # sg.add(self.mth)
        # sg.add(self.num)
        # sg.add(self.passwd)
        # sg.add(self.rd)
        # sg.add(self.rng)
        # pg.add(sg)
        self.lbl1 = Label('lbl1', 'TextBox Label:', self.txt)
        self.dd = DropDown('dd', app=app, onchange_callback=self.dd_changed)
        self.dd.add_option('a', 'A', False)
        self.dd.add_option('b', 'B', False)
        self.dd.add_option('c', 'C', False)
        self.lbl2 = Label('lbl2', 'DropDown Label:', self.dd, app=app, onclick_callback=self.lbl_clicked)
        self.frm.add(self.lbl1)
        self.frm.add(self.txt)
        self.frm.add(self.lbl2)
        self.frm.add(self.dd)
        pg.add(self.frm)
        content = pg.render()
        return content

    def lbl_clicked(self):
        print("Label 2 clicked")
        return "success"

    def dd_changed(self):
        print("DD Changed")
        return "success"

    def form_submitted(self):
        print("Form Submitted Successfully!")
        print("Field Count: " + str(self.frm.get_submitted_form_data().__len__()))
        data = self.frm.get_submitted_form_data()
        for fld in data:
            print(str(fld) + " = " + data.get(fld))
        return "success"

    def range_changed(self):
        print("Range Changed: " + self.rng.get_value())
        return "success"

    def radio_clicked(self):
        print("Radio clicked: " + self.rd.get_checked())
        return "success"

    def pass_changed(self):
        print("Password Changed: " + self.passwd.get_password())
        return "success"

    def numb_changed(self):
        print("Number Changed: " + self.num.get_number())
        return "success"

    def month_changed(self):
        print("Month Changed")
        return "success"

    def image_clicked(self):
        print("Image Clcked!")
        return "success"

    def file_changed(self):
        print("File changed")
        return "success"

    def email_changed(self):
        print("Email Changed!")
        print("Email: " + self.eml.get_text())
        return "success"

    def datetime_changed(self):
        print("Datetime changed")
        print("DateTime: " + self.dtl.get_value())
        return "success"

    def date_changed(self):
        print("Date Changed!")
        print("Date: " + self.dt.get_value())
        return "success"

    def color_changed(self):
        print("Color changed!")
        print("Color: " + self.clr.get_value())
        return "success"

    def checkbox_clicked(self):
        print("Checkbox clicked!")
        return "success"

    def populate_text(self):
        self.txt.set_text("Hello!")
        print("Text Populated!")
        return "success"

    def change_btn_title(self):
        self.btn.set_title("New Title")
        print("Btn title changed!")
        return "success"

    def text_changed(self):
        print("Text Changed:" + self.txt.get_text())
        # if self.txt.get_text() == "" or self.txt.get_text() is None:
        #     self.btn1.set_title('Populate')
        # else:
        #     self.btn1.set_title('Clear')
        return "Text Change Triggred!"


def start_app():
    p = PageTest()
    app.add_url_rule('/', 'index', p.show_layout)
    app.run(host='127.0.0.1', port=5000)


def start_web_view():
    webview.create_window("My Application", "http://localhost:5000", resizable=True)


if __name__ == "__main__":
    app_proc = Process(target=start_app)
    web_app = Process(target=start_web_view)
    app_proc.start()
    web_app.start()
    app_proc.join()
    web_app.join()
