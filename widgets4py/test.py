from flask import Flask
from widgets4py.base import Page
from widgets4py.basic import Form, TextBox, Submit, Reset

app = Flask(__name__)


class PageTest:

    def show_layout(self):
        pg = Page('myPage', 'My Page')
        frm = Form("myform", app=app, submit_callback=self.hello)
        txt = TextBox("firstName", disabled=True)
        sub = Submit("submit", "Submit")
        rst = Reset("cancel", "Reset")
        frm.add(txt)
        frm.add(sub)
        frm.add(rst)
        pg.add(frm)
        content = pg.render()
        return content

    def hello(self):
        print("Hello!")
        return "Hello!"


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
