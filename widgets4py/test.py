import os
import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
from widgets4py.layouts import SimpleGridLayout
# from widgets4py.html5.app_ui import TextBox, Button  # , CheckBox, Color, Date
# from widgets4py.html5.app_ui import DateTimeLocal, Email, File, Image, Month
# from widgets4py.html5.app_ui import Number, Password, Radio, Range
# from widgets4py.html5.app_ui import Form, Label, DropDown
# from widgets4py.jquery.ui import Accordion, Section, RadioButtonGroup
# from widgets4py.jquery.ui import CheckBoxGroup, DialogBox, DialogTypes
# from widgets4py.jquery.ui import Menu, MenuItem, SubMenu, MenuTypes, Slider, Spinner
# from widgets4py.jquery.ui import TabSection, Tab
# from widgets4py.w2ui.ui import GridColumn, GridColumnCollection
# from widgets4py.w2ui.ui import GridRecord, GridRecordCollection, Grid
# from widgets4py.w2ui.ui import Toolbar, ToolbarButton, ToolbarSeparator, ToolbarCheck
# from widgets4py.w2ui.ui import ToolbarRadio, ToolbarMenu, ToolbarMenuRadio
# from widgets4py.w2ui.ui import ToolbarMenuCheck, ToolbarDropDown, ToolbarHTML
# from widgets4py.w2ui.ui import Sidebar, SidebarNode
# from widgets4py.w2ui.ui import Form, FormFieldAlpha, FormFieldText, FormFieldDate
# from widgets4py.w2ui.ui import FormFieldList, FormFieldEnum, FormFieldSelect
# from widgets4py.w2ui.ui import Popup
from widgets4py.jstree.ui import JSTree, JSTreeNode, ContextMenuItem
from multiprocessing import Process


app = Flask(__name__)


