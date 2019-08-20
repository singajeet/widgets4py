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

    @property
    def icon(self):
        """Returns JavaScript `dict` of CSS classes related to icons of sections"""
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val

    @property
    def fill_space(self):
        """Returns whether sections will be filled with space to match parent's
        height"""
        return self._fill_space

    @fill_space.setter
    def fill_space(self, val):
        self._fill_space = val

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
                            $("#%s").accordion({
                                collapsible: %s,
                                icons: %s,
                                heightStyle: "%s"
                            });
                        });
                        </script>
                    """ % (self._name, "true" if self._collapsible else "false",
                           self._icons, "fill" if self._fill_space else "")
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

                            selector_lbl.on("click", function(event){
                                    checkbox = event.currentTarget.nextSibling;
                                    var checked = {}
                                    selector.each(function(index, value){
                                        var id = $(this).attr("id");
                                        if(id != checkbox.id){
                                            checked[id] = false; //$(this).prop("checked");
                                        } else {
                                            checked[id] = !checkbox.checked;
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

                            selector_lbl.on("click", function(event){
                                checkbox = event.currentTarget.nextSibling;
                                var checked = {}
                                selector.each(function(index, value){
                                    var id = $(this).attr("id");
                                    if(id != checkbox.id){
                                        checked[id] = $(this).prop("checked");
                                    } else {
                                        checked[id] = !checkbox.checked;
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

    _title = None
    _namespace = None
    _socket_io = None
    _onok_pressed_callback = None
    _oncancel_pressed_callback = None
    _disabled = None
    _command = None
    _dialog_type = None
    _height = None
    _width = None
    _onbefore_close_callback = None
    _is_dialog_open = None

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

    @property
    def dialog_type(self):
        return self._dialog_type

    @dialog_type.setter
    def dialog_type(self, val):
        self._dialog_type = val
        self._sync_properties('dialog_type', val)

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
                                    } else if(cmd === 'title'){
                                        selector.dialog('option', 'title', value);
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
                                    } else if(cmd === 'title'){
                                        selector.dialog('option', 'title', value);
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

                                        //if(!isOpen){
                                            selector.dialog('open');
                                        //}
                                    } else if(cmd === 'close'){
                                        var isOpen = selector.dialog('isOpen');
                                        if(isOpen){
                                            selector.dialog('close');
                                        }
                                    } else if(cmd === 'title'){
                                        selector.dialog('option', 'title', value);
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

                                        //if(!isOpen){
                                            selector.dialog('open');
                                        //}
                                    } else if(cmd === 'close'){
                                        var isOpen = selector.dialog('isOpen');
                                        if(isOpen){
                                            selector.dialog('close');
                                        }
                                    } else if(cmd === 'title'){
                                        selector.dialog('option', 'title', value);
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

    _app = None
    _menu_type = None
    _socket_io = None
    _namespace = None

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
                                $('#%s').menu();
                            });
                        </script>
                    """ % (self._name)
        elif self._menu_type == MenuTypes.HORIZONTAL:
            script = """<script>$(function() {
                            $('#%s').menu();

                            $('#%s').menu({
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
                        });
                    </script>
                    """ % (self._name, self._name, self._name)
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


