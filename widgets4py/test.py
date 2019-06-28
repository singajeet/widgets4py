from flask import Flask
from widgets4py.base import Page
from widgets4py.layouts import SimpleGridLayout
from widgets4py.ajax import Button


app = Flask(__name__)


class PageTest:

    _txt = None
    btn = None

    def show_layout(self):
        pg = Page('myPage', 'My Page')
        sg = SimpleGridLayout("Grid", 2, 2)
        self.btn = Button('btn', 'Push', app=app, onclick_callback=self.click)
        btn1 = Button('btn1', 'Pop', app=app, onclick_callback=self.hello)
        sg.add(self.btn)
        sg.add(btn1)
        pg.add(sg)
        content = pg.render()
        return content

    def hello(self):
        print("Hello!")
        return "Hello!"

    def click(self):
        self.btn.set_title("New Title")
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
