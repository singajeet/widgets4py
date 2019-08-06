from widgets4py.base import Page
from widgets4py.websocket.jqmobile.ui import MobilePage, Button, ButtonStyle, FormButton
from widgets4py.websocket.jqmobile.ui import CheckBox, Radio, Collapsible
from widgets4py.websocket.jqmobile.ui import CollapsibleSet, ControlGroup, FlipSwitch
from widgets4py.websocket.jqmobile.ui import GridLayout, SectionLayout
from widgets4py.websocket.jqmobile.ui import ListItem, ListView, NavBar, Panel, Popup, HTML, RangeSlider
from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)


class MobileExample:

    _pg = None
    _mpg = None

    def show_layout(self):
        self._pg = Page('pg', 'Mobile Example')
        self._mpg1 = MobilePage('mpg1', 'Page1 Example', socketio, footer_title="Footer", click_callback=self.pg_clicked)  # noqa
        self._mpg2 = MobilePage('mpg2', 'Page2 Example', socketio, footer_title="Dialog Footer", is_dialog=True)  # noqa
        self._btn = Button('btn', socketio, btn_styles=[ButtonStyle.ROUND_CORNERS, ButtonStyle.ICON_LEFT],
                           title="My Button", icon='ui-icon-delete', click_callback=self.btn_clicked, href='#mpg2')  # noqa
        self._btn1 = FormButton('btn1', socketio, title="Form Button", icon='ui-icon-delete',
                                btn_styles=[ButtonStyle.ROUND_CORNERS, ButtonStyle.ICON_LEFT],
                                click_callback=self.btn_clicked)
        self._chkbox = CheckBox('chkbox', socketio, is_group=True, orientation="vertical",
                                icon_position="right", legend="My Checkboxes",
                                click_callback=self.chk_clicked)
        self._chkbox.add_item('item1', 'Item1')
        self._chkbox.add_item('item2', 'Item2')
        self._chkbox.add_item('item3', 'Item3')
        self._chkbox.add_item('item4', 'Item4')
        self._rd = Radio('rd', socketio, is_group=True, orientation="vertical",
                         legend="My RadioButtons",
                         click_callback=self.chk_clicked)
        self._rd.add_item('rd_item1', 'RadioItem1')
        self._rd.add_item('rd_item2', 'RadioItem2')
        self._rd.add_item('rd_item3', 'RadioItem3')
        self._rd.add_item('rd_item4', 'RadioItem4')
        self._ctrl_gp = ControlGroup('ctrl_gp', socketio)
        self._ctrl_gp.add(self._rd)
        self._clsp1 = Collapsible('clsp1', 'My Collapsible1', socketio, collapse_callback=self.clsp_clicked)
        self._clsp2 = Collapsible('clsp2', 'My Collapsible2', socketio, collapse_callback=self.clsp_clicked)
        self._clsp3 = Collapsible('clsp3', 'My Collapsible3', socketio, collapse_callback=self.clsp_clicked)
        self._clsp = CollapsibleSet('clsp', '', socketio, use_filter=True)
        self._fs = FlipSwitch('fs', socketio, on_text="Light", off_text="Dark",
                              change_callback=self.fs_changed)
        self._clsp.add(self._clsp1)
        self._clsp.add(self._clsp2)
        self._clsp.add(self._clsp3)
        self._grid = GridLayout('grid', 4)
        self._grid.add(Button('gb1', socketio, title="Btn1"))
        self._grid.add(Button('gb2', socketio, title="Btn2"))
        self._grid.add(Button('gb3', socketio, title="Btn3"))
        self._grid.add(Button('gb4', socketio, title="Btn4"))
        self._pnl_html = HTML('pnl_html', '<h2>My Panel</h2><br>This is a standard left panel with close button')
        self._pnl = Panel('pnl', socketio, display='overlay', show_close_btn=True,
                          before_close_callback=self.before_panel_closed, child_widgets=[self._pnl_html])
        self._sl = SectionLayout('sl', 'My Section', header_corners=True, body_corners=True, body_theme='a')
        self._sl.add(Button('slb', socketio, title='Button', href='#pnl'))
        self._lv = ListView('lv', socketio, is_filterable=True)
        self._li1 = ListItem('li1', 'ListItem1', socketio, click_callback=self.li_clicked)
        self._li2 = ListItem('li2', 'ListItem2', socketio, click_callback=self.li_clicked)
        self._li3 = ListItem('li3', 'ListItem3', socketio, click_callback=self.li_clicked)
        self._li4 = ListItem('li4', 'ListItem4', socketio, click_callback=self.li_clicked)
        self._lv.add(self._li1)
        self._lv.add(self._li2)
        self._lv.add(self._li3)
        self._lv.add(self._li4)
        self._nb = NavBar('nb', socketio, click_callback=self.nb_clicked)
        self._nb.add_item('nb1', 'NB1', True, href='#pop', data_rel='popup')
        self._nb.add_item('nb2', 'NB2', False)
        self._nb.add_item('nb3', 'NB3', False)
        self._nb.add_item('nb4', 'NB4', False)
        self._nb.add_item('nb5', 'NB5', False)
        self._pop_html = HTML('pop_html', '<center><h4>My Popup</h4></center>This is an popup with a HTML child widget')
        self._pop = Popup('pop', socketio, child_widgets=[self._pop_html])
        self._rng = RangeSlider('rng', socketio, 'Title1', 'Title2')
        self._mpg1.add(self._btn)
        self._mpg1.add(self._btn1)
        self._mpg1.add(self._chkbox)
        self._mpg1.add(self._ctrl_gp)
        self._mpg1.add(self._clsp)
        self._mpg1.add(self._fs)
        self._mpg1.add(self._grid)
        self._mpg1.add(self._sl)
        self._mpg1.add(self._lv)
        self._mpg1.add(self._nb)
        self._mpg1.add_panel(self._pnl)
        self._mpg1.add(self._pop)
        self._mpg1.add(self._rng)
        self._pg.add(self._mpg1)
        self._pg.add(self._mpg2)
        return self._pg.render()

    def before_panel_closed(self, source, props):
        print("Before Panel Closed: " + source + ", Props: " + str(props))

    def pg_clicked(self, source, props):
        print("Mobile Page Clicked: " + source + ", Props:" + str(props))

    def nb_clicked(self, source, props):
        print("NavBar clicked: " + source + ", Props: " + str(props))

    def lv_clicked(self, source, props):
        print("List view clicked: " + source + ", Props: " + str(props))

    def li_clicked(self, source, props):
        print("List Item clicked: " + source + ", Props: " + str(props))

    def fs_changed(self, source, props):
        print("FlipSwitch Changed: " + source + ", Props:" + str(props))

    def clsp_clicked(self, source, props):
        print("Collapsible closed! Source: " + source + ", Props: " + str(props))
        # self._fs._is_checked = not self._fs._is_checked

    def chk_clicked(self, source, status, items):
        print("Check Clicked: " + source + ", " + str(status))

    def btn_clicked(self, source, props):
        print("Button clicked: " + source + ", Props: " + str(props))
        self._clsp1.is_collapsed = not self._clsp1.is_collapsed
        if self._btn.icon == 'ui-icon-delete':
            self._btn.icon = 'ui-icon-alert'
            self._btn.remove_style(ButtonStyle.ICON_LEFT)
            self._btn.add_style(ButtonStyle.ICON_RIGHT)
        else:
            self._btn.remove_style(ButtonStyle.ICON_RIGHT)
            self._btn.add_style(ButtonStyle.ICON_LEFT)
            self._btn.icon = 'ui-icon-delete'


def start_app():
    p = MobileExample()
    app.add_url_rule('/', 'index', p.show_layout)
    # socketio.on_namespace(p.bt)
    socketio.run(app, debug=True)


if __name__ == '__main__':
    start_app()
