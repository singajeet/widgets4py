"""

HTML Widgets based on the JQuery UI framework with WebSocket implementation
Author: Ajeet Singh
Date: 08/16/2019

"""
from flask_socketio import Namespace, emit
from widgets4py.base import Widget
from flask import json
from enum import Enum


class Section(Widget, Namespace):
    """Section class renders an section with title in an Accordion.
        This class can have further widgets as its children and same
        will be rendered within the section itself.
    """

    _title = None
    _onclick_callback = None
    _disabled = None
    _required = None
    _namespace = None
    _socket_io = None

    def __init__(self, name, title, socket_io, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, onclick_callback=None, css_cls=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                socket_io (SocketIO): An instance of the SocketIO class
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                required (Boolean, optional): Widget is required to be filled-in or not
                onclick_callback (function, optional): A function to be called back on onclick event
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + str(name) + "_section").replace('.', '_'))
        self._title = title
        self._namespace = '/' + str(__name__ + str(name) + "_section").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._onclick_callback = onclick_callback
        self._disabled = disabled
        self._required = required

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties('title', val)

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    def _attach_onclick(self):
        script = """<script>
                    $(document).ready(function(){
                        var selector = $("#%s");
                        var title_selector = $("#%s_h3");
                        var socket = io("%s");

                        title_selector.bind("click", function(){
                            var props = {
                                        "title": title_selector.text(),
                                        "disabled": selector.hasClass("ui-state-disabled")
                            };
                            socket.emit("fire_click_event", props);
                        });

                      socket.on("sync_properties_%s", function(props){
                          if(props["cmd"] === "title"){
                              title_selector.text(props["value"]);
                          } else if(props["cmd"] === "disabled"){
                              if(props["value"] == true){
                                  selector.addClass("ui-state-disabled");
                              } else {
                                  selector.removeClass("ui-state-disabled");
                              }
                          }
                        });
                    });
                    </script>
            """ % (self._name, self._name, self._namespace, self._name)
        return script

    def on_fire_click_event(self, props):
        if props.__len__() > 0:
            tit = props['title']
            if tit is not None:
                self._title = tit
            dsbld = props['disabled']
            if dsbld is not None:
                self._disabled = dsbld
        if self._onclick_callback is not None:
            self._onclick_callback(self._name, props)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def on_click(self, onclick_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                onclick_callback (function): The function/callback that will be called for this event
        """
        self._onclick_callback = onclick_callback

    def render(self):
        content = "<h3 id='" + self._name + "_h3' "\
            + " >"\
            + self._title + "</h3>\n"
        content += self._render_pre_content('div')
        for widget in self._child_widgets:
            content += "\n" + widget.render()
        content += "\n" + self._attach_onclick()
        content += self._render_post_content('div')
        self._widget_content = content
        return self._widget_content


class Accordion(Widget, Namespace):
    """Class to render an accordion widget and its sections built using the
    `Section` class of this module.
    """

    _onclick_callback = None
    _disabled = None
    _required = None
    _collapsible = None
    _icons = None
    _fill_space = None
    _namespace = None
    _socket_io = None
    _active = None
    _animate = None
    _event_to_toggle = None
    _height_style = None

    def __init__(self, name, socket_io, collapsible=False, desc=None, prop=None, style=None,
                 attr=None, disabled=False, required=False, onclick_callback=None, css_cls=None,
                 icons=None, fill_space=False):
        """Default constructor of the Accordion widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                socket_io (SocketIO): An instance of the socketIO class
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                required (Boolean, optional): Widget is required to be filled-in or not
                onclick_callback (function, optional): A function to be called back on onclick event
                css_cls (list, optional): An list of CSS class names to be added to current widget
                collapsible (boolean, optional): Whether to have all sections collapsible
                fill_space (boolean, optional): Fill the vertical space to match the parent container's
                                                height
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_accordion").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_accordion").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._onclick_callback = onclick_callback
        self._disabled = disabled
        self._required = required
        self._collapsible = collapsible
        if icons is not None:
            self._icons = icons
        else:
            self._icons = {}
        self._fill_space = fill_space

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val):
        self._active = val
        self._sync_properties('active', val)

    @property
    def animate(self):
        return self._animate

    @animate.setter
    def animate(self, val):
        self._animate = val
        self._sync_properties('animate', val)

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def collapsible(self):
        """Returns whether the sections are collapsible or not"""
        return self._collapsible

    @collapsible.setter
    def collapsible(self, val):
        self._collapsible = val
        self._sync_properties('collapsible', val)

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def event_to_toggle(self):
        return self._event_to_toggle

    @event_to_toggle.setter
    def event_to_toggle(self, val):
        self._event_to_toggle = val
        self._sync_properties('event', val)

    @property
    def height_style(self):
        return self._height_style

    @height_style.setter
    def height_style(self, val):
        self._height_style = val
        self._sync_properties('height_style', val)

    @property
    def icons(self):
        """Returns JavaScript `dict` of CSS classes related to icons of sections

            Example:
                { "header": "ui-icon-plus", "activeHeader": "ui-icon-minus" }
        """
        return self._icons

    @icons.setter
    def icons(self, val):
        self._icons = val
        self._sync_properties('icons', val)

    @property
    def fill_space(self):
        """Returns whether sections will be filled with space to match parent's
        height"""
        return self._fill_space

    @fill_space.setter
    def fill_space(self, val):
        self._fill_space = val

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def render(self):
        """Method to render the content of Accordion and its child widget's
        i.e., `Section`
        """
        content = self._render_pre_content('div')
        for widget in self._child_widgets:
            content += "\n" + widget.render()
        content += self._render_post_content('div')
        content += """<script>
                        $(function(){
                            var selector = $("#%s");
                            var socket = io("%s");

                            selector.accordion({
                                collapsible: %s,
                                icons: %s,
                                heightStyle: "%s"
                            });

                            socket.on('sync_properties_%s', function(props){
                                selector.accordion("option", props['cmd'], props['value']);
                            });
                        });
                        </script>
                    """ % (self._name, self._namespace, "true" if self._collapsible else "false",
                           self._icons, "fill" if self._fill_space else "", self._name)
        self._widget_content = content
        return self._widget_content