class PageTest:

    # txt = None
    # btn = None
    # btn1 = None
    # clr = None
    # chk = None
    # dt = None
    # dtl = None
    # eml = None
    # fl = None
    # img = None
    # mth = None
    # num = None
    # passwd = None
    # rd = None
    # rng = None
    # lbl1 = None
    # lbl2 = None
    # dd = None
    # frm = None
    # sec1 = None
    # sec2 = None
    # acrd = None
    # rbg = None
    # rbg_items = {'rd1': ['Radio1', False],
    #              'rd2': ['Radio2', False],
    #              'rd3': ['Radio3', False]
    #              }
    # cbg = None
    # cbg_items = {'cb1': ['CheckBox1', False],
    #              'cb2': ['CheckBox2', False],
    #              'cb3': ['CheckBox3', False],
    #              }
    # dlg = None
    # dlg_btn = None
    # menu = None
    # m_menu_itm1 = None
    # m_menu_itm2 = None
    # m_submenu_item3 = None
    # m_menu_item4 = None
    # sm_menu_item1 = None
    # sm_menu_item2 = None
    # sld = None
    # spn = None
    # tab = None
    # tab_sec1 = None
    # tab_sec2 = None
    # g_col1 = None
    # g_col2 = None
    # g_column_coll = None
    # g_rec1 = None
    # g_rec2 = None
    # g_record_coll = None
    # grid = None
    # tool_btn1 = None
    # tool_sep = None
    # tool_btn2 = None
    # toolbar = None
    # tool_rd1 = None
    # tool_rd2 = None
    # tool_chk1 = None
    # tool_menu = None
    # tool_menu_rd = None
    # tool_menu_chk = None
    # tool_dd = None
    # tool_html = None
    # s_node1 = None
    # s_node11 = None
    # s_node12 = None
    # s_node13 = None
    # s_node2 = None
    # s_node21 = None
    # s_node211 = None
    # s_node212 = None
    # s_node213 = None
    # s_node22 = None
    # s_node23 = None
    # frm = None
    # frm_text = None
    # frm_alpha = None
    # frm_dt = None
    # frm_lst = None
    # frm_enm = None
    # frm_sel = None
    # pop = None
    tree = None
    node1 = None
    node2 = None
    node3 = None
    ctx_item1 = None
    ctx_item2 = None
    ctx_item21 = None
    ctx_item22 = None
    ctx_item3 = None

    def show_layout(self):
        pg = Page('myPage', 'My Page')
        self.ctx_item1 = ContextMenuItem('Item1', "function(item, ref, ele, pos){alert(item);}")
        self.ctx_item2 = ContextMenuItem('Item2', "function(item, ref, ele, pos){}")
        self.ctx_item21 = ContextMenuItem('Item2-1', "function(item, ref, ele, pos){}")
        self.ctx_item22 = ContextMenuItem('Item2-2', "function(item, ref, ele, pos){}")
        self.ctx_item2.add('Item2-1', self.ctx_item21)
        self.ctx_item2.add('Item2-2', self.ctx_item22)
        self.ctx_item3 = ContextMenuItem('Item3', "function(item, ref, ele, pos){}")
        self.tree = JSTree('tree', plugin_contextmenu=True, plugin_dnd=True, plugin_search=True)
        self.tree.add_ctx_menu_item('Item1', self.ctx_item1)
        self.tree.add_ctx_menu_item('Item2', self.ctx_item2)
        self.tree.add_ctx_menu_item('Item3', self.ctx_item3)
        self.node1 = JSTreeNode('node1', 'Node 1', is_opened=True)
        self.node2 = JSTreeNode('node2', 'Node 2')
        self.node3 = JSTreeNode('node3', 'Node 3')
        self.tree.add(self.node1)
        self.node1.add(self.node2)
        self.node1.add(self.node3)
        # self.pop = Popup('pop', 'Test Title', app=app,
        #                  buttons='<input type="button" onclick="w2popup.close();" value="Close" />',
        #                  show_max=True, show_close=True, modal=True,
        #                  body='<span>This message for you to show in popup widow!</span>')
        # self.frm_text = FormFieldText('frm_text', caption='Text Field', required=True)
        # self.frm_alpha = FormFieldAlpha('frm_alpha', caption='Alphanum Field')
        # self.frm_dt = FormFieldDate('frm_dt', caption='Date Field', required=True)
        # self.frm_lst = FormFieldList('frm_lst', caption='List Field', options=True, items=['abc', 'def', 'ghi'])
        # self.frm_enm = FormFieldEnum('frm_enm', caption='Enum Field', options=True, items=['abc', 'def', 'ghi'])
        # self.frm_sel = FormFieldSelect('frm_sel', caption='Select Field', options=True, items=['abc', 'def', 'ghi'])
        # self.frm = Form('frm', app=app, submit_callback=self.w2ui_form_submitted)
        # self.frm.add(self.frm_text)
        # self.frm.add(self.frm_alpha)
        # self.frm.add(self.frm_dt)
        # self.frm.add(self.frm_lst)
        # self.frm.add(self.frm_enm)
        # self.frm.add(self.frm_sel)
        # self.sidebar = Sidebar('sidebar', flatButton=True, app=app, onclick_callback=self.sidebar_clicked)
        # self.sidebar.add_style("height", "100%")
        # self.sidebar.add_style("width", "100%")
        # self.s_node1 = SidebarNode('s_node1', text='Level1', expanded=True, group=True)
        # self.s_node11 = SidebarNode('s_node11', text='Level1-1', is_leaf=True)
        # self.s_node12 = SidebarNode('s_node12', text='Level1-2', is_leaf=True)
        # self.s_node13 = SidebarNode('s_node13', text='Level1-3', is_leaf=True)
        # self.s_node2 = SidebarNode('s_node2', text='Level2', expanded=True, group=True)
        # self.s_node21 = SidebarNode('s_node21', text='Level2-1', expanded=True)
        # self.s_node211 = SidebarNode('s_node211', text='Level2-1-1', is_leaf=True)
        # self.s_node212 = SidebarNode('s_node212', text='Level2-1-2', is_leaf=True)
        # self.s_node213 = SidebarNode('s_node213', text='Level2-1-3', is_leaf=True)
        # self.s_node22 = SidebarNode('s_node22', text='Level2-2', is_leaf=True)
        # self.s_node23 = SidebarNode('s_node23', text='Level2-3', is_leaf=True)
        # self.s_node1.add(self.s_node11)
        # self.s_node1.add(self.s_node12)
        # self.s_node1.add(self.s_node13)
        # self.s_node2.add(self.s_node21)
        # self.s_node21.add(self.s_node211)
        # self.s_node21.add(self.s_node212)
        # self.s_node21.add(self.s_node213)
        # self.s_node2.add(self.s_node22)
        # self.s_node2.add(self.s_node23)
        # self.sidebar.add(self.s_node1)
        # self.sidebar.add(self.s_node2)
        # self.toolbar = Toolbar('MyBar', onclick_callback=self.toolbar_clicked, app=app)
        # self.tool_btn1 = ToolbarButton('tool_btn1', 'Button1', icon='fa-star')
        # self.tool_btn2 = ToolbarButton('tool_btn2', 'Button2', icon='fa-heart')
        # self.tool_sep = ToolbarSeparator('tool_sep', 'Sep')
        # self.tool_rd1 = ToolbarRadio('tool_rd1', 'Radio1', group='A')
        # self.tool_rd2 = ToolbarRadio('tool_rd2', 'Radio2', group='A')
        # self.tool_chk1 = ToolbarCheck('tool_chk1', 'Checkbox')
        # self.tool_menu = ToolbarMenu('tool_menu', 'Menu', count=2)
        # self.tool_menu.add_item('Item1', '', count=1)
        # self.tool_menu.add_item('Item2', '', count=1)
        # self.tool_menu_rd = ToolbarMenuRadio('tool_menu_rd', 'MenuRadio')
        # self.tool_menu_rd.add_item('rd1', 'Radio1')
        # self.tool_menu_rd.add_item('rd2', 'Radio2')
        # self.tool_menu_rd.add_item('rd3', 'Radio3')
        # self.tool_menu_chk = ToolbarMenuCheck('tool_menu_chk', 'MenuCheck')
        # self.tool_menu_chk.add_item('ck1', 'Check1')
        # self.tool_menu_chk.add_item('ck2', 'Check2')
        # self.tool_menu_chk.add_item('ck3', 'Check3')
        # self.tool_dd = ToolbarDropDown('tool_dd', "<p>My name is Singh...Ajeet Singh!!", "Drop")
        # self.tool_html = ToolbarHTML('tool_html', '<span>Name:</span><input type="text" id="smid" />', title='abc')
        # self.toolbar.add(self.tool_btn1)
        # self.toolbar.add(self.tool_sep)
        # self.toolbar.add(self.tool_btn2)
        # self.toolbar.add(self.tool_rd1)
        # self.toolbar.add(self.tool_rd2)
        # self.toolbar.add(self.tool_chk1)
        # self.toolbar.add(self.tool_menu)
        # self.toolbar.add(self.tool_menu_rd)
        # self.toolbar.add(self.tool_menu_chk)
        # self.toolbar.add(self.tool_dd)
        # self.toolbar.add(self.tool_html)
        # pg.add(self.toolbar)
        # self.g_col1 = GridColumn('fname', 'First Name', 50)
        # self.g_col2 = GridColumn('lname', 'Last Name', 50)
        # self.g_column_coll = GridColumnCollection()
        # self.g_column_coll.add(self.g_col1)
        # self.g_column_coll.add(self.g_col2)
        # self.g_rec1 = GridRecord()
        # self.g_rec1.add_cell("fname", "Ajeet")
        # self.g_rec1.add_cell("lname", "Singh")
        # self.g_rec2 = GridRecord()
        # self.g_rec2.add_cell("fname", "Armin")
        # self.g_rec2.add_cell("lname", "Kaur")
        # self.g_record_coll = GridRecordCollection()
        # self.g_record_coll.add(self.g_rec1)
        # self.g_record_coll.add(self.g_rec2)
        # self.grid = Grid('grid', 'My Table', self.g_column_coll, row_collection=self.g_record_coll,
        #                  toolbar=True, footer=True, line_numbers=True, select_column=True,
        #                  multi_select=True, app=app, toolbarAdd=True, toolbarDelete=True,
        #                  toolbarSave=True, toolbarEdit=True)
        # self.frm = Form('frm', app=app, submit_callback=self.form_submitted)
        sg = SimpleGridLayout("Grid", 1, 2, col_ratio=["20%", "80%"])
        sg.add_style("height", "500px")
        sg.add_style("width", "100%")
        sg.add(self.tree)
        # sg.add(self.sidebar)
        # sg.add(self.grid)
        # self.btn = Button('btn', 'Push', app=app, onclick_callback=self.change_btn_title)
        # self.btn1 = Button('btn1', 'Populate', app=app, onclick_callback=self.populate_text)
        # self.txt = TextBox('txt', app=app, onchange_callback=self.text_changed)
        # self.chk = CheckBox('chk', "Checkbox text", app=app, onclick_callback=self.checkbox_clicked)
        # self.clr = Color('clr', app=app, onchange_callback=self.color_changed)
        # self.dt = Date('dt', min="2019-01-01", max="2020-12-31", app=app, onchange_callback=self.date_changed)
        # self.dtl = DateTimeLocal('dtl', app=app, onchange_callback=self.datetime_changed)
        # self.eml = Email('eml', app=app, onchange_callback=self.email_changed)
        # self.fl = File('fl', app=app, onchange_callback=self.file_changed)
        # self.img = Image('img', url_for('static', filename='images.jpeg'), app=app,
        # onclick_callback=self.image_clicked)
        # self.mth = Month('mth', app=app, onchange_callback=self.month_changed)
        # self.num = Number('num', app=app, onchange_callback=self.numb_changed)
        # self.passwd = Password('passwd', app=app, onchange_callback=self.pass_changed)
        # self.rd = Radio('rd', "Radio Text", app=app, onclick_callback=self.radio_clicked)
        # self.rng = Range('rng', app=app, onchange_callback=self.range_changed)
        # sg.add(self.btn)
        # sg.add(self.btn1)
        # sg.add(self.txt)
        # sg.add(self.chk)
        # sg.add(self.clr)
        # sg.add(self.dt)
        # sg.add(self.dtl)
        # sg.add(self.eml)
        # sg.add(self.fl)
        # sg.add(self.img)
        # sg.add(self.mth)
        # sg.add(self.num)
        # sg.add(self.passwd)
        # sg.add(self.rd)
        # sg.add(self.rng)
        pg.add(sg)
        # self.lbl1 = Label('lbl1', 'TextBox Label:', self.txt)
        # self.dd = DropDown('dd', app=app, onchange_callback=self.dd_changed)
        # self.dd.add_option('a', 'A', False)
        # self.dd.add_option('b', 'B', False)
        # self.dd.add_option('c', 'C', False)
        # self.lbl2 = Label('lbl2', 'DropDown Label:', self.dd, app=app, onclick_callback=self.lbl_clicked)
        # self.frm.add(self.lbl1)
        # self.frm.add(self.txt)
        # self.frm.add(self.lbl2)
        # self.frm.add(self.dd)
        # pg.add(self.frm)
        # self.acrd = Accordion('acrd', collapsible=True)
        # self.sec1 = Section('sec1', 'Section1', app=app, onclick_callback=self.section_clicked)
        # self.sec2 = Section('sec2', 'Section2', app=app, onclick_callback=self.section_clicked)
        # self.acrd.add(self.sec1)
        # self.acrd.add(self.sec2)
        # self.rbg = RadioButtonGroup('rbg', "RadioBtn Group", self.rbg_items,
        #                             app=app, onclick_callback=self.rbg_clicked)
        # self.cbg = CheckBoxGroup('cbg', "CheckBox Group", self.cbg_items,
        #                          app=app, onclick_callback=self.cbg_clicked)
        # self.dlg = DialogBox('dlg', 'My Dialog', DialogTypes.MODAL_CONFIRM, app=app)
        # self.dlg_btn = Button('dlg_btn', "Open Dialog", app=app, onclick_callback=self.open_dialog)
        # pg.add(self.acrd)
        # pg.add(self.rbg)
        # pg.add(self.cbg)
        # pg.add(self.dlg)
        # pg.add(self.dlg_btn)
        # self.menu = Menu('menu', menu_type=MenuTypes.HORIZONTAL)
        # self.m_menu_itm1 = MenuItem('m_menu_itm1', 'Item1', app=app,
        #                             menu_clicked_callback=self.menu_clicked, icon='ui-icon-disk')
        # self.m_menu_itm2 = MenuItem('m_menu_itm2', 'Item2', app=app,
        #                             menu_clicked_callback=self.menu_clicked, icon='ui-icon-zoomin')
        # self.m_submenu_itm3 = SubMenu('m_submenu_itm3', 'Item3')
        # self.m_menu_itm4 = MenuItem('m_menu_itm4', 'Item4', app=app, menu_clicked_callback=self.menu_clicked)
        # self.sm_menu_itm1 = MenuItem('sm_menu_itm1', 'SubItem1', app=app,
        #                              menu_clicked_callback=self.menu_clicked, icon='ui-icon-play')
        # self.sm_menu_itm2 = MenuItem('sm_menu_itm2', 'SubItem2', app=app,
        #                              menu_clicked_callback=self.menu_clicked, icon='ui-icon-stop')
        # self.m_submenu_itm3.add(self.sm_menu_itm1)
        # self.m_submenu_itm3.add(self.sm_menu_itm2)
        # self.menu.add(self.m_menu_itm1)
        # self.menu.add(self.m_menu_itm2)
        # self.menu.add(self.m_submenu_itm3)
        # self.menu.add(self.m_menu_itm4)
        # pg.add(self.menu)
        # self.sld = Slider('sld', slider_changed_callback=self.slider_changed, app=app)
        # pg.add(self.sld)
        # self.spn = Spinner('spn', app=app, onchange_callback=self.spinner_changed, number_format="C")
        # pg.add(self.spn)
        # self.tab = Tab('tab', app=app, tab_activated_callback=self.tab_clicked)
        # self.tab_sec1 = TabSection('tab_sec1', 'Tab1')
        # self.tab_sec2 = TabSection('tab_sec2', 'Tab2')
        # self.tab.add(self.tab_sec1)
        # self.tab.add(self.tab_sec2)
        # pg.add(self.tab)
        # pg.add(self.frm)
        # pg.add(self.pop)
        content = pg.render()
        return content

    def w2ui_form_submitted(self, form):
        print("Form has been submitted with data: " + str(form))
        return "success"

    def sidebar_clicked(self):
        print("Sidebar clicked: " + self.sidebar.clicked_item)
        if self.sidebar.clicked_item == "s_node11":
            self.sidebar.collapse_item('s_node21')
        return "success"

    def toolbar_clicked(self):
        print("Toolbar clicked on item: " + self.toolbar.clicked_item)
        if self.toolbar.clicked_item == 'tool_btn1':
            self.toolbar.disable_item('tool_btn2')
        if self.toolbar.clicked_item == 'tool_btn2':
            self.pop.open()
        return "success"

    def tab_clicked(self):
        print("Tab clicked: " + self.tab.selected_index)
        return "success"

    def spinner_changed(self):
        print("Spinner Changed: " + self.spn.value)
        return "success"

    def slider_changed(self):
        print("Slider Changed: " + str(self.sld.get_value()))
        return "success"

    def menu_clicked(self):
        print("Menu clicked")
        self.m_menu_itm4.set_disabled(True)
        return "success"

    def open_dialog(self):
        print("Open dialog btn clicked")
        self.dlg.open()
        return "success"

    def cbg_clicked(self):
        print("CBG Clicked: " + str(self.cbg.get_value()))
        return "success"

    def rbg_clicked(self):
        print("RBG clicked: " + self.rbg.get_value())
        if self.rbg.get_value() == "rd3":
            self.rbg.set_disable("rd1", True)
        return "success"

    def section_clicked(self):
        print("Section clicked")
        return "success"

    def lbl_clicked(self):
        print("Label 2 clicked")
        return "success"

    def dd_changed(self):
        print("DD Changed")
        return "success"

    def form_submitted(self):
        print("Form Submitted Successfully!")
        print("Field Count: " + str(self.frm.get_submitted_form_data().__len__()))
        data = self.frm.get_submitted_form_data()
        for fld in data:
            print(str(fld) + " = " + data.get(fld))
        return "success"

    def range_changed(self):
        print("Range Changed: " + self.rng.get_value())
        return "success"

    def radio_clicked(self):
        print("Radio clicked: " + self.rd.get_checked())
        return "success"

    def pass_changed(self):
        print("Password Changed: " + self.passwd.get_password())
        return "success"

    def numb_changed(self):
        print("Number Changed: " + self.num.get_number())
        return "success"

    def month_changed(self):
        print("Month Changed")
        return "success"

    def image_clicked(self):
        print("Image Clcked!")
        return "success"

    def file_changed(self):
        print("File changed")
        return "success"

    def email_changed(self):
        print("Email Changed!")
        print("Email: " + self.eml.get_text())
        return "success"

    def datetime_changed(self):
        print("Datetime changed")
        print("DateTime: " + self.dtl.get_value())
        return "success"

    def date_changed(self):
        print("Date Changed!")
        print("Date: " + self.dt.get_value())
        return "success"

    def color_changed(self):
        print("Color changed!")
        print("Color: " + self.clr.get_value())
        return "success"

    def checkbox_clicked(self):
        print("Checkbox clicked!")
        return "success"

    def populate_text(self):
        self.txt.set_text("Hello!")
        print("Text Populated!")
        return "success"

    def change_btn_title(self):
        self.btn.set_title("New Title")
        print("Btn title changed!")
        return "success"

    def text_changed(self):
        print("Text Changed:" + self.txt.get_text())
        # if self.txt.get_text() == "" or self.txt.get_text() is None:
        #     self.btn1.set_title('Populate')
        # else:
        #     self.btn1.set_title('Clear')
        return "Text Change Triggred!"


def start_app():
    p = PageTest()
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
