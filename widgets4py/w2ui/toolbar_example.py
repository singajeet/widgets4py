import os
import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
from widgets4py.w2ui.ui import Toolbar, ToolbarButton, ToolbarCheck
from widgets4py.w2ui.ui import ToolbarHTML, ToolbarMenu, ToolbarMenuCheck
from widgets4py.w2ui.ui import ToolbarMenuRadio, ToolbarRadio, ToolbarSeparator
from widgets4py.w2ui.ui import ToolbarDropDown, ToolbarSpacer
from multiprocessing import Process


app = Flask(__name__)


class W2UIPage:

    pg = None
    toolbar = None
    tool_btn = None
    tool_chk = None
    tool_html = None
    tool_menu = None
    tool_menu_chk = None
    tool_menu_rd = None
    tool_rd = None
    tool_sep = None
    tool_dd = None
    tool_spacer = None

    def show_layout(self):
        self.pg = Page('myPage', 'My Page')
        self.toolbar = Toolbar('toolbar', app=app, onclick_callback=self._toolbar_clicked)
        self.tool_btn = ToolbarButton('toolbtn', 'Button')
        self.tool_chk = ToolbarCheck('tool_chk', 'Check')
        self.tool_dd = ToolbarDropDown('tool_dd', 'My DropDown content', 'DropDown')
        self.tool_html = ToolbarHTML('tool_html', '<input type=text />', 'Html')
        self.tool_menu = ToolbarMenu('tool_menu', 'Actions')
        self.tool_menu.add_item('Add')
        self.tool_menu.add_item('Insert')
        self.tool_menu.add_item('Remove')
        self.tool_menu.add_item('Show')
        self.tool_menu.add_item('Hide')
        self.tool_menu.add_item('Enable')
        self.tool_menu.add_item('Disable')
        self.tool_menu_chk = ToolbarMenuCheck('tool_menu_chk', 'MenuCheck')
        self.tool_menu_chk.add_item('item1', 'Item1')
        self.tool_menu_chk.add_item('item2', 'Item2')
        self.tool_menu_rd = ToolbarMenuRadio('tool_menu_rd', 'MenuRadio')
        self.tool_menu_rd.add_item('item1', 'Item1')
        self.tool_menu_rd.add_item('item2', 'Item2')
        self.tool_rd = ToolbarRadio('tool_rd', 'Radio')
        self.tool_sep = ToolbarSeparator('tool_sep', 'Sep')
        self.tool_spacer = ToolbarSpacer('tool_spacer', 'Spac')
        self.toolbar.add(self.tool_btn)
        self.toolbar.add(self.tool_chk)
        self.toolbar.add(self.tool_dd)
        self.toolbar.add(self.tool_html)
        self.toolbar.add(self.tool_menu)
        self.toolbar.add(self.tool_menu_chk)
        self.toolbar.add(self.tool_menu_rd)
        self.toolbar.add(self.tool_rd)
        self.toolbar.add(self.tool_sep)
        self.toolbar.add(self.tool_spacer)
        self.pg.add(self.toolbar)
        content = self.pg.render()
        return content

    def _toolbar_clicked(self):
        menu = self.toolbar.clicked_item
        if str(menu).find(':') > 0:
            item = str(menu).split(':')[1]
            if item.upper() == 'ADD':
                new_btn = ToolbarButton('new_btn', 'New Button')
                self.toolbar.add_item(new_btn)
            if item.upper() == 'INSERT':
                new_ins_btn = ToolbarButton('new_ins_btn', 'New Insert Button')
                self.toolbar.insert_item(new_ins_btn, 'tool_btn')
            if item.upper() == 'REMOVE':
                self.toolbar.remove_item('new_ins_btn')
            if item.upper() == 'HIDE':
                self.toolbar.hide_item('toolbtn')
            if item.upper() == 'SHOW':
                self.toolbar.show_item('toolbtn')
            if item.upper() == 'ENABLE':
                self.toolbar.enable_item('toolbtn')
            if item.upper() == 'DISABLE':
                self.toolbar.disable_item('toolbtn')


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