class RadioButtonGroup(Widget, Namespace):
    """Widget to display options provided in `dict` object as RadioButton grouped
    together under a title passed as parameter
    """

    _title = None
    _items = None
    _show_icon = None
    _onclick_callback = None
    _checked = None
    _disabled_buttons = None
    _namespace = None
    _socket_io = None

    def __init__(self, name, title, socket_io, items=None, show_icon=False, desc=None, prop=None, style=None,
                 attr=None, onclick_callback=None, css_cls=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the Radio button group
                items (dict): A dict object containing items in the following format...
                                {'key1': ['title1', false]} false means radio will be shown unselected
                socket_io (SocketIO): An instance of SocketIO class
                show_icon (boolean, optional): whether to show icon or not, default is true
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                onclick_callback (function, optional): A function to be called back on onclick event
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_rbg").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_rbg").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._title = title
        if items is not None:
            self._items = items
        else:
            self._items = {}
        self._show_icon = show_icon
        self._onclick_callback = onclick_callback
        self._disabled_buttons = {}
        self._checked_buttons = {}

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, val):
        self._items = val

    @property
    def show_icon(self):
        return self._show_icon

    @show_icon.setter
    def show_icon(self, val):
        self._show_icon = val

    @property
    def disabled_buttons(self):
        return self._disabled_buttons

    @disabled_buttons.setter
    def disabled_buttons(self, val):
        self._disabled_buttons = val

    @property
    def checked_buttons(self):
        return self._checked_buttons

    @checked_buttons.setter
    def checked_buttons(self, val):
        self._checked_buttons = val

    def set_disabled(self, btn, state):
        """Sets whether the passed radio button should be set as disabled or not

            Args:
                btn (string): Name of the radio button that exists in this group
                state (boolean): True or False
        """
        self._disabled_buttons[btn] = state
        self._sync_properties("disabled", self._disabled_buttons)

    def get_disabled(self, btn):
        """Returns the state of the radio button passed as parameter

            Args:
                btn (string): Name of the radio button that exists in the ths group
            Returns:
                boolean: True or False based on current state
        """
        return self._disabled_buttons[btn]

    def set_checked(self, btn, state):
        """Sets whether the passed radio button should be set as checked or not

            Args:
                btn (string): Name of the radio button that exists in the group
            Returns:
                boolean: True or False based on current state
        """
        self._checked_buttons[btn] = state
        self._sync_properties("checked", self._checked_buttons)

    def get_checked(self, btn):
        """Returns the state of the radio button passes as parameter

            Args:
                btn (string): Name of the radio button that exists in the ths group
            Returns:
                boolean: True or False based on current state
        """
        return self._checked_buttons[btn]

    def add_item(self, name, title, is_selected):
        """Adds an new item to the group of radio buttons

            Args:
                name (string): A unique identifier of the radio button
                title (string): Title to be displyed along the radio button
                is_selected (boolean): Shows radio button as checked or not checked
        """
        self._items[name] = [title, is_selected]
        self._checked_buttons[name] = is_selected
        self._disabled_buttons[name] = False

    def remove_item(self, name):
        """Removes an radio button from the group

            Args:
                name (string): Unique identifier of the radio button
        """
        self._items.pop(name)

    def _attach_script(self):

        script = """
                    <script>
                        $(function(){
                            var selector_lbl = $("label[id^='%s_lbl']");
                            var selector = $("input[id^='%s_rd']");
                            var socket = io("%s");

                            selector.checkboxradio({
                                icon: %s
                            });

                            socket.on("sync_properties_%s", function(props){
                                if(props["cmd"] == "checked"){
                                    var checked = props["value"];
                                    selector.each(function(index, value){
                                        var id = $(this).attr("id");
                                        $(this).prop("checked", checked[id]);
                                    });
                                } else if(prop["cmd"] == "disabled"){
                                    var disabled = props["value"];
                                    selector.each(function(index, value){
                                        var id = $(this).attr("id");
                                        $(this).checkboxradio("option", "disabled", disabled[id]);
                                    });
                                }
                            });

                            selector.on("click", function(event){
                                    checkbox = event.currentTarget;
                                    var checked = {}
                                    selector.each(function(index, value){
                                        var id = $(this).attr("id");
                                        if(id != checkbox.id){
                                            checked[id] = $(this).prop("checked");
                                        } else {
                                            checked[id] = checkbox.checked;
                                        }
                                    });
                                    var disabled = {}
                                    selector.each(function(index, value){
                                        var id = $(this).attr("id");
                                        disabled[id] = $(this).checkboxradio("option", "disabled");
                                    });
                                    var props = {"checked": checked, "disabled": disabled};
                                    socket.emit('fire_click_event', props);

                            });

                        });
                    </script>
                """ % (self._name, self._name, self._namespace, json.dumps(True if self._show_icon else False),
                       self._name)
        return script

    def on_fire_click_event(self, props):
        if props.__len__() > 0:
            check = props['checked']
            if check is not None:
                self._checked_buttons = check
            dsbld = props['disabled']
            if dsbld is not None:
                self._disabled_buttons = dsbld
        if self._onclick_callback is not None:
            self._onclick_callback(self._name, props)

    def on_click(self, onclick_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                onclick_callback (function): The function/callback that will be called for this event
        """
        self._onclick_callback = onclick_callback

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def render(self):
        """Renders the Radio button group with title passed as param
        """
        content = "<fieldset>\n<legend>" + self._title + "</legend>\n"
        for item in self._items:
            val = self._items.get(item)
            title = val[0]
            is_sel = val[1]
            name = self._name + "_rd_" + item
            lbl_name = self._name + "_lbl_" + item
            label = "<label for='" + name + "' id='" + lbl_name + "' >"\
                + (title if title is not None else item) + "</label>"
            radio = "<input id='" + name + "' type='radio'"\
                + (" checked" if is_sel else "")\
                + " name='" + self._name + "_rd' />"
            content += "\n" + label + "\n" + radio
        self._widget_content = content + "\n</fieldset>"\
                                       + self._attach_script()
        return self._widget_content


class CheckBoxGroup(Widget, Namespace):
    """Widget to display options provided in `dict` object as CheckBox grouped
    together under a title passed as parameter
    """

    _title = None
    _items = None
    _show_icon = None
    _onclick_callback = None
    _checked = None
    _disabled_buttons = None
    _namespace = None
    _socket_io = None

    def __init__(self, name, title, socket_io, items=None, show_icon=False, desc=None, prop=None, style=None,
                 attr=None, onclick_callback=None, css_cls=None):
        """Default constructor of the checkbox widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the checkbox button group
                items (dict): A dict object containing items in the following format...
                                {'key1': ['title1', false]} false means radio will be shown unselected
                socket_io (SocketIO): An instance of SocketIO class
                show_icon (boolean, optional): whether to show icon or not, default is true
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                onclick_callback (function, optional): A function to be called back on onclick event
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_cbg").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_cbg").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._title = title
        if items is not None:
            self._items = items
        else:
            self._items = {}
        self._show_icon = show_icon
        self._onclick_callback = onclick_callback
        self._disabled_buttons = {}
        self._checked_buttons = {}

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, val):
        self._items = val

    @property
    def show_icon(self):
        return self._show_icon

    @show_icon.setter
    def show_icon(self, val):
        self._show_icon = val

    @property
    def disabled_buttons(self):
        return self._disabled_buttons

    @disabled_buttons.setter
    def disabled_buttons(self, val):
        self._disabled_buttons = val

    @property
    def checked_buttons(self):
        return self._checked_buttons

    @checked_buttons.setter
    def checked_buttons(self, val):
        self._checked_buttons = val

    def set_disabled(self, btn, state):
        """Sets whether the passed checkbox button should be set as disabled or not

            Args:
                btn (string): Name of the checkbox button that exists in this group
                state (boolean): True or False
        """
        self._disabled_buttons[btn] = state
        self._sync_properties("disabled", self._disabled_buttons)

    def get_disabled(self, btn):
        """Returns the state of the radio button passed as parameter

            Args:
                btn (string): Name of the checkbox button that exists in the ths group
            Returns:
                boolean: True or False based on current state
        """
        return self._disabled_buttons[btn]

    def set_checked(self, btn, state):
        """Sets whether the passed checkbox button should be set as checked or not

            Args:
                btn (string): Name of the checkbox button that exists in the group
            Returns:
                boolean: True or False based on current state
        """
        self._checked_buttons[btn] = state
        self._sync_properties("checked", self._checked_buttons)

    def get_checked(self, btn):
        """Returns the state of the checkbox button passes as parameter

            Args:
                btn (string): Name of the checkbox button that exists in the ths group
            Returns:
                boolean: True or False based on current state
        """
        return self._checked_buttons[btn]

    def add_item(self, name, title, is_selected):
        """Adds an new item to the group of checkbox buttons

            Args:
                name (string): A unique identifier of the checkbox button
                title (string): Title to be displyed along the checkbox button
                is_selected (boolean): Shows check button as checked or not checked
        """
        self._items[name] = [title, is_selected]
        self._checked_buttons[name] = is_selected
        self._disabled_buttons[name] = False

    def remove_item(self, name):
        """Removes an checkbox button from the group

            Args:
                name (string): Unique identifier of the checkbox button
        """
        self._items.pop(name)

    def _attach_script(self):

        script = """
                    <script>
                        $(function(){
                            var selector = $("input[id^='%s_cb']");
                            var selector_lbl = $("label[id^='%s_lbl']");
                            var socket = io("%s");

                            selector.checkboxradio({
                                icon: %s
                            });

                            socket.on("sync_properties_%s", function(props){
                                if(props["cmd"] == "checked"){
                                    var checked = props["value"];
                                    selector.each(function(index, value){
                                        var id = $(this).attr("id");
                                        $(this).prop("checked", checked[id]);
                                    });
                                } else if(prop["cmd"] == "disabled"){
                                    var disabled = props["value"];
                                    selector.each(function(index, value){
                                        var id = $(this).attr("id");
                                        $(this).checkboxradio("option", "disabled", disabled[id]);
                                    });
                                }
                            });

                            selector.on("click", function(event){
                                checkbox = event.currentTarget;
                                var checked = {}
                                selector.each(function(index, value){
                                    var id = $(this).attr("id");
                                    if(id != checkbox.id){
                                        checked[id] = $(this).prop("checked");
                                    } else {
                                        checked[id] = checkbox.checked;
                                    }
                                });
                                var disabled = {}
                                selector.each(function(index, value){
                                    var id = $(this).attr("id");
                                    disabled[id] = $(this).checkboxradio("option", "disabled");
                                });
                                var props = {"checked": checked, "disabled": disabled};
                                socket.emit('fire_click_event', props);
                            });
                        });
                    </script>
                """ % (self._name, self._name, self._namespace, json.dumps(True if self._show_icon else False),
                       self._name)
        return script

    def on_fire_click_event(self, props):
        if props.__len__() > 0:
            check = props['checked']
            if check is not None:
                self._checked_buttons = check
            dsbld = props['disabled']
            if dsbld is not None:
                self._disabled_buttons = dsbld
        if self._onclick_callback is not None:
            self._onclick_callback(self._name, props)

    def on_click(self, onclick_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                onclick_callback (function): The function/callback that will be called for this event
        """
        self._onclick_callback = onclick_callback

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def render(self):
        """Renders the checkbox button group with title passed as param
        """
        content = "<fieldset>\n<legend>" + self._title + "</legend>\n"
        for item in self._items:
            val = self._items.get(item)
            title = val[0]
            is_sel = val[1]
            name = self._name + "_cb_" + item
            lbl_name = self._name + "_lbl_" + item
            label = "<label for='" + name + "' id='" + lbl_name + "' >"\
                + (title if title is not None else item) + "</label>"
            checkbox = "<input id='" + name + "' type='checkbox'"\
                + (" checked" if is_sel else "")\
                + " name='" + name + "' />"
            content += checkbox + "\n" + label
        content += "\n</fieldset>"
        self._widget_content = self._attach_script() + "\n" + content
        return self._widget_content


class DialogTypes(Enum):
    """Various types are supported by DialogBox which are shown below. One of the type
    needs to be passed to object of `DialogBox` while creating it. Below are the
    supported dialog types:

        1. Default
        2. Modal Confirmation
        3. Modal Form
        4. Modal Message
    """
    DEFAULT = 0
    MODAL_CONFIRM = 1
    MODAL_FORM = 2
    MODAL_MESSAGE = 3


class DialogBox(Widget, Namespace):
    """Class to shown dialog boxes which is on overlay position within the viewport.
     It has a title bar and a content area, and can be moved, resized and closed with the 'x' icon by default.
     """

    _namespace = None
    _socket_io = None
    _onok_pressed_callback = None
    _oncancel_pressed_callback = None
    _disabled = None
    _command = None
    _dialog_type = None
    _onbefore_close_callback = None
    _is_dialog_open = None
    _title = None
    _height = None
    _width = None
    _append_to = None
    _autoOpen = None
    _buttons = None
    _closeOnEscape = None
    _closeText = None
    _draggable = None
    _hide = None
    _maxHeight = None
    _maxWidth = None
    _minHeight = None
    _minWidth = None
    _modal = None
    _position = None
    _resizable = None
    _show = None

    def __init__(self, name, title, dlg_type, socket_io, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, css_cls=None, height=400, width=350,
                 onbefore_close_callback=None, onok_pressed_callback=None,
                 oncancel_pressed_callback=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                dlg_type (DialogType): The type of the dialog box that needs to be created
                socket_io (SocketIO): Instance of SocketIO class
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                onclick_callback (function, optional): A function to be called back on onclick event
                css_cls (list, optional): An list of CSS class names to be added to current widget
                height (int, optional): Height of the dialog box, used in dialog type = MODAL_CONFIRM,
                                        MODAL_FORM, MODAL_MESSAGE
                width (int, optional): Width of the dialog box, used in dialog type = MODAL_CONFIRM,
                                        MODAL_FORM, MODAL_MESSAGE
                onbefore_close_callback (func): Callback function that will be called before dialog
                                                is closed
                onok_pressed_callback (func): This function is called when ok button is pressed
                oncancel_pressed_callback (func): Function is called when cancel is pressed
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_dialog").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_dialog").replace('.', '_')
        self._title = title
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._onok_pressed_callback = onok_pressed_callback
        self._oncancel_pressed_callback = oncancel_pressed_callback
        self._disabled = disabled
        self._dialog_type = dlg_type
        self._height = height
        self._width = width
        self._onbefore_close_callback = onbefore_close_callback
        self._is_dialog_open = False
        self.add_property('title', title)

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def dialog_type(self):
        return self._dialog_type

    @dialog_type.setter
    def dialog_type(self, val):
        self._dialog_type = val

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties('title', val)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val
        self._sync_properties('height', val)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val
        self._sync_properties('width', val)

    @property
    def is_dialog_open(self):
        return self._is_dialog_open

    @is_dialog_open.setter
    def is_dialog_open(self, val):
        self._is_dialog_open = val

    @property
    def appendTo(self):
        return self._appendTo

    @appendTo.setter
    def appendTo(self, val):
        self._appendTo = val
        self._sync_properties('appendTo', val)

    @property
    def autoOpen(self):
        return self._autoOpen

    @autoOpen.setter
    def autoOpen(self, val):
        self._autoOpen = val
        self._sync_properties('autoOpen', val)

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    def buttons(self, val):
        self._buttons = val
        self._sync_properties('buttons', val)

    @property
    def closeOnEscape(self):
        return self._closeOnEscape

    @closeOnEscape.setter
    def closeOnEscape(self, val):
        self._closeOnEscape = val
        self._sync_properties('closeOnEscape', val)

    @property
    def closeText(self):
        return self._closeText

    @closeText.setter
    def closeText(self, val):
        self._closeText = val
        self._sync_properties('closeText', val)

    @property
    def draggable(self):
        return self._draggable

    @draggable.setter
    def draggable(self, val):
        self._draggable = val
        self._sync_properties('draggable', val)

    @property
    def hide(self):
        return self._hide

    @hide.setter
    def hide(self, val):
        self._hide = val
        self._sync_properties('hide', val)

    @property
    def maxHeight(self):
        return self._maxHeight

    @maxHeight.setter
    def maxHeight(self, val):
        self._maxHeight = val
        self._sync_properties('maxHeight', val)

    @property
    def maxWidth(self):
        return self._maxWidth

    @maxWidth.setter
    def maxWidth(self, val):
        self._maxWidth = val
        self._sync_properties('maxWidth', val)

    @property
    def minHeight(self):
        return self._minHeight

    @minHeight.setter
    def minHeight(self, val):
        self._minHeight = val
        self._sync_properties('minHeight', val)

    @property
    def minWidth(self):
        return self._minWidth

    @minWidth.setter
    def minWidth(self, val):
        self._minWidth = val
        self._sync_properties('minWidth', val)

    @property
    def modal(self):
        return self._modal

    @modal.setter
    def modal(self, val):
        self._modal = val
        self._sync_properties('modal', val)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val
        self._sync_properties('position', val)

    @property
    def resizable(self):
        return self._resizable

    @resizable.setter
    def resizable(self, val):
        self._resizable = val
        self._sync_properties('resizable', val)

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        self._show = val
        self._sync_properties('show', val)

    def open(self):
        """Opens the dialog box
        """
        self._command = "open"
        self._sync_properties(self._command, "")
        self._is_dialog_open = True

    def close(self):
        """Closes the dialog box
        """
        self._command = "close"
        self._sync_properties(self._command, "")
        self._is_dialog_open = False

    def on_fire_before_close_event(self, props):
        self._is_dialog_open = False
        # Reset the command to close, before the dialogbox is closed using esc key,
        # or on, cancel buttons
        self._command = "close"
        if self._onbefore_close_callback is not None:
            self._onbefore_close_callback(self._name, props)

    def on_fire_ok_pressed_event(self, props):
        if self._onok_pressed_callback is not None:
            self._onok_pressed_callback(self._name, props)

    def on_fire_cancel_pressed_event(self, props):
        if self._oncancel_pressed_callback is not None:
            self._oncancel_pressed_callback(self._name, props)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def on_before_close(self, onbefore_close_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                onbefore_close_callback (function): The function/callback that will be
                                                    called for this event
        """
        self._onbefore_close_callback = onbefore_close_callback

    def on_ok_pressed(self, onok_pressed_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                onok_pressed_callback (function): The function/callback that will be
                                                    called for this event
        """
        self._onok_pressed_callback = onok_pressed_callback

    def on_cancel_pressed(self, oncancel_pressed_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                oncancel_pressed_callback (function): The function/callback that will be
                                                        called for this event
        """
        self._oncancel_pressed_callback = oncancel_pressed_callback

    def _attach_dialog(self, dlg_type):  # noqa
        script = ""
        if dlg_type == DialogTypes.DEFAULT:
            script = """<script>
                            $(function(){
                                var selector = $("#%s");
                                var socket = io("%s");

                                socket.on('sync_properties_%s', function(props){
                                    cmd = props['cmd'];
                                    value = props['value'];
                                    if(cmd === 'open'){
                                        var isOpen = selector.dialog('isOpen');

                                        if(!isOpen){
                                            selector.dialog('open');
                                        }
                                    } else if(cmd === 'close'){
                                        var isOpen = selector.dialog('isOpen');
                                        if(isOpen){
                                            selector.dialog('close');
                                        }
                                    } else{
                                        selector.dialog('option', cmd, value);
                                    }
                                });

                                selector.dialog({
                                    autoOpen: false,
                                    resizable: true,
                                    beforeClose: function(event, ui){
                                        socket.emit('fire_before_close_event', {});
                                    }
                                });
                            });
                        </script>
                    """ % (self._name, self._namespace, self._name)
        elif dlg_type == DialogTypes.MODAL_CONFIRM:
            script = """<script>
                            $(function(){
                                var selector = $("#%s");
                                var socket = io("%s");

                                socket.on('sync_properties_%s', function(props){
                                    cmd = props['cmd'];
                                    value = props['value'];
                                    if(cmd === 'open'){
                                        var isOpen = selector.dialog('isOpen');

                                        if(!isOpen){
                                            selector.dialog('open');
                                        }
                                    } else if(cmd === 'close'){
                                        var isOpen = selector.dialog('isOpen');
                                        if(isOpen){
                                            selector.dialog('close');
                                        }
                                    } else {
                                        selector.dialog('option', cmd, value);
                                    }
                                });

                                selector.dialog({
                                    autoOpen: false,
                                    resizable: false,
                                    height: %d,
                                    width: %d,
                                    modal: true,
                                    buttons: {
                                        "Ok": function(){
                                            //Call the OK pressed callback or endpoint
                                            socket.emit('fire_ok_pressed_event', {});
                                            $(this).dialog('close');
                                        },
                                        "Cancel": function(){
                                            //Call the CANCEL pressed callback or endpoint
                                            socket.emit('fire_cancel_pressed_event', {});
                                            $(this).dialog('close');
                                        }
                                    },
                                    beforeClose: function(event, ui){
                                        socket.emit('fire_before_close_event', {});
                                    }
                                });
                            });
                        </script>
                    """ % (self._name, self._namespace, self._name, self._height, self._width)
        elif dlg_type == DialogTypes.MODAL_FORM:
            script = """<script>
                            $(function(){
                                var selector = $("#%s");
                                var socket = io("%s");

                                socket.on('sync_properties_%s', function(props){
                                    cmd = props['cmd'];
                                    value = props['value'];
                                    if(cmd === 'open'){
                                        var isOpen = selector.dialog('isOpen');

                                        if(!isOpen){
                                            selector.dialog('open');
                                        }
                                    } else if(cmd === 'close'){
                                        var isOpen = selector.dialog('isOpen');
                                        if(isOpen){
                                            selector.dialog('close');
                                        }
                                    } else{
                                        selector.dialog('option', cmd, value);
                                    }
                                });

                                selector.dialog({
                                    autoOpen: false,
                                    resizable: true,
                                    height: %d,
                                    width: %d,
                                    modal: true,
                                    buttons: {
                                        "Ok": function(){
                                            //Call the OK pressed callback or endpoint
                                            socket.emit('fire_ok_pressed_event', {});
                                            $(this).dialog('close');
                                        },
                                        "Cancel": function(){
                                            //Call the CANCEL pressed callback or endpoint
                                            socket.emit('fire_cancel_pressed_event', {});
                                            $(this).dialog('close');
                                        }
                                    },
                                    beforeClose: function(event, ui){
                                        socket.emit('fire_before_close_event', {});
                                    }

                                });
                            });
                        </script>
                    """ % (self._name, self._namespace, self._name, self._height, self._width)
        elif dlg_type == DialogTypes.MODAL_MESSAGE:
            script = """<script>
                            $(function(){
                                var selector = $("#%s");
                                var socket = io("%s");

                                socket.on('sync_properties_%s', function(props){
                                    cmd = props['cmd'];
                                    value = props['value'];
                                    if(cmd === 'open'){
                                        var isOpen = selector.dialog('isOpen');

                                        if(!isOpen){
                                            selector.dialog('open');
                                        }
                                    } else if(cmd === 'close'){
                                        var isOpen = selector.dialog('isOpen');
                                        if(isOpen){
                                            selector.dialog('close');
                                        }
                                    } else {
                                        selector.dialog('option', cmd, value);
                                    }
                                });

                                selector.dialog({
                                    autoOpen: false,
                                    modal: true,
                                    buttons: {
                                        "Ok": function(){
                                            //Call the OK pressed callback or endpoint
                                            socket.emit('fire_ok_pressed_event', {});
                                            $(this).dialog('close');
                                        }
                                    },
                                    beforeClose: function(event, ui){
                                        socket.emit('fire_before_close_event', {});
                                    }

                                });
                            });
                        </script>
                    """ % (self._name, self._namespace, self._name)
        return script

    def render(self):
        content = self._render_pre_content('div')
        for widget in self._child_widgets:
            content += "\n" + widget.render()
        content += self._render_post_content('div')
        content += "\n" + self._attach_dialog(self._dialog_type)
        self._widget_content = content + "\n"  # + self._attach_script()
        return self._widget_content


class MenuItem(Widget, Namespace):
    """A menuitem represents the action item that is clickable or
    executable. A menuitem can have label, icon or submenus.
    Seperator's are built using dash or space as item
    """
    _title = None
    _icon = None
    _menu_clicked_callback = None
    _socket_io = None
    _namespace = None
    _disabled = None

    def __init__(self, name, title, socket_io, icon=None, desc=None, prop=None, style=None, attr=None,
                 menu_clicked_callback=None, css_cls=None, disabled=None):
        """Default constructor of the Menuitem widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the Checkbox button group
                socket_io (SocketIO): An instance of the SocketIO class
                icon (string, optional): whether to show icon or not, default is None
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                menu_clicked_callback (function, optional): A function to be called back on onclick event
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_menuItem").replace(".", "_"))
        self._namespace = '/' + str(__name__ + "_" + name + "_menuItem").replace(".", "_")
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._title = title
        self._icon = icon
        self._menu_clicked_callback = menu_clicked_callback
        self._disabled = disabled
        if disabled:
            self.add_property('class', 'ui-state-disabled')

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def disabled(self):
        """Gets the state of MenuItem widget i.e., whether it is enabled or disabled"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties("disabled", val)

    @property
    def title(self):
        """Returns the value of the title of current MenuItem"""
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties("title", val)

    @property
    def icon(self):
        """Returns the name of the jquery-ui icon style class used for current widget"""
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val
        self._sync_properties("icon", val)

    def _attach_script(self):
        script = """
                    <script>
                        $(function(){
                            var selector = $('#%s');
                            var socket = io('%s');

                            selector.on("click", function(event){
                                var props = {
                                    'disabled': selector.hasClass('ui-state-disabled'),
                                    'icon': '',
                                    'title': selector.children('div').text(),
                                };
                                socket.emit("fire_click_event", props);
                            });

                            socket.on('sync_properties_%s', function(props){
                                if(props['cmd'] == "title" && props["value"] != undefined && props["value"] != ""){
                                    selector.text(props["value"]);
                                }

                                if(props["cmd"] == "disabled" && props["value"]){
                                    if(!selector.hasClass('ui-state-disabled')){
                                            selector.addClass('ui-state-disabled');
                                    }
                                } else if(props["cmd"] == "disabled" && !props["value"]) {
                                    if(selector.hasClass('ui-state-disabled')){
                                        selector.removeClass('ui-state-disabled');
                                    }
                                }

                                if(props["cmd"] == "icon" && props["value"] != ""){
                                    icon_selector = $('#%s_icon');
                                    if(icon_selector != undefined){
                                        if(!icon_selector.hasClass(props["value"])){
                                            icon_selector.addClass(props["value"]);
                                        }
                                    }
                                }
                            });
                        });
                    </script>
                    """ % (self._name, self._namespace, self._name, self._name)
        return script

    def on_menu_clicked(self, menu_clicked_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                menu_clicked_callback (function): The function/callback that will be
                                                    called for this event
        """
        self._menu_clicked_callback = menu_clicked_callback

    def on_fire_click_event(self, props):
        if props.__len__() > 0:
            tit = props['title']
            if tit is not None:
                self._title = tit
            dsbld = props['disabled']
            if dsbld is not None:
                self._disabled = dsbld
        if self._menu_clicked_callback is not None:
            self._menu_clicked_callback(self._name, props)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value})

    def render(self):
        """Renders the menuitem and returns the content to parent widget
        """
        content = self._render_pre_content('li')
        if self._icon is None:
            content += "<div>" + self._title + "</div>"
        else:
            content += "<div><span id='" + (self._name + "_icon")\
                       + "' class='ui-icon " + self._icon + "'></span>"\
                       + self._title + "</div>"
        content += self._render_post_content('li')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content


class SubMenu(MenuItem):
    """SubMenu is an MenuItem with title and further have its child menuitems which appears as
    dropdown panel.
    """

    def __init__(self, name, title, socket_io, icon=None, desc=None, prop=None, style=None, attr=None,
                 menu_clicked_callback=None, css_cls=None):
        """Default constructor of the Menuitem widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the Checkbox button group
                icon (string, optional): whether to show icon or not, default is None
                socket_io (SocketIO): An instance of SocketIO class
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                menu_clicked_callback (function, optional): A function to be called back on onclick event
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        MenuItem.__init__(self, name, title, socket_io, icon=icon, desc=desc, prop=prop, style=style, attr=attr,
                          menu_clicked_callback=menu_clicked_callback, css_cls=css_cls)
        self._namespace = '/' + str(__name__ + "_" + name + "_submenu").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)

    def render(self):
        content = self._render_pre_content('li')
        content += "<div>" + self._title + "</div>"
        content += "<ul>"
        for widget in self._child_widgets:
            content += widget.render()
        content += "</ul>\n</li>"
        self._widget_content = content
        return self._widget_content


class MenuTypes(Enum):
    """Different type of menu layout"""
    VERTICAL = 0
    HORIZONTAL = 1


class Menu(Widget, Namespace):
    """The root of the menu used to layout menu in the desired position and uses various options to
    customize the menu. This is the class that will init the menu system and renders to its parent
    widget
    """
    _menu_type = None
    _socket_io = None
    _namespace = None
    _disabled = None
    _icons = None
    _items = None
    _menus = None
    _position = None
    _role = None

    def __init__(self, name, socket_io, menu_type=None, desc=None, prop=None, style=None, attr=None,
                 css_cls=None):
        """Default constructor of the Menu widget class

            Args:
                name (string): name of the widget for internal use
                menu_type (MenuTypes): Specify which menu type to render, default is vertical
                socket_io (SocketIO): An instance of SocketIO class
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_menu").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_menu").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        if menu_type is None:
            self._menu_type = MenuTypes.VERTICAL
        else:
            self._menu_type = menu_type

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def icons(self):
        return self._icons

    @icons.setter
    def icons(self, val):
        self._icons = val
        self._sync_properties('icons', val)

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, val):
        self._items = val
        self._sync_properties('items', val)

    @property
    def menus(self):
        return self._menus

    @menus.setter
    def menus(self, val):
        self._menus = val
        self._sync_properties('menus', val)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val
        self._sync_properties('position', val)

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, val):
        self._role = val
        self._sync_properties('role', val)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def _attach_css(self):
        css = ""
        if self._menu_type == MenuTypes.VERTICAL:
            css = """<style>
                    .ui-menu {
                        width: 200px;
                    }
                </style>
                """
        elif self._menu_type == MenuTypes.HORIZONTAL:
            css = """<style>
                    #%s {
                      position: fixed;
                      top: 0;
                      left: 0;
                      width: 100%%;
                    }

                    #%s > li {
                      display: inline-block;
                    }
                    #%s > li > ul > li {
                      display: block;
                    }

                    #%s > li > div > span.ui-icon-caret-1-e {
                      background:url(https://www.drupal.org/files/issues/ui-icons-222222-256x240.png) no-repeat -64px -16px !important;  /*  # noqa */
                    }
                    #%s ul li div span.ui-icon-caret-1-e {
                      background:url(https://www.drupal.org/files/issues/ui-icons-222222-256x240.png) no-repeat -32px -16px !important;
                    }
                </style>
            """ % (self._name, self._name, self._name, self._name, self._name)
        return css

    def _attach_script(self):
        script = ""
        if self._menu_type == MenuTypes.VERTICAL:
            script = """<script>
                            $(function(){
                                var selector = $('#%s');
                                var socket = io('%s');

                                selector.menu();

                                socket.on('sync_properties_%s', function(props){
                                    selector.menu('option', props['cmd'], props['value']);
                                });
                            });
                        </script>
                    """ % (self._name, self._namespace, self._name)
        elif self._menu_type == MenuTypes.HORIZONTAL:
            script = """<script>
                        $(function() {
                            var selector = $('#%s');
                            var socket = io('%s');

                            selector.menu();

                            selector.menu({
                                position: { my: 'left top', at: 'left bottom' },
                                blur: function() {
                                            $(this).menu('option', 'position', { my: 'left top', at: 'left bottom' });
                                },
                                focus: function(e, ui) {
                                if ($('#%s').get(0) !== $(ui).get(0).item.parent().get(0)) {
                                    $(this).menu('option', 'position', { my: 'left top', at: 'right top' });
                                    }
                                },
                            });

                            socket.on('sync_properties_%s', function(props){
                                selector.menu('option', props['cmd'], props['value']);
                            });
                        });
                    </script>
                    """ % (self._name, self._namespace, self._name, self._name)
        return script

    def render(self):
        """Renders the menu and all its child submenu and menuitems
        """
        content = self._render_pre_content('ul')
        for widget in self._child_widgets:
            content += widget.render()
        content += self._render_post_content('ul')
        self._widget_content = content + "\n" + self._attach_script() + "\n" + self._attach_css()
        return self._widget_content


class Slider(Widget, Namespace):
    """Slider class to render an slider widget on a page. This class provides
    the callback functionality whenever value is changed in the slider through
    mouse drag operation. The latest value of slider can be captured in the
    callback function
    """

    _onclick_callback = None
    _onchange_callback = None
    _namespace = None
    _socket_io = None
    _animate = None
    _disabled = None
    _max = None
    _min = None
    _orientation = None
    _range = None
    _step = None
    _value = None
    _values = None

    def __init__(self, name, socket_io, value=None, orientation=None, max=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, onclick_callback=None, onchange_callback=None, css_cls=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                socket_io (SocketIO): An instance of SocketIO class
                value (int): Initial value of the slider
                orientation (string): Horizontal or Vertical
                max (int): Maximum value of the slider
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                required (Boolean, optional): Widget is required to be filled-in or not
                onclick_callback (function, optional): A function to be called back on onclick event
                slider_changed_callback (function, optional): Called whenever value of slider changes
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_slider").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_slider").replace('.', '_')
        if value is None:
            self._value = 0
        else:
            self._value = value
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._onchange_callback = onchange_callback
        self._onclick_callback = onclick_callback
        self._disabled = disabled
        if orientation is None:
            self._orientation = "horizontal"
        else:
            self._orientation = orientation
        if max is None:
            self._max = 100
        else:
            self._max = max

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    def _attach_script(self):
        script = """
                    <script>
                        $(function(){
                            var selector = $('#%s');
                            var socket = io('%s');

                            selector.slider();

                            selector.on("click", function(event){
                                var prop = {
                                    'value': selector.slider('value')
                                };
                                socket.emit('fire_click_event', prop);
                            });

                            selector.on("slidechange", function(event){
                                var props = {
                                    'value': selector.slider('value')
                                };
                                socket.emit('fire_change_event', props);
                            });

                            socket.on('sync_properties_%s', function(props){
                                var cmd = props['cmd'];
                                var value = props['value'];
                                selector.slider('option', cmd, value);
                            });
                        });
                    </script>
                """ % (self._name, self._namespace, self._name)
        return script

    def on_fire_click_event(self, props):
        if props.__len__() > 0:
            val = props['value']
            if val is not None:
                self._value = val
        if self._onclick_callback is not None:
            self._onclick_callback(self._name, props)

    def on_fire_change_event(self, props):
        if props.__len__() > 0:
            val = props['value']
            if val is not None:
                self._value = val
        if self._onchange_callback is not None:
            self._onchange_callback(self._name, props)

    def on_slider_clicked(self, onclick_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                onclick_callback (function): The function/callback that will be called for this event
        """
        self._onclick_callback = onclick_callback

    def on_slider_changed(self, onchange_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                onclick_callback (function): The function/callback that will be called for this event
        """
        self._onchange_callback = onchange_callback

    @property
    def animate(self):
        return self._animate

    @animate.setter
    def animate(self, val):
        self._animate = val
        self._sync_properties('animate', val)

    @property
    def disabled(self):
        """Returns the disabled state of the slider widget"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def max(self):
        """Returns the maximum value of the slider"""
        return self._max

    @max.setter
    def max(self, val):
        self._max = val
        self._sync_properties('max', val)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, val):
        self._min = val
        self._sync_properties('min', val)

    @property
    def orientation(self):
        """Returns the value of orientation of the slider"""
        return self._orientation

    @orientation.setter
    def orientation(self, val):
        self._orientation = val
        self._sync_properties('orientation', val)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, val):
        self._range = val
        self._sync_properties('range', val)

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, val):
        self._step = val
        self._sync_properties('step', val)

    @property
    def value(self):
        """Returns the current value of the slider"""
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._sync_properties('value', val)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, val):
        self._values = val
        self._sync_properties('values', val)

    def _attach_css(self):
        css = """<style>
                    #%s_handle {
                        width: 3em;
                        height: 1.6em;
                        top: 50%%;
                        margin-top: -.8em;
                        text-align: center;
                        line-height: 1.6em;
                    }
                </style>
            """ % (self._name)
        return css

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def render(self):
        """Renders the slider widget under parent widget
        """
        content = self._attach_css() + "\n"
        content += self._render_pre_content('div')
        content += "<div id='" + self._name + "_handle' class='ui-slider-handle'></div>"
        content += self._render_post_content('div')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content


