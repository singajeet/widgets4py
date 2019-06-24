from flask import Flask
from widgets4py.base import Page
from widgets4py.layouts import GridLayout

app = Flask(__name__)


@app.route("/")
def show_layout():
    pg = Page('My Page')
    lay = GridLayout('Grid', 2, 2, row_ratio=['40%', '60%'], col_ratio=['30%', '70%'])
    pg.add(lay)
    content = pg.render()
    return content


# def local_func():
#     w = Page('My Widget')
#     lay = GridLayout('Grid', 2, 2)
#     w.add(lay)
#     print(w.render())


# if __name__ == "__main__":
#     local_func()
#     input()
#     local_func()