class Slider(Widget):
    """Slider class to render an slider widget on a page. This class provides
    the callback functionality whenever value is changed in the slider through
    mouse drag operation. The latest value of slider can be captured in the
    callback function
    """

    _value = None
    _app = None
    _onclick_callback = None
    _slider_changed_callback = None
    _disabled = None
    _orientation = None
    _max = None
    _app = None

    def __init__(self, name, value=None, orientation=None, max=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, onclick_callback=None, slider_changed_callback=None, app=None, css_cls=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
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
                app (Flask, optional): An instance of Flask class
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        if value is None:
            self._value = 0
        else:
            self._value = value
        self._app = app
        self._slider_changed_callback = slider_changed_callback
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
        self.add_property('onclick', self._attach_onclick())

    def _attach_onclick(self):
        ajax = ""
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """
                var val = $("#%s").slider('value')
                $.ajax({
                    url: "/%s",
                    dataType: "json",
                    data: {"value":  val},
                    type: "get",
                    success: function(status){alertify.success("Action completed successfully!");},
                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            }
                });
            """ % (self._name, url)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onclick_callback)
        return ajax

    def _process_onclick_callback(self):
        if request.args.__len__() > 0:
            val = request.args['value']
            if val is not None:
                self._value = val
        return json.dumps({"result": self._onclick_callback()})

    def on_click(self, onclick_callback, app=None):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function. If no app is associated with current widget, it should be
        linked by passing `app` param

            Args:
                onclick_callback (function): The function/callback that will be called for this event
                app (Flask, optional): An instance of Flask app, though this param is optional, it is
                                        required to have events work properly. So, it should be passed
                                        during creation of widget in the constructor or should be
                                        passed in this function
        """
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self.add_property('onclick', self._attach_onclick())

    def set_value(self, val):
        """Sets the initial value of the slider

            Args:
                val (int): An initial value of the slider
        """
        self._value = val

    def get_value(self):
        """Returns the current value of the slider

            Returns:
                int: current value of the slider
        """
        return self._value

    def set_orientation(self, val):
        """Sets the orientation of the slider either Horizontally or vertically

            Args:
                val (string): valid values are "horizontal" and "vartical"
        """
        self._orientation = val

    def get_orientation(self):
        """Returns the value of orientation of the slider

            Returns:
                string: horizontal or vertical
        """
        return self._orientation

    def set_max(self, val):
        """Sets the maximum value of the slider till it can reach

            Args:
                val (int): Maximum value of the slider
        """
        self._max = val

    def get_max(self):
        """Returns the maximum value of the slider

            Returns:
                int: Maximum value of slider
        """
        return self._max

    def set_disabled(self, val):
        """Sets the slider widget to disabled mode

            Args:
                val (boolean): true or false as required
        """
        self._disabled = val

    def get_disabled(self):
        """Returns the disabled state of the slider widget

            Returns:
                boolean: true or false
        """
        return self._disabled

    def _attach_script(self):
        script = ""
        if self._app is not None:
            url = str(__name__ + "_" + self._name + "_slider_changed").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            script = """<script>
                        $(function(){
                            var handle = $('#%s_handle');
                            $('#%s').slider({
                                orientation: "%s",
                                max: %d,
                                value: %d,
                                change: refreshValue,
                                create: function() {
                                    handle.text( $( this ).slider( "value" ) );
                                },
                                slide: function( event, ui ) {
                                    handle.text( ui.value );
                                }
                             });
                            function refreshValue(){
                                var val = $("#%s").slider("value");
                                $.ajax({
                                    url: "/%s",
                                    type: "get",
                                    data: {"value": val},
                                    dataType: "json",
                                    success: function(status){alertify("Action completed successfully!");},
                                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                    }
                                });
                            }
                        });
                    </script>
                """ % (self._name, self._name, self._orientation, self._max, self._value, self._name, url)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_slider_changed_callback)
        return script

    def _process_slider_changed_callback(self):
        if request.args.__len__() > 0:
            val = request.args['value']
            if val is not None:
                self._value = val
        if self._slider_changed_callback is not None:
            return json.dumps({'result': self._slider_changed_callback()})
        return json.dumps({'result': ''})

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

    def _sync_properties(self):
        return json.dumps({'value': self._value,
                           'orientation': self._orientation,
                           'max': self._max,
                           'disabled': self._disabled
                           })

    def _attach_polling(self):
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                        (function %s_poll(){
                            setTimeout(function(){
                                $.ajax({
                                    url: "/%s",
                                    success: function(props){
                                        selector = $('#%s');
                                        //fill up the values
                                        if(props.value != undefined){
                                            var existing_val = selector.slider('option', 'value');
                                            if(existing_val != props.value){
                                                selector.slider('option', 'value', props.value);
                                            }
                                        }
                                        if(props.max != undefined){
                                            selector.slider('option', 'max', props.max);
                                        }
                                        if(props.orientation != undefined){
                                            selector.slider('option', 'orientation', props.orientation);
                                        }
                                        if(props.disabled != undefined){
                                            selector.slider('option', 'disabled', props.disabled);
                                        }
                                        //poll again
                                        %s_poll();
                                    },
                                    error: function(err_status){
                                                                alertify.error("Status Code: "
                                                                + err_status.status + "<br />" + "Error Message:"
                                                                + err_status.statusText);
                                                            },
                                    dataType: "json"
                                });
                            },500);
                        })();
                    </script>
                """ % (url, url, self._name, url)
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == url:
                found = True
        if not found:
            self._app.add_url_rule('/' + url, url,
                                   self._sync_properties)
        return script

    def render(self):
        """Renders the slider widget under parent widget
        """
        content = self._attach_css() + "\n"
        content += self._render_pre_content('div')
        content += "<div id='" + self._name + "_handle' class='ui-slider-handle'></div>"
        content += self._render_post_content('div')
        self._widget_content = content + "\n" + self._attach_script() + "\n" + self._attach_polling()
        return self._widget_content