class Spinner(Widget, Namespace):
    """The spinner widget enhances a text input for entring numeric values, with up/down
    buttons and arrow key handling. Spinner supports the functionality to have min & max
    fixed value, the starting point of the spinner, value of step for incremeting or
    decrementing the spinner's value and so on.
    """

    _name = None
    _namespace = None
    _socket_io = None
    _value = None
    _start = None
    _onchange_callback = None
    _culture = None
    _disabled = None
    _icons = None
    _incremental = None
    _max = None
    _min = None
    _number_format = None
    _page = None
    _step = None

    def __init__(self, name, socket_io, value=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, css_cls=None, min=None, max=None, start=None, step=None,
                 number_format=None, onchange_callback=None):
        """Default constructor of the Spinner widget class

            Args:
                name (string): name of the widget for internal use
                socket_io (SocketIO): A instance of SocketIO class
                value (int, optional): Current value of the spinner
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                css_cls (list, optional): An list of CSS class names to be added to current widget
                min (int, optional): Minimum value of the spinner widget. Default=0
                max (int, optional): The max range spinner can go upto. Default=100
                start (int, optional): The starting numer of the spinner. Default=0
                step (int, optional): The value by which spinner incr/decr its value. Default=1
                number_format (char, optional): The number format expected by Spinner
                onchange_callback (func, optional): The callable object to be called when sppiner's value changes
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_spinner").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_spinner").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._onchange_callback = onchange_callback
        self._disabled = disabled
        if value is not None:
            self._value = value
        else:
            self._value = 0
        if min is not None:
            self._min = min
        else:
            self._min = 0
        if max is not None:
            self._max = max
        else:
            self._max = 100
        if start is not None:
            self._start = start
        else:
            self._start = 0
        if step is not None:
            self._step = step
        else:
            self._step = 1
        if number_format is not None:
            self._number_format = number_format
        else:
            self._number_format = "n"
        if disabled is not None:
            self._disabled = disabled
        else:
            self._disabled = False

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def value(self):
        """The current value of the spinner widget"""
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def start(self):
        """Starting value of the spinner widget. NOTE: It is NOT same as `min`
        Default value is 0
        """
        return self._start

    @start.setter
    def start(self, val):
        self._start = val

    @property
    def culture(self):
        return self._culture

    @culture.setter
    def culture(self, val):
        self._culture = val
        self._sync_properties('culture', val)

    @property
    def disabled(self):
        """Whether to enable or disable the spinner widget"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def icons(self):
        return self._icons

    @icons.setter
    def icons(self, val):
        self._icons = val
        self._sync_properties('icons', val)

    @property
    def incremental(self):
        return self._incremental

    @incremental.setter
    def incremental(self, val):
        self._incremental = val
        self._sync_properties('incremental', val)

    @property
    def max(self):
        """The maximum value of spinner widget. Once it is reached, the number
        will not increment anymore
        Default value is 100
        """
        return self._max

    @max.setter
    def max(self, val):
        self._max = val
        self._sync_properties('max', val)

    @property
    def min(self):
        """The minium value allowed for the spinner widget
        Default value is 0
        """
        return self._min

    @min.setter
    def min(self, val):
        self._min = val
        self._sync_properties('min', val)

    @property
    def number_format(self):
        """Number format to be used by spinner widget
        Default value is "n"
        """
        return self._number_format

    @number_format.setter
    def number_format(self, val):
        self._number_format = val
        self._sync_properties('numberFormat', val)

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, val):
        self._page = val
        self._sync_properties('page', val)

    @property
    def step(self):
        """The value by which spinner widget will incr/decr its value
        Default value is 1
        """
        return self._step

    @step.setter
    def step(self, val):
        self._step = val
        self._sync_properties('step', val)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def _attach_script(self):
        script = ""
        script = """
                    <script>
                        $(function(){
                            var selector = $("#%s");
                            var socket = io("%s");

                            selector.spinner({
                                min: %d,
                                max: %d,
                                start: %d,
                                step: %d,
                                numberFormat: "%s",
                                stop: sendValue
                            });

                            function sendValue(){
                                var props = {
                                                'value': selector.spinner('value')
                                            };
                                socket.emit('fire_spinner_changed', props);
                            }

                            selector.on('spinchange', function(event){
                                var props = {
                                                'value': selector.spinner('value')
                                            };
                                socket.emit('fire_spinner_changed', props);
                            });

                            socket.on('sync_properties_%s', function(props){
                                selector.spinner('option', props['cmd'], props['value']);
                            });
                        });
                    </script>
                """ % (self._name, self._namespace, self._min, self._max, self._start, self._step,
                       self._number_format, self._name)
        return script

    def on_fire_spinner_changed(self, props):
        if props.__len__() > 0:
            val = props["value"]
            if val is not None:
                self._value = val
        if self._onchange_callback is not None:
            self._onchange_callback(self._name, props)

    def render(self):
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        content += "\n" + self._attach_script()
        self._widget_content = content
        return content


