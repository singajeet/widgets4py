from flask import Flask
from widgets4py.base import Page
from widgets4py.layouts import SimpleGridLayout
from widgets4py.ajax import Button, TextBox, CheckBox, Color


app = Flask(__name__)


class PageTest:

    txt = None
    btn = None
    btn1 = None
    clr = None

    def show_layout(self):
        pg = Page('myPage', 'My Page')
        sg = SimpleGridLayout("Grid", 3, 2)
        self.btn = Button('btn', 'Push', app=app, onclick_callback=self.change_btn_title)
        self.btn1 = Button('btn1', 'Populate', app=app, onclick_callback=self.populate_text)
        self.txt = TextBox('txt', app=app, onchange_callback=self.text_changed)
        self.chk = CheckBox('chk', "Checkbox text", app=app, onclick_callback=self.checkbox_clicked)
        self.clr = Color('clr', app=app, onchange_callback=self.color_changed)
        sg.add(self.btn)
        sg.add(self.btn1)
        sg.add(self.txt)
        sg.add(self.chk)
        sg.add(self.clr)
        pg.add(sg)
        content = pg.render()
        return content

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
        if self.txt.get_text() == "" or self.txt.get_text() is None:
            self.btn1.set_title('Populate')
        else:
            self.btn1.set_title('Clear')
        return "Text Change Triggred!"


p = PageTest()
app.add_url_rule('/', 'index', p.show_layout)
# def local_func():
#     w = Page('My Widget')
#     lay = GridLayout('Grid', 2, 2)
#     w.add(lay)
#     print(w.render())


# if __name__ == "__main__":
#     local_func()
#     input()
#     local_func()
