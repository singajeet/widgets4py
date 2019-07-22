import os
import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
from multiprocessing import Process
from widgets4py.w2ui.ui import Form, FormFieldAlpha, FormFieldCheckbox, FormFieldDate
from widgets4py.w2ui.ui import FormFieldEnum, FormFieldFloat, FormFieldInt, FormFieldList
from widgets4py.w2ui.ui import FormFieldRadio, FormFieldSelect, FormFieldText, FormFieldTextArea


app = Flask(__name__)


class W2UIPage:

    pg = None
    form = None
    ffa = None
    ffc = None
    ffd = None
    ffe = None
    fff = None
    ffi = None
    ffl = None
    ffr = None
    ffs = None
    fft = None
    ffta = None

    def show_layout(self):
        self.pg = Page('pg', 'Forms')
        self.form = Form('form', header="Form Example", submit_callback=self.form_submitted, app=app)
        self.ffa = FormFieldAlpha('ffa', caption='AlphaNumeric:')
        self.ffc = FormFieldCheckbox('ffc', caption="CheckBox:")
        self.ffd = FormFieldDate('ffd', caption="Date:")
        self.ffe = FormFieldEnum('ffe', caption="Enum:", items=['ABC', 'DEF', 'GHI'], options=True)
        self.fff = FormFieldFloat('fff', caption="Float:")
        self.ffi = FormFieldInt('ffi', caption="Int:")
        self.ffl = FormFieldList('ffl', caption="List:", items=['ABC', 'DEF', 'GHI'], options=True)
        self.ffr = FormFieldRadio('ffr', caption="Radio:", items=['ABC', 'DEF'], options=True)
        self.ffs = FormFieldSelect('ffs', caption="Select:", items=['ABC', 'DEF', 'GHI'], options=True)
        self.fft = FormFieldText('fft', caption="Text:")
        self.ffta = FormFieldTextArea('ffta', caption="TextArea:")
        self.form.add(self.ffa)
        self.form.add(self.ffc)
        self.form.add(self.ffd)
        self.form.add(self.ffe)
        self.form.add(self.fff)
        self.form.add(self.ffi)
        self.form.add(self.ffl)
        self.form.add(self.ffr)
        self.form.add(self.ffs)
        self.form.add(self.fft)
        self.form.add(self.ffta)
        self.pg.add(self.form)
        return self.pg.render()

    def form_submitted(self, form_data):
        print("Form Data:" + str(form_data))


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
