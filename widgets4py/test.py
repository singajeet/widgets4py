from flask import Flask
from widgets4py.layouts import GridLayout
from widgets4py.base import Page

app = Flask(__name__)


@app.route("/")
def show_layout():
    pg = Page('My Page')
    lay = GridLayout('Grid', 2, 2)
    pg.add(lay)
    content = pg.render()
    return content
