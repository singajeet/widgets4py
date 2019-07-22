import os
import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
from multiprocessing import Process
from widgets4py.w2ui.ui import SidebarNode, Sidebar


app = Flask(__name__)


class W2UIPage:

    pg = None
    sb = None
    sb_node1 = None
    sb_node11 = None
    sb_node12 = None
    sb_node13 = None
    sb_node2 = None
    sb_node21 = None
    sb_node22 = None
    sb_node23 = None

    def show_layout(self):
        self.pg = Page('myPage', 'My Page')
        self.sb = Sidebar('sb', app=app, topHTML="Top Conttent", bottomHTML="Bottom Content")
        self.sb.add_style("height", "500px")
        self.sb.add_style("width", "200px")
        self.sb_node1 = SidebarNode('sb_node1', 'Node 1')
        self.sb_node11 = SidebarNode('sb_node11', 'Node 11')
        self.sb_node12 = SidebarNode('sb_node12', 'Node 12')
        self.sb_node13 = SidebarNode('sb_node13', 'Node 13')
        self.sb_node1.add(self.sb_node11)
        self.sb_node1.add(self.sb_node12)
        self.sb_node1.add(self.sb_node13)
        self.sb_node2 = SidebarNode('sb_node2', 'Node 2')
        self.sb_node21 = SidebarNode('sb_node21', 'Node 21')
        self.sb_node22 = SidebarNode('sb_node22', 'Node 22')
        self.sb_node23 = SidebarNode('sb_node23', 'Node 23')
        self.sb_node2.add(self.sb_node21)
        self.sb_node2.add(self.sb_node22)
        self.sb_node2.add(self.sb_node23)
        self.sb.add(self.sb_node1)
        self.sb.add(self.sb_node2)
        self.pg.add(self.sb)
        return self.pg.render()


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