class Spinner(Widget):
    """The spinner widget enhances a text input for entring numeric values, with up/down
    buttons and arrow key handling. Spinner supports the functionality to have min & max
    fixed value, the starting point of the spinner, value of step for incremeting or
    decrementing the spinner's value and so on.
    """

    _name = None
    _app = None
    _disabled = None
    _min = None
    _max = None
    _start = None
    _step = None
    _number_format = None
    _value = None
    _onchange_callback = None

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, app=None, css_cls=None, min=None, max=None, start=None, step=None,
                 number_format=None, onchange_callback=None):
        """Default constructor of the Spinner widget class

            Args:
                name (string): name of the widget for internal use
                value (int, optional): Current value of the spinner
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                app (Flask, optional): An instance of Flask class
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
        self._app = app
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
    def value(self):
        """The current value of the spinner widget"""
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def min(self):
        """The minium value allowed for the spinner widget
        Default value is 0
        """
        return self._min

    @min.setter
    def min(self, val):
        self._min = val

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
    def step(self):
        """The value by which spinner widget will incr/decr its value
        Default value is 1
        """
        return self._step

    @step.setter
    def step(self, val):
        self._step = val

    @property
    def number_format(self):
        """Number format to be used by spinner widget
        Default value is "n"
        """
        return self._number_format

    @number_format.setter
    def number_format(self, val):
        self._number_format = val

    @property
    def disabled(self):
        """Whether to enable or disable the spinner widget"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val

    def _sync_properties(self):
        return json.dumps({'min': self._min,
                           'max': self._max,
                           'start': self._start,
                           'step': self._step,
                           'numberFormat': self._number_format,
                           'value': self._value,
                           'disabled': self._disabled
                           })

    def _attach_polling(self):
        script = ""
        if self._app is not None:
            url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
            script = """<script>
                        (function %s_poll(){
                            setTimeout(function(){
                                $.ajax({
                                    url: "/%s",
                                    success: function(props){
                                        selector = $('#%s');
                                        //fill up the values
                                        if(props.value != undefined){
                                            var existing_val = selector.spinner('value');
                                            if(existing_val != props.value){
                                                selector.spinner('value', props.value);
                                            }
                                        }
                                        if(props.max != undefined){
                                            selector.spinner('option', 'max', props.max);
                                        }
                                        if(props.min != undefined){
                                            selector.spinner('option', 'min', props.min);
                                        }
                                        if(props.start != undefined){
                                            selector.spinner('option', 'start', props.start);
                                        }
                                        if(props.step != undefined){
                                            selector.spinner('option', 'step', props.step);
                                        }
                                        if(props.numberFormat != undefined){
                                            selector.spinner('option', 'numberFormat', props.numberFormat);
                                        }
                                        if(props.disabled != undefined){
                                            selector.spinner('option', 'disabled', props.disabled);
                                        }
                                        //poll again
                                        %s_poll();
                                    },
                                    error: function(err_status){
                                                                alertify.error("Status Code: "
                                                                + err_status.status + "<br />" + "Error Message:"
                                                                + err_status.statusText);
                                                            },
                                    dataType: "json"
                                });
                            },500);
                        })();
                    </script>
                """ % (url, url, self._name, url)
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._sync_properties)
        return script

    def _attach_script(self):
        script = ""
        found = True
        if self._app is not None:
            url = str(__name__ + "_" + self._name + "_spinner_changed").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
        script = """
                    <script>
                        $(function(){
                            $("#%s").spinner({
                                min: %d,
                                max: %d,
                                start: %d,
                                step: %d,
                                numberFormat: "%s",
                                stop: refreshValue
                            });
                """ % (self._name, self._min, self._max, self._start, self._step,
                       self._number_format)
        if self._app is not None:
            script += """
                            var selector = $("#%s");
                            function refreshValue(){
                                $.ajax({
                                    url: "/%s",
                                    type: "get",
                                    dataType: "json",
                                    data: {"value": selector.val()},
                                    success: function(status){alertify("Action completed successfully!");},
                                    error: function(err_status){
                                            alertify.error("Status Code: "
                                            + err_status.status + "<br />" + "Error Message:"
                                            + err_status.statusText);
                                    }
                                });
                            }
                        });
                    </script>
                """ % (self._name, url)
        else:
            script += """
                        function refreshValue(){}
                        });
                        </script>
                    """
        if not found:
            self._app.add_url_rule('/' + url, url,
                                   self._process_spinner_changed_callback)
        return script

    def _process_spinner_changed_callback(self):
        if request.args.__len__() > 0:
            val = request.args["value"]
            if val is not None:
                self._value = val
        if self._onchange_callback is not None:
            return json.dumps({'result': self._onchange_callback()})
        return json.dumps({'result': ''})

    def render(self):
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        content += "\n" + self._attach_script()
        content += "\n" + self._attach_polling()
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


