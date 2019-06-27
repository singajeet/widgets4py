from flask import Flask
from widgets4py.base import Page
from widgets4py.basic import TextBox, Submit, Reset, Form, Label
from widgets4py.layouts import SimpleGridLayout


app = Flask(__name__)


class PageTest:

    _txt = None

    def show_layout(self):
        pg = Page('myPage', 'My Page')
        sg = SimpleGridLayout("Grid", 2, 2)
        frm = Form("myform", app=app, submit_callback=self.hello)
        self._txt = TextBox("firstName", app=app, onchange_callback=self.txt_change)
        lbl = Label('lbl', 'First Name', self._txt)
        sub = Submit("submit", "Submit")
        rst = Reset("cancel", "Reset")
        sg.add(lbl)
        sg.add(self._txt)
        sg.add(sub)
        sg.add(rst)
        frm.add(sg)
        pg.add(frm)
        content = pg.render()
        return content

    def hello(self):
        self._txt.set_text("My Text")
        print("Hello!")
        return "Hello!"

    def click(self):
        print("Btn pushed")
        return "success"

    def txt_change(self):
        print('Text changed')
        return "Text Change Triggred!"


p = PageTest()
app.add_url_rule('/', 'index', p.show_layout)
# def local_func():
#     w = Page('My Widget')
#     lay = GridLayout('Grid', 2, 2)
#     w.add(lay)
#     print(w.render())


# if __name__ == "__main__":
#     local_func()
#     input()
#     local_func()
