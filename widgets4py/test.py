from flask import Flask
from widgets4py.base import Page
from widgets4py.layouts import GridLayout
from widgets4py.basic import Button

app = Flask(__name__)


class PageTest:

    def show_layout(self):
        pg = Page('My Page')
        lay = GridLayout('Grid', 2, 2, row_ratio=['40%', '60%'], col_ratio=['30%', '70%'])
        bt = Button('my btn')
        lay.add(0, 0, bt)
        pg.add(lay)
        content = pg.render()
        return content


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