class Tab(Widget):
    """A tab widget to display multiple panel at the same place stacked over each other.
    A panel is made active and visible by clicking on the headers of the panel or section
    """

    _collapsible = None
    _open_on_mouseover = None
    _sortable = None
    _v_orient = None
    _tab_activated_callback = None
    _app = None
    _disabled = None
    _selected_index = None

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 app=None, css_cls=None, collapsible=None, open_on_mouseover=None,
                 sortable=None, v_orient=None, tab_activated_callback=None,
                 disabled=None, selected_index=None):
        """Default constructor of the TabSection widget class

            Args:
                name (string): name of the widget for internal use
                header (string): Current value of the spinner
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                app (Flask, optional): An instance of Flask app
                css_cls (list, optional): An list of CSS class names to be added to current widget
                collapsible (boolean, optional): Whether the active panel should collapse on re-click or not
                open_on_mouseover (boolean, optional): Whether tab should be active on mouse hover instead of click
                sortable (boolean, optional): If true, allows to sort tabs using drag & drop
                v_orient (boolean, optional): Whether to render headers vertically instead of horizontally
                tab_activated_callback (callable, optional): Calls the function when an tab is activated
                disabled (boolean, optional): True or False to disable the whole tab widget or list
                of panel indices to disable individual tabs
                selected_index (int, optional): Index of the selected tab in the widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        if collapsible is not None:
            self._collapsible = collapsible
        else:
            self._collapsible = False
        if open_on_mouseover is not None and open_on_mouseover:
            self._open_on_mouseover = "mouseover"
        else:
            self._open_on_mouseover = "click"
        if sortable is not None:
            self._sortable = sortable
        else:
            self._sortable = False
        if v_orient is not None:
            self._v_orient = v_orient
        else:
            self._v_orient = False
        self._tab_activated_callback = tab_activated_callback
        self._app = app
        if disabled is not None:
            self._disabled = disabled
        else:
            self._disabled = False
        if selected_index is not None:
            self._selected_index = selected_index
        else:
            self._selected_index = 0

    @property
    def collapsible(self):
        return self._collapsible

    @collapsible.setter
    def collapsible(self, val):
        self._collapsible = val

    @property
    def open_on_mouseover(self):
        return self._open_on_mouseover

    @open_on_mouseover.setter
    def open_on_mouseover(self, val):
        self._open_on_mouseover = val

    @property
    def selected_index(self):
        """Value or Index of the selected section or panel under Tab widget
        """
        return self._selected_index

    @selected_index.setter
    def selected_index(self, val):
        self._selected_index = val

    def _attach_script(self):
        script = ""
        found = True
        if self._app is not None:
            url = str(__name__ + "_" + self._name + "_tab_activated").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
        script = """<script>
                        $(function(){
                            var selector = $("#%s");
                            selector.tabs({
                                collapsible: %s,
                                event: "%s",
                                activate: tabActivated
                            });
                            var sortable = %s
                            if(sortable){
                                selector.find( ".ui-tabs-nav" ).sortable({
                                    axis: "x",
                                    stop: function() {
                                    selector.tabs( "refresh" );
                                    }
                                });
                            }
                            var v_orient = %s
                            if(v_orient){
                                selector.tabs().addClass( "ui-tabs-vertical ui-helper-clearfix" );
                                selector.removeClass( "ui-corner-top" ).addClass( "ui-corner-left" );
                            }""" % (self._name, json.dumps(self._collapsible),
                                    self._open_on_mouseover, json.dumps(self._sortable),
                                    self._v_orient)
        if self._app is not None and self._tab_activated_callback is not None:
            script += """function tabActivated(event, ui){
                            $.ajax({
                                url: "/%s",
                                type: "get",
                                dataType: "json",
                                data: {'selected_index': selector.tabs("option", "active")},
                                success: function(){alertify("Done!");},
                                error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            }
                        });
                    </script>
                """ % (url)
        else:
            script += """
                            function tabActivated(event, ui){}
                            });</script>
                        """
        if not found:
            self._app.add_url_rule('/' + url, url,
                                   self._process_tab_activated_callback)
        return script

    def _process_tab_activated_callback(self):
        if request.args.__len__() > 0:
            val = request.args['selected_index']
            if val is not None:
                self._selected_index = val
        if self._tab_activated_callback is not None:
            return json.dumps({'result': self._tab_activated_callback()})
        return json.dumps({'result': ''})

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

    def _sync_properties(self):
        return json.dumps({'collapsible': self._collapsible,
                           'open_on_mouseover': self._open_on_mouseover,
                           'sortable': self._sortable,
                           'selected_index': self._selected_index,
                           'disabled': self._disabled
                           })

    def _attach_polling(self):
        script = ""
        if self._app is not None:
            url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
            script = """<script>
                        (function %s_poll(){
                            setTimeout(function(){
                                $.ajax({
                                    url: "/%s",
                                    success: function(props){
                                        selector = $('#%s');
                                        //fill up the values
                                        if(props.selected_index != undefined){
                                            var existing_val = selector.tabs('option', 'active');
                                            if(existing_val != props.selected_index){
                                                selector.tabs('option', 'active', props.selected_index);
                                            }
                                        }
                                        if(props.collapsible != undefined){
                                            selector.tabs('option', 'collapsible', props.collapsible);
                                        }
                                        if(props.open_on_mouseover != undefined){
                                            selector.tabs('option', 'event', props.open_on_mouseover);
                                        }
                                        if(props.sortable != undefined){
                                            selector.tabs('option', 'sortable', props.sortable);
                                        }
                                        if(props.disabled != undefined){
                                            selector.tabs('option', 'disabled', props.disabled);
                                        }
                                        //poll again
                                        %s_poll();
                                    },
                                    error: function(err_status){
                                                                alertify.error("Status Code: "
                                                                + err_status.status + "<br />" + "Error Message:"
                                                                + err_status.statusText);
                                                            },
                                    dataType: "json"
                                });
                            },500);
                        })();
                    </script>
                """ % (url, url, self._name, url)
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._sync_properties)
        return script

    def render(self):
        content = self._attach_css() + "\n"
        content += self._render_pre_content('div')
        content += "\n" + "<ul>"
        for widget in self._child_widgets:
            content += "\n" + "<li><a href='" + widget.name + "'>" + widget.header
            content += "</a></li>"
        content += "</ul>"
        for widget in self._child_widgets:
            content += "\n" + widget.render()
        content += self._render_post_content('div')
        self._widget_content = content + self._attach_script() + "\n" + self._attach_polling()
        return self._widget_content