class TabSection(Widget):
    """Defines a section or panel in the Tab widget. A tab widget can have multiple
    sections associated with respective heading. By clicking on the header, a panel
    becomes active display's its content on top of other panels which goes behind
    the active panel virtually
    """

    _header = None
    _disabled = None

    def __init__(self, name, header, desc=None, prop=None, style=None, attr=None,
                 disabled=False, css_cls=None):
        """Default constructor of the TabSection widget class

            Args:
                name (string): name of the widget for internal use
                header (string): Current value of the spinner
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._header = header
        self._disabled = disabled

    @property
    def name(self):
        """The name or id of the widget. This is used internally and is a required
        field"""
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def header(self):
        """Header text of the tab panel section"""
        return self._header

    @header.setter
    def header(self, val):
        self._header = val

    def render(self):
        """Renders the panel or tab section to its parent tab widget"""
        content = self._render_pre_content('div')
        for widget in self._child_widgets:
            content += widget.render()
        content += self._render_post_content('div')
        self._widget_content = content
        return self._widget_content


class TabEvents(Enum):
    OPEN_ON_MOUSE_OVER = "mouseover"
    CLICK = "click"


class Tab(Widget, Namespace):
    """A tab widget to display multiple panel at the same place stacked over each other.
    A panel is made active and visible by clicking on the headers of the panel or section
    """

    _namespace = None
    _socket_io = None
    _sortable = None
    _v_orient = None
    _tab_activated_callback = None
    _active = None
    _collapsible = None
    _disabled = None
    _event = None
    _height_style = None
    _hide = None
    _show = None

    def __init__(self, name, socket_io, desc=None, prop=None, style=None, attr=None,
                 css_cls=None, collapsible=None, event=None,
                 sortable=None, v_orient=None, tab_activated_callback=None,
                 disabled=None, active=None):
        """Default constructor of the TabSection widget class

            Args:
                name (string): name of the widget for internal use
                socket_io (SocketIO): An instance of SocketIO
                header (string): Current value of the spinner
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                css_cls (list, optional): An list of CSS class names to be added to current widget
                collapsible (boolean, optional): Whether the active panel should collapse on re-click or not
                event (TabEvents, optional): Whether tab should be active on mouse hover instead of click
                sortable (boolean, optional): If true, allows to sort tabs using drag & drop
                v_orient (boolean, optional): Whether to render headers vertically instead of horizontally
                tab_activated_callback (callable, optional): Calls the function when an tab is activated
                disabled (boolean, optional): True or False to disable the whole tab widget or list
                of panel indices to disable individual tabs
                active (int, optional): Index of the selected tab in the widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_tab").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_tab").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        if collapsible is not None:
            self._collapsible = collapsible
        else:
            self._collapsible = False
        if event is not None:
            self._event = event
        else:
            self._event = TabEvents.CLICK.value
        if sortable is not None:
            self._sortable = sortable
        else:
            self._sortable = False
        if v_orient is not None:
            self._v_orient = v_orient
        else:
            self._v_orient = False
        self._tab_activated_callback = tab_activated_callback
        if disabled is not None:
            self._disabled = disabled
        else:
            self._disabled = False
        if active is not None:
            self._active = active
        else:
            self._active = 0

    @property
    def sortable(self):
        return self._sortable

    @sortable.setter
    def sortable(self, val):
        self._sortable = val
        self._sync_properties('sortable', val)

    @property
    def v_orient(self):
        return self._v_orient

    @v_orient.setter
    def v_orient(self, val):
        self._v_orient = val
        self._sync_properties('v_orient', val)

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val):
        self._active = val
        self._sync_properties('active', val)

    @property
    def collapsible(self):
        return self._collapsible

    @collapsible.setter
    def collapsible(self, val):
        self._collapsible = val
        self._sync_properties('collapsible', val)

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def event(self):
        if self._event == "click":
            return TabEvents.CLICK
        return TabEvents.OPEN_ON_MOUSE_OVER

    @event.setter
    def event(self, val):
        self._event = val.value
        self._sync_properties('event', val.value)

    @property
    def heightStyle(self):
        return self._heightStyle

    @heightStyle.setter
    def heightStyle(self, val):
        self._heightStyle = val
        self._sync_properties('heightStyle', val)

    @property
    def hide(self):
        return self._hide

    @hide.setter
    def hide(self, val):
        self._hide = val
        self._sync_properties('hide', val)

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        self._show = val
        self._sync_properties('show', val)

    def _attach_script(self):
        script = ""
        script = """<script>
                        $(function(){
                                var selector = $("#%s");
                                var socket = io("%s");

                                selector.tabs({
                                    collapsible: %s,
                                    event: "%s"
                                });

                                selector.on('tabsactivate', function(event, ui){
                                    var props = {'newTab': ui.newTab != undefined ? ui.newTab[0].id : "",
                                                 'oldTab': ui.oldTab != undefined ? ui.oldTab[0].id : "",
                                                 'newPanel': ui.newPanel != undefined ? ui.newPanel[0].id : "",
                                                 'oldPanel': ui.oldPanel != undefined ? ui.oldPanel[0].id : "",
                                                 'active': selector.tabs('option', 'active')}
                                    socket.emit('fire_tab_activated', props);
                                });

                                socket.on('sync_properties_%s', function(props){
                                    var cmd = props['cmd'];
                                    var value = props['value'];
                                    if(cmd === 'sortable' && value){
                                        selector.find( ".ui-tabs-nav" ).sortable({
                                            axis: "x",
                                            stop: function() {
                                                selector.tabs( "refresh" );
                                            }
                                        });
                                    } else if (cmd === 'v_orient' && value){
                                        selector.tabs().addClass( "ui-tabs-vertical ui-helper-clearfix" );
                                        selector.removeClass( "ui-corner-top" ).addClass( "ui-corner-left" );
                                    } else {
                                        selector.tabs('option', cmd, value);
                                    }
                                });
                            });

                            </script>
                            """ % (self._name, self._namespace, json.dumps(self._collapsible),
                                    self._event, self._name)
        return script

    def on_fire_tab_activated(self, props):
        if props.__len__() > 0:
            val = props['active'];
            if val is not None:
                self._active = val
        if self._tab_activated_callback is not None:
            self._tab_activated_callback(self._name, props)

    def _attach_css(self):
        css = ""
        if self._v_orient == "true":
            css = """<style>
                `       .ui-tabs-vertical { width: 55em; }
                        .ui-tabs-vertical .ui-tabs-nav { padding: .2em .1em .2em .2em; float: left; width: 12em; }
                        .ui-tabs-vertical .ui-tabs-nav li { clear: left; width: 100%; border-bottom-width: 1px !important; border-right-width: 0 !important; margin: 0 -1px .2em 0; }  /*  # noqa */
                        .ui-tabs-vertical .ui-tabs-nav li a { display:block; }
                        .ui-tabs-vertical .ui-tabs-nav li.ui-tabs-active { padding-bottom: 0; padding-right: .1em; border-right-width: 1px; }
                        .ui-tabs-vertical .ui-tabs-panel { padding: 1em; float: right; width: 40em;}
                    </style>
                """
        return css

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def render(self):
        content = self._attach_css() + "\n"
        content += self._render_pre_content('div')
        content += "\n" + "<ul>"
        for widget in self._child_widgets:
            content += "\n" + "<li id='" + widget.name + "'><a href='" + widget.name + "_a'>" + widget.header
            content += "</a></li>"
        content += "</ul>"
        for widget in self._child_widgets:
            content += "\n" + widget.render()
        content += self._render_post_content('div')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content
