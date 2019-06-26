from flask import Flask
from widgets4py.base import Page
from widgets4py.basic import TextBox, Submit, Reset, Button  # ,Form
from widgets4py.basic import DropDown
from widgets4py.layouts import VerticalLayout

app = Flask(__name__)


class PageTest:

    def show_layout(self):
        pg = Page('myPage', 'My Page')
        vly = VerticalLayout("vlout")
        # frm = Form("myform", app=app, submit_callback=self.hello)
        txt = TextBox("firstName")
        btn = Button("btn", "Push Me!", app=app, onclick_callback=self.click)
        dd = DropDown("dd", options={'abc': ['ABC', False], 'def': ['DEF', True], 'ghi': ['GHI', False]})
        sub = Submit("submit", "Submit")
        rst = Reset("cancel", "Reset")
        vly.add(txt)
        vly.add(btn)
        vly.add(dd)
        vly.add(sub)
        vly.add(rst)
        pg.add(vly)
        # pg.add(frm)
        content = pg.render()
        return content

    def hello(self):
        print("Hello!")
        return "Hello!"

    def click(self):
        print("Btn pushed")
        return "success"


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
