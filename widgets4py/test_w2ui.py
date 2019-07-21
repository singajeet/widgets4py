import os
import webview
from flask import Flask  # , url_for
from widgets4py.base import Page
from widgets4py.layouts import SimpleGridLayout
from widgets4py.w2ui.ui import GridColumn, GridColumnCollection
from widgets4py.w2ui.ui import GridRecord, GridRecordCollection, Grid
from widgets4py.html5.app_ui import Button
from multiprocessing import Process


app = Flask(__name__)


class W2UIPage:

    pg = None
    g_col1 = None
    g_col2 = None
    g_column_coll = None
    g_rec1 = None
    g_rec2 = None
    g_record_coll = None
    grid = None
    sgl = None
    bt_tgl = None
    bt_add = None
    bt_sel_all = None
    bt_unsel_all = None
    bt_sel = None
    bt_unsel = None

    def show_layout(self):
        self.pg = Page('myPage', 'My Page')
        self.sgl = SimpleGridLayout('sgl', 1, 6)
        self.bt_tgl = Button('bt_tgl', 'Toggle', app=app, onclick_callback=self.grid_col_callback)
        self.bt_add = Button('bt_add', 'Add Record', app=app, onclick_callback=self.grid_add_rec_callback)
        self.bt_sel_all = Button('bt_sel_all', 'Select All', app=app, onclick_callback=self.grid_sel_all_callback)
        self.bt_unsel_all = Button('bt_unsel_all', 'Unselect All', app=app,
                                   onclick_callback=self.grid_unsel_all_callback)
        self.bt_sel = Button('bt_sel', 'Select', app=app, onclick_callback=self.grid_sel_callback)
        self.bt_unsel = Button('bt_unsel', 'UnSelect', app=app, onclick_callback=self.grid_unsel_callback)
        self.sgl.add(self.bt_tgl)
        self.sgl.add(self.bt_add)
        self.sgl.add(self.bt_sel_all)
        self.sgl.add(self.bt_unsel_all)
        self.sgl.add(self.bt_sel)
        self.sgl.add(self.bt_unsel)
        self.pg.add(self.sgl)
        self.g_col1 = GridColumn('fname', 'First Name', 50)
        self.g_col2 = GridColumn('lname', 'Last Name', 50)
        self.g_column_coll = GridColumnCollection()
        self.g_column_coll.add(self.g_col1)
        self.g_column_coll.add(self.g_col2)
        self.g_rec1 = GridRecord()
        self.g_rec1.add_cell("fname", "Ajeet")
        self.g_rec1.add_cell("lname", "Singh")
        self.g_rec2 = GridRecord()
        self.g_rec2.add_cell("fname", "Armin")
        self.g_rec2.add_cell("lname", "Kaur")
        self.g_record_coll = GridRecordCollection()
        self.g_record_coll.add(self.g_rec1)
        self.g_record_coll.add(self.g_rec2)
        self.grid = Grid('grid', 'My Table', self.g_column_coll, row_collection=self.g_record_coll,
                         toolbar=True, footer=True, line_numbers=True, select_column=True,
                         multi_select=True, app=app, toolbarAdd=True, toolbarDelete=True,
                         toolbarSave=True, toolbarEdit=True)
        self.pg.add(self.grid)
        content = self.pg.render()
        return content

    def grid_col_callback(self):
        self.grid.toggle_column('fname')

    def grid_add_rec_callback(self):
        rec = GridRecord()
        rec.add_cell("fname", "Jippy")
        rec.add_cell("lname", "Singh")
        self.grid.add_record(rec)

    def grid_sel_all_callback(self):
        self.grid.select_all_records()

    def grid_unsel_all_callback(self):
        self.grid.unselect_all_records()

    def grid_sel_callback(self):
        self.grid.select_records("2")

    def grid_unsel_callback(self):
        self.grid.unselect_records("2")


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
