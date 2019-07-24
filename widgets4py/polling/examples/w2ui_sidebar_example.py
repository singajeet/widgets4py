import os
import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
from multiprocessing import Process
from widgets4py.polling.w2ui.ui import SidebarNode, Sidebar


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
    actions = None
    add_item = None
    ins_item = None
    rm_item = None
    shw_item = None
    hide_item = None
    enb_item = None
    dsbl_item = None
    expnd_item = None
    clsp_item = None
    sel_item = None
    unsel_item = None
    clk_item = None

    def show_layout(self):
        self.pg = Page('myPage', 'My Page')
        self.sb = Sidebar('sb', app=app, topHTML="Top Conttent", bottomHTML="Bottom Content",
                          onclick_callback=self.sidebar_clicked)
        self.sb.add_style("height", "500px")
        self.sb.add_style("width", "200px")
        self.actions = SidebarNode('actions', 'Actions')
        self.add_item = SidebarNode('add_item', 'Add')
        self.ins_item = SidebarNode('ins_item', 'Insert')
        self.rm_item = SidebarNode('rm_item', 'Remove')
        self.shw_item = SidebarNode('shw_item', 'Show')
        self.hide_item = SidebarNode('hide_item', 'Hide')
        self.enb_item = SidebarNode('enb_item', 'Enable')
        self.dsbl_item = SidebarNode('dsbl_item', 'Disable')
        self.expnd_item = SidebarNode('expnd_item', 'Expand')
        self.clsp_item = SidebarNode('clsp_item', 'Collapse')
        self.sel_item = SidebarNode('sel_item', 'Select')
        self.unsel_item = SidebarNode('unsel_item', 'Unselect')
        self.clk_item = SidebarNode('clk_item', 'Click')
        self.actions.add(self.add_item)
        self.actions.add(self.ins_item)
        self.actions.add(self.rm_item)
        self.actions.add(self.shw_item)
        self.actions.add(self.hide_item)
        self.actions.add(self.enb_item)
        self.actions.add(self.dsbl_item)
        self.actions.add(self.expnd_item)
        self.actions.add(self.clsp_item)
        self.actions.add(self.sel_item)
        self.actions.add(self.unsel_item)
        self.actions.add(self.clk_item)
        self.sb.add(self.actions)
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

    def sidebar_clicked(self):  # noqa
        if self.sb.clicked_item == 'add_item':
            new_item = SidebarNode('new_item', 'New Item')
            self.sb.add_items([new_item])
        if self.sb.clicked_item == 'ins_item':
            new_ins_item = SidebarNode('new_ins_item', 'New Inserted Item')
            self.sb.insert_items([new_ins_item], 'sb_node1')
        if self.sb.clicked_item == 'rm_item':
            self.sb.remove_items(['new_ins_item'])
        if self.sb.clicked_item == 'shw_item':
            self.sb.show_items(['new_item'])
        if self.sb.clicked_item == 'hide_item':
            self.sb.hide_items(['new_item'])
        if self.sb.clicked_item == 'enb_item':
            self.sb.enable_item('new_item')
        if self.sb.clicked_item == 'dsbl_item':
            self.sb.disable_item('new_item')
        if self.sb.clicked_item == 'expnd_item':
            self.sb.expand_item('sb_node2')
        if self.sb.clicked_item == 'clsp_item':
            self.sb.collapse_item('sb_node2')
        if self.sb.clicked_item == 'sel_item':
            self.sb.select_item('new_item')
        if self.sb.clicked_item == 'unsel_item':
            self.sb.unselect_item('new_item')
        if self.sb.clicked_item == 'clk_item':
            self.sb.click_item('new_item')


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
