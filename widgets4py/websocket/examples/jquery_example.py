from widgets4py.base import Page
from flask import Flask
from flask_socketio import SocketIO
from widgets4py.websocket.jquery.ui import Section, Accordion, RadioButtonGroup, CheckBoxGroup, DialogBox
from widgets4py.websocket.jquery.ui import DialogTypes
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
        self._pg.add(self._sg)
        self._pg.add(self._dlg)
        return self._pg.render()

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
