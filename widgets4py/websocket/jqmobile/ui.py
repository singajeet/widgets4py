"""
This module contains the API's to create app for mobile using
JQuery Mobile framework

Author: Ajeet Singh
Date: 07/30/2019
"""
from flask_socketio import Namespace
from widgets4py.base import Widget
from enum import Enum


class MPage(Widget):
    """The mobile will will act as parent widget to hold all
    other widgets for mobile
    """

    _title = None
    _header_widgets = None
    _footer_widgets = None
    _socketio = None
    _footer_title = None
    _before_render_callback = None
    _after_render_callback = None

    def __init__(self, name, title, socketio, header_widgets=None, footer_widgets=None,
                 child_widgets=None, footer_title=None, before_render_callback=None,
                 after_render_callback=None):
        Widget.__init__(self, name)
        self._title = title
        self._socketio = socketio
        if header_widgets is not None:
            self._header_widgets = header_widgets
        else:
            self._header_widgets = []
        if child_widgets is not None:
            self._child_widgets = child_widgets
        else:
            self._child_widgets = []
        if footer_widgets is not None:
            self._footer_widgets = footer_widgets
        else:
            self._footer_widgets = []
        self._footer_title = footer_title
        self._before_render_callback = before_render_callback
        self._after_render_callback = after_render_callback

    def render(self):
        """Render the contents of mobile page in browser"""
        if self._before_render_callback is not None:
            self._before_render_callback(self._name, {'title': self._title,
                                                      'footer_title': self._footer_title})
        header_content = ""
        if self._header_widgets is not None:
            for hwidget in self._header_widgets:
                header_content += hwidget.render()
        footer_content = ""
        if self._footer_widgets is not None:
            for fwidget in self._footer_widgets:
                footer_content += fwidget.render()
        child_content = ""
        if self._child_widgets is not None:
            for cwidget in self._child_widgets:
                child_content += cwidget.render()
        content = """
                    <div data-role="page" id='%s'>
                        <div data-role="header">
                            <h1>%s</h1>
                            %s
                         </div><!-- /header -->

                         <div role="main" class="ui-content">
                            %s
                         </div><!-- /content -->

                         <div data-role="footer">
                            <h4>%s</h4>
                            %s
                         </div><!-- /footer -->
                    </div><!-- /page -->
                """ % (self._name, self._title, header_content, child_content,
                       self._footer_title, footer_content)
        if self._after_render_callback is not None:
            self._after_render_callback(self._name, {'title': self._title,
                                                     'footer_title': self._footer_title})
        return content


class ButtonStyle(Enum):
    """Types of button supported by the framework"""
    ROUND_CORNERS = 'ui-corner-all'
    SHADOW = 'ui-shadow'
    INLINE = 'ui-btn-inline'
    THEME_A = 'ui-btn-a'
    THEME_B = 'ui-btn-b'
    MINI = 'ui-mini'
    ICON_LEFT = 'ui-btn-icon-left'
    ICON_RIGHT = 'ui-btn-icon-right'
    ICON_TOP = 'ui-btn-icon-top'
    ICON_BOTTOM = 'ui-btn-icon-bottom'
    ICON_NOTEXT = 'ui-btn-icon-notext'
    ICON_SHADOW = 'ui-shadow-icon'
    DISABLED = 'ui-state-disabled'


class Button(Widget, Namespace):
    """Button class to create buttons using <a> tag or <button> tag.
    """

    UI_BTN_CLASS = 'ui-btn'
    ROUND_CORNER_NOTEXT_STYLE = """<style>
                                    #%s-border-radius .ui-btn-icon-notext.ui-corner-all{
                                        -webkit-border-radius: .3125em;
                                        border-radius: .3125em;
                                    }
                                    </style>
                                    """
    _title = None
    _icon = None
    _full_round = None
    _tag_type = None
    _btn_styles = None
    _socket_io = None
    _namespace = None
    _click_callback = None

    def __init__(self, name, socket_io, title=None, icon=None, full_round=None, tag_type=None,
                 btn_styles=None, click_callback=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, str(__name__ + "_" + name + "_mbtn").replace('.', '_'))
        self._namespace = str(__name__ + "_" + name + "_mbtn").replace('.', '_')
        self._socket_io = socket_io
        self._title = title
        self._icon = icon
        if full_round is not None:
            self._full_round = full_round
        else:
            self._full_round = False
        if tag_type is not None:
            self._tag_type = tag_type
        else:
            self._tag_type = 'A'
        if btn_styles is not None:
            self._btn_styles = btn_styles
        else:
            self._btn_styles = []
        if title is None and icon is not None:
            found = False
            for st in self._btn_styles:
                if st == ButtonStyle.ICON_NOTEXT:
                    found = True
            if not found:
                self._btn_styles.append(ButtonStyle.ICON_NOTEXT)
        self._socket_io.on_namespace(self)

    @property
    def namespace(self):
        """Namespace to be used by websockets"""
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def title(self):
        """Title to be shown on the button"""
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def icon(self):
        """CSS icon class to show icon on button"""
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val

    @property
    def is_full_round(self):
        """Returns whether the button should be fully round or not"""
        return self._full_round

    @is_full_round.setter
    def is_full_round(self, val):
        self._full_round = val

    @property
    def tag_type(self):
        """The HTML tag type (a or button) to render the button"""
        return self._tag_type

    @tag_type.setter
    def tag_type(self, val):
        self._tag_type = val

    @property
    def btn_styles(self):
        """A list of the styles applied to button"""
        return self._btn_styles

    @btn_styles.setter
    def btn_styles(self, val):
        self._btn_styles = val

    def render(self):
        content = ""
        if self._tag_type == "A":
            content = "<a href='#' "
        else:
            content = "<button "
        content += "id='" + self._name + "' "
        content += "class='" + self.UI_BTN_CLASS + " "
        if self._icon is not None:
            content += self._icon + " "
        if self._btn_styles is not None:
            for st in self._btn_styles:
                content += st.value + " "
        content = content.strip() + "' >"
        if self._title is not None:
            content += self._title
        if self._tag_type == "A":
            content += "</a>"
        else:
            content += "</button>"
        if self._full_round is not None and not self._full_round and self._title is None:
            content = ("<div id='%s-border-radius'>" % (self._name)) + content + "</div>"
            content += (self.ROUND_CORNER_NOTEXT_STYLE % (self._name))
        return content