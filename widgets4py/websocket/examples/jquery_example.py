from widgets4py.base import Page
from flask import Flask
from flask_socketio import SocketIO
from widgets4py.websocket.jquery.ui import Section, Accordion, RadioButtonGroup, CheckBoxGroup, DialogBox
from widgets4py.websocket.jquery.ui import DialogTypes, MenuItem, Menu, SubMenu, MenuTypes, Slider, Spinner
from widgets4py.websocket.jquery.ui import TabSection, Tab
from widgets4py.layouts import SimpleGridLayout


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)


class PageTest:
    _pg = None

    def show_layout(self):
        self._pg = Page('pg', 'JQuery UI Demo')
        self._sg = SimpleGridLayout('sg', 25, 1)
        self._sec1 = Section('sec1', 'Section 1', socketio)
        self._sec2 = Section('sec2', 'Section 2', socketio)
        self._sec3 = Section('sec3', 'Section 3', socketio)
        self._sec4 = Section('sec4', 'Section 4', socketio)
        self._accd = Accordion('accd', socketio)
        self._accd.add(self._sec1)
        self._accd.add(self._sec2)
        self._accd.add(self._sec3)
        self._accd.add(self._sec4)
        self._sg.add(self._accd)
        self._rbg = RadioButtonGroup('rbg', 'Radio Buttons', socketio, onclick_callback=self.rbg_clicked)
        self._rbg.add_item('rd1', 'Radio 1', False)
        self._rbg.add_item('rd2', 'Radio 2', False)
        self._rbg.add_item('rd3', 'Radio 3', False)
        self._rbg.add_item('rd4', 'Radio 4', False)
        self._sg.add(self._rbg)
        self._cbg = CheckBoxGroup('cbg', 'CheckBox Group', socketio, onclick_callback=self.cbg_clicked)
        self._cbg.add_item('cb1', 'Checkbox 1', False)
        self._cbg.add_item('cb2', 'Checkbox 2', False)
        self._cbg.add_item('cb3', 'Checkbox 3', False)
        self._cbg.add_item('cb4', 'Checkbox 4', False)
        self._sg.add(self._cbg)
        self._dlg = DialogBox('dlg', 'My Dialog', DialogTypes.MODAL_CONFIRM, socketio)
        self.menu = Menu('menu', socketio, menu_type=MenuTypes.HORIZONTAL)
        self.m_menu_itm1 = MenuItem('m_menu_itm1', 'Item1', socketio,
                                    menu_clicked_callback=self.menu_clicked, icon='ui-icon-disk')
        self.m_menu_itm2 = MenuItem('m_menu_itm2', 'Item2', socketio,
                                    menu_clicked_callback=self.menu_clicked, icon='ui-icon-zoomin')
        self.m_submenu_itm3 = SubMenu('m_submenu_itm3', 'Item3', socketio)
        self.m_menu_itm4 = MenuItem('m_menu_itm4', 'Item4', socketio, menu_clicked_callback=self.menu_clicked)
        self.sm_menu_itm1 = MenuItem('sm_menu_itm1', 'SubItem1', socketio,
                                     menu_clicked_callback=self.menu_clicked, icon='ui-icon-play')
        self.sm_menu_itm2 = MenuItem('sm_menu_itm2', 'SubItem2', socketio,
                                     menu_clicked_callback=self.menu_clicked, icon='ui-icon-stop')
        self.m_submenu_itm3.add(self.sm_menu_itm1)
        self.m_submenu_itm3.add(self.sm_menu_itm2)
        self.menu.add(self.m_menu_itm1)
        self.menu.add(self.m_menu_itm2)
        self.menu.add(self.m_submenu_itm3)
        self.menu.add(self.m_menu_itm4)
        self._pg.add(self.menu)
        self._slide = Slider('slide', socketio, onclick_callback=self.slider_clicked, onchange_callback=self.slider_clicked)
        self._sg.add(self._slide)
        self._spin = Spinner('spin', socketio, onchange_callback=self.spin_changed)
        self._sg.add(self._spin)
        self._tab1 = TabSection('tab1', 'Tab1')
        self._tab2 = TabSection('tab2', 'Tab2')
        self._tab3 = TabSection('tab3', 'Tab3')
        self._tab4 = TabSection('tab4', 'Tab4')
        self._tab = Tab('tab', socketio, tab_activated_callback=self.tab_changed)
        self._tab.add(self._tab1)
        self._tab.add(self._tab2)
        self._tab.add(self._tab3)
        self._tab.add(self._tab4)
        self._sg.add(self._tab)
        self._pg.add(self._sg)
        self._pg.add(self._dlg)
        return self._pg.render()

    def tab_changed(self, source, props):
        print("Tab activated: " + source + ", Props: " + str(props))

    def spin_changed(self, source, props):
        print("Spinner Changed: " + source + ", Props: " + str(props))

    def slider_clicked(self, source, props):
        print("Slider Clicked: " + source + ", Props: " + str(props))

    def menu_clicked(self, source, props):
        print("Menu clicked: " + source + ", Props: " + str(props))

    def cbg_clicked(self, source, props):
        print("CBG Clicked: " + source + ", Props: " + str(props))

    def rbg_clicked(self, source, props):
        print("RBG Clicked: " + source + ", Props: " + str(props))
        if self._dlg.is_dialog_open:
            self._dlg.close()
        else:
            self._dlg.open()

def start_app():
    p = PageTest()
    app.add_url_rule('/', 'index', p.show_layout)
    # socketio.on_namespace(p.bt)
    socketio.run(app, debug=True)


if __name__ == '__main__':
    start_app()
