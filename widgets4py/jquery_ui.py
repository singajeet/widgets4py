"""HTML Widgets based on the JQuery UI framework
Author: Ajeet Singh
Date: 06/25/2019
"""
from widgets4py.base import Widget
from flask import request, json
from enum import Enum


class Section(Widget):
    """Section class renders an section with title in an Accordion.
        This class can have further widgets as its children and same
        will be rendered within the section itself.
    """

    _title = None
    _app = None
    _onclick_callback = None
    _disabled = None
    _required = None

    def __init__(self, name, title, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, onclick_callback=None, app=None, css_cls=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                required (Boolean, optional): Widget is required to be filled-in or not
                onclick_callback (function, optional): A function to be called back on onclick event
                app (Flask, optional): An instance of Flask class
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._title = title
        self._app = app
        self._onclick_callback = onclick_callback
        self._disabled = disabled
        self._required = required

    def _attach_onclick(self):
        ajax = ""
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """
                var val = $("#%s_h3").text();
                $.ajax({
                    url: "/%s",
                    type: "get",
                    dataType: "json",
                    data: {"title":  val},
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
            tit = request.args['title']
            if tit is not None:
                self._title = tit
            # dsbld = request.args['disabled']
            # if dsbld is not None:
            #     self._disabled = True if dsbld == "true" else False
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

    def render(self):
        content = "<h3 id='" + self._name + "_h3' "\
            + "onclick='" + self._attach_onclick() + "' >"\
            + self._title + "</h3>\n"
        content += self._render_pre_content('div')
        for widget in self._child_widgets:
            content += "\n" + widget.render()
        content += self._render_post_content('div')
        self._widget_content = content
        return self._widget_content


class Accordion(Widget):
    """Class to render an accordion widget and its sections built using the
    `Section` class of this module.
    """

    _app = None
    _onclick_callback = None
    _disabled = None
    _required = None
    _collapsible = None
    _icons = None
    _fill_space = None

    def __init__(self, name, collapsible=False, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, onclick_callback=None, app=None, css_cls=None,
                 icons=None, fill_space=False):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                required (Boolean, optional): Widget is required to be filled-in or not
                onclick_callback (function, optional): A function to be called back on onclick event
                app (Flask, optional): An instance of Flask class
                css_cls (list, optional): An list of CSS class names to be added to current widget
                collapsible (boolean, optional): Whether to have all sections collapsible
                fill_space (boolean, optional): Fill the vertical space to match the parent container's
                                                height
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._app = app
        self._onclick_callback = onclick_callback
        self._disabled = disabled
        self._required = required
        self._collapsible = collapsible
        if icons is not None:
            self._icons = icons
        else:
            self._icons = {}
        self._fill_space = fill_space

    def set_collapsible(self, value):
        """Sets whether to have all sections as collapsible or not

            Args:
                value (boolean): True or False to have sections collapsible or not
        """
        self._collapsible = value

    def get_collapsible(self):
        """Returns whether the sections are collapsible or not

            Returns:
                boolean: True or False based on the sections state
        """
        return self._collapsible

    def set_icons(self, value):
        """Sets the icons to be used. The value of parameter should be a `dict`
        (JavaScript dict)of objects as shown below

            Example:
                icons = {
                            header: "ui-icon-circle-arrow-e",
                            activeHeader: "ui-icon-circle-arrow-s"
                        };
            Args:
                value (str): An JavaScript `dict` of CSS classes as shown in the example
        """
        self._icons = value

    def get_icons(self):
        """Returns JavaScript `dict` of CSS classes related to icons of sections

            Returns:
                str: Icon css classes for Accordion sections
        """
        return self._icons

    def set_fill_space(self, val):
        """Whether to fill the vertical height of section with space to match the
        height of parent containet

            Args:
                val (boolean): True or False as required
        """
        self._fill_space = val

    def get_fill_space(self):
        """Returns whether sections will be filled with space to match parent's
        height

            Returns:
                boolean: True or False
        """
        return self._fill_space

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


class RadioButtonGroup(Widget):
    """Widget to display options provided in `dict` object as RadioButton grouped
    together under a title passed as parameter
    """

    _title = None
    _items = None
    _show_icon = None
    _app = None
    _onclick_callback = None
    _value = None
    _disabled_buttons = None

    def __init__(self, name, title, items, show_icon=True, desc=None, prop=None, style=None, attr=None,
                 onclick_callback=None, app=None, css_cls=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the Radio button group
                items (dict): A dict object containing items in the following format...
                                {'key1': ['title1', false]} false means radio will be shown unselected
                show_icon (boolean, optional): whether to show icon or not, default is true
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                onclick_callback (function, optional): A function to be called back on onclick event
                app (Flask, optional): An instance of Flask class
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._title = title
        self._items = items
        self._show_icon = show_icon
        self._app = app
        self._onclick_callback = onclick_callback
        self._disabled_buttons = {}

    def set_disable(self, btn, state):
        """Sets whether the passed radio button should be set as disabled or not

            Args:
                btn (string): Name of the radio button that exists in this group
                state (boolean): True or False
        """
        if self._disabled_buttons is None:
            self._disabled_buttons = {}
        self._disabled_buttons[btn] = state

    def get_disable(self, btn):
        """Returns the state of the radio button passed as parameter

            Args:
                btn (string): Name of the radio button that exists in the ths group
            Returns:
                boolean: True or False based on current state
        """
        return self._disabled_buttons[btn]

    def _attach_script(self):
        script = """<script>
                        $(function(){
                            $("input[id^='%s_rd']").checkboxradio({
                                icon: %s
                            });
                        });
                    </script>
                """ % (self._name, "true" if self._show_icon else "false")
        return script

    def _attach_onclick(self, item):
        ajax = ""
        found = False
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            name = (self._name + "_rd_" + item)
            ajax = """
                    var full_id = $("#%s").prop("id");
                    var index = $("#%s").prop("id").indexOf("rd_") + 3; //3=len(rd_)
                    var id = $("#%s").prop("id").substr(index);
                    $.ajax({
                        url: "/%s",
                        dataType: "json",
                        type: "get",
                        data: {"value": id},
                        success: function(status){alertify.success("Action completed successfully!");},
                        error: function(err_status){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                                }
                    });
                """ % (name, name, name, url)
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
        for item in self._items:
            self._attach_onclick(item)

    def set_value(self, val):
        """Set the value of RadioButtonGroup widget's value to the one passed as parameter

            Args:
                val (str): Value passed from RadioButtonGroup widget
        """
        self._value = val

    def get_value(self):
        """Returns the selected value of the RadioButtonGroup

            Returns:
                str: The selected value from the group
        """
        return self._value

    def _sync_properties(self):
        return json.dumps({'name': self._name,
                           'value': self._value,
                           'disabled': json.dumps(self._disabled_buttons)
                           })

    def _attach_polling(self):
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                        (function %s_poll(){
                            setTimeout(function(){
                                $.ajax({
                                    url: "/%s",
                                    success: function(props){
                                        id = props.name + "_rd_" + props.value;
                                        selector = $("#" + id);
                                        if(selector != undefined){
                                            selector.prop('checked', true);
                                            $('input[name^="' + props.name + '_rd"]').checkboxradio('refresh');
                                        }
                                        if(props.disabled != undefined && props.disabled != "")
                                        {
                                            radios = JSON.parse(props.disabled);
                                            for(index in radios){
                                                rd = props.name + "_rd_" + index;
                                                if(radios[index]){
                                                    $('#' + rd).checkboxradio('disable');
                                                }
                                                else{
                                                    $('#' + rd).checkboxradio('enable');
                                                }
                                            }
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
                            },10000);
                        })();
                    </script>
                """ % (url, url, url)
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == url:
                found = True
        if not found:
            self._app.add_url_rule('/' + url, url,
                                   self._sync_properties)
        return script

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
                + " name='" + self._name + "_rd'"\
                + " onclick='" + self._attach_onclick(item) + "' />"
            content += "\n" + label + "\n" + radio
        self._widget_content = content + "\n</fieldset>"\
                                       + self._attach_script() + "\n"\
                                       + self._attach_polling()
        return self._widget_content


class CheckBoxGroup(RadioButtonGroup):
    """Widget to display options provided in `dict` object as CheckBox grouped
    together under a title passed as parameter
    """

    def __init__(self, name, title, items, show_icon=True, desc=None, prop=None, style=None, attr=None,
                 onclick_callback=None, app=None, css_cls=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the Checkbox button group
                items (dict): A dict object containing items in the following format...
                                {'key1': ['title1', false]} false means radio will be shown unselected
                show_icon (boolean, optional): whether to show icon or not, default is true
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                onclick_callback (function, optional): A function to be called back on onclick event
                app (Flask, optional): An instance of Flask class
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        RadioButtonGroup.__init__(self, name, title, items, show_icon=show_icon, desc=desc, prop=prop,
                                  style=style, attr=attr, css_cls=css_cls, onclick_callback=onclick_callback,
                                  app=app)
        self._value = {}
        for item in items:
            record = items.get(item)
            is_checked = record[1]
            self._value[item] = is_checked

    def _attach_script(self):
        script = """<script>
                        $(function(){
                            $("input[id^='%s_chk']").checkboxradio({
                                icon: %s
                            });
                        });
                    </script>
                """ % (self._name, "true" if self._show_icon else "false")
        return script

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
        for item in self._items:
            self._attach_onclick(item)

    def _attach_onclick(self, item):
        ajax = ""
        found = False
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            name = (self._name + "_chk_" + item)
            ajax = """
                    var full_id = $("#%s").prop("id");
                    var index = $("#%s").prop("id").indexOf("chk_") + 4; //4=len(chk_)
                    var id = $("#%s").prop("id").substr(index);
                    $.ajax({
                        url: "/%s",
                        dataType: "json",
                        type: "get",
                        data: {"key": id},
                        success: function(status){alertify.success("Action completed successfully!");},
                        error: function(err_status){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                                }
                    });
                """ % (name, name, name, url)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onclick_callback)
        return ajax

    def _process_onclick_callback(self):
        if request.args.__len__() > 0:
            key = request.args['key']
            if key is not None:
                if self._value is not None:
                    existing_val = self._value.get(key)
                    if existing_val is not None:
                        self._value[key] = not self._value.get(key)
                    else:
                        self._value[key] = True
                else:
                    self._value = {key: True}
        return json.dumps({"result": self._onclick_callback()})

    def _sync_properties(self):
        return json.dumps({'name': self._name,
                           'value': json.dumps(self._value),
                           'disabled': json.dumps(self._disabled_buttons)
                           })

    def _attach_polling(self):
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                        (function %s_poll(){
                            setTimeout(function(){
                                $.ajax({
                                    url: "/%s",
                                    success: function(props){
                                        checks = JSON.parse(props.value)
                                        for(check in checks){
                                            id = props.name + "_chk_" + check;
                                            selector = $("#" + id);
                                            if(selector != undefined){
                                                selector.prop('checked', checks[check]);
                                                $('input[name^="' + props.name + '_chk"]').checkboxradio('refresh');
                                            }
                                        }
                                        if(props.disabled != undefined && props.disabled != "")
                                        {
                                            checks = JSON.parse(props.disabled);
                                            for(index in checks){
                                                cb = props.name + "_chk_" + index;
                                                if(checks[index]){
                                                    $('#' + cb).checkboxradio('disable');
                                                }
                                                else{
                                                    $('#' + cb).checkboxradio('enable');
                                                }
                                            }
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
                            },10000);
                        })();
                    </script>
                """ % (url, url, url)
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == url:
                found = True
        if not found:
            self._app.add_url_rule('/' + url, url,
                                   self._sync_properties)
        return script

    def render(self):
        """Renders the checkbox group with title passed as param
        """
        content = "<fieldset>\n<legend>" + self._title + "</legend>\n"
        for item in self._items:
            val = self._items.get(item)
            title = val[0]
            is_sel = val[1]
            name = self._name + "_chk_" + item
            lbl_name = self._name + "_lbl_" + item
            label = "<label for='" + name + "' id='" + lbl_name + "' >"\
                + (title if title is not None else item) + "</label>"
            checkbox = "<input id='" + name + "' type='checkbox'"\
                + (" checked" if is_sel else "")\
                + " name='" + self._name + "_chk'"\
                + " onclick='" + self._attach_onclick(item) + "' />"
            content += "\n" + label + "\n" + checkbox
        self._widget_content = content + "\n</fieldset>"\
                                       + self._attach_script() + "\n"\
                                       + self._attach_polling()
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


class DialogBox(Widget):
    """Class to shown dialog boxes which is on overlay position within the viewport.
     It has a title bar and a content area, and can be moved, resized and closed with the 'x' icon by default.
     """

    _title = None
    _app = None
    _onok_pressed_callback = None
    _oncancel_pressed_callback = None
    _disabled = None
    _command = None
    _dialog_type = None
    _height = None
    _width = None
    _onbefore_close_callback = None

    def __init__(self, name, title, dlg_type, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, app=None, css_cls=None, height=400, width=350,
                 onbefore_close_callback=None, onok_pressed_callback=None,
                 oncancel_pressed_callback=None):
        """Default constructor of the Label widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                dlg_type (DialogType): The type of the dialog box that needs to be created
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                disabled (Boolean, optional): Enabled or Disabled state of widget
                onclick_callback (function, optional): A function to be called back on onclick event
                app (Flask, optional): An instance of Flask class
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
        self._title = title
        self._app = app
        self._onok_pressed_callback = onok_pressed_callback
        self._oncancel_pressed_callback = oncancel_pressed_callback
        self._disabled = disabled
        self._dialog_type = dlg_type
        self._height = height
        self._width = width
        self._onbefore_close_callback = onbefore_close_callback
        self.add_property('title', title)

    def open(self):
        """Opens the dialog box
        """
        self._command = "open"

    def close(self):
        """Closes the dialog box
        """
        self._command = "close"

    def _onbefore_close_event(self):
        self._command = "close"
        if self._onbefore_close_callback is not None:
            return json.dumps({'result': self._onbefore_close_callback()})
        else:
            return json.dumps({'result': ''})

    def _onok_pressed_event(self):
        if self._onok_pressed_callback is not None:
            return json.dumps({'result': self._onok_pressed_callback()})
        else:
            return json.dumps({'result': ''})

    def _oncancel_pressed_event(self):
        if self._oncancel_pressed_callback is not None:
            return json.dumps({'result': self._oncancel_pressed_callback()})
        else:
            return json.dumps({'result': ''})

    def _sync_properties(self):
        return json.dumps({'title': self._title,
                           'command': self._command
                           })

    def _attach_polling(self):
        script = ""
        if self._app is not None:
            url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
            script = """<script>
            (function %s_poll(){
                setTimeout(function(){
                $.ajax({
                    url: '/%s',
                    success: function(props){
                        selector = $('#%s');
                        if (props.command == 'open'){
                            var isOpen = selector.dialog('isOpen');
                            if (!isOpen){
                                selector.dialog('open');
                            }
                        }else if (props.command == 'close'){
                            var isOpen = selector.dialog('isOpen');
                            if (isOpen){
                                selector.dialog('close');
                            }
                        }
                        if (props.title != selector.dialog('option', 'title')){
                            selector.dialog('option', 'title', props.title);
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
                },10000);
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

    def on_before_close(self, onbefore_close_callback, app=None):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function. If no app is associated with current widget, it should be
        linked by passing `app` param

            Args:
                onbefore_close_callback (function): The function/callback that will be
                                                    called for this event
                app (Flask, optional): An instance of Flask app, though this param is optional, it is
                                        required to have events work properly. So, it should be passed
                                        during creation of widget in the constructor or should be
                                        passed in this function
        """
        if app is not None:
            self._app = app
        self._onbefore_close_callback = onbefore_close_callback

    def on_ok_pressed(self, onok_pressed_callback, app=None):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function. If no app is associated with current widget, it should be
        linked by passing `app` param

            Args:
                onok_pressed_callback (function): The function/callback that will be
                                                    called for this event
                app (Flask, optional): An instance of Flask app, though this param is optional, it is
                                        required to have events work properly. So, it should be passed
                                        during creation of widget in the constructor or should be
                                        passed in this function
        """
        if app is not None:
            self._app = app
        self._onok_pressed_callback = onok_pressed_callback

    def on_cancel_pressed(self, oncancel_pressed_callback, app=None):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function. If no app is associated with current widget, it should be
        linked by passing `app` param

            Args:
                oncancel_pressed_callback (function): The function/callback that will be
                                                        called for this event
                app (Flask, optional): An instance of Flask app, though this param is optional, it is
                                        required to have events work properly. So, it should be passed
                                        during creation of widget in the constructor or should be
                                        passed in this function
        """
        if app is not None:
            self._app = app
        self._oncancel_pressed_callback = oncancel_pressed_callback

    def _attach_script(self, dlg_type):  # noqa
        if self._app is not None:
            before_close_url = str(__name__ + "_" + self._name + "_onbefore_close").replace('.', '_')
            ok_pressed_url = str(__name__ + "_" + self._name + "_onok_pressed").replace('.', '_')
            cancel_pressed_url = str(__name__ + "_" + self._name +
                                     "_oncancel_pressed").replace('.', '_')
            # before close url rule
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == before_close_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + before_close_url, before_close_url,
                                       self._onbefore_close_event)
            # ok pressed url rule
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == ok_pressed_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + ok_pressed_url, ok_pressed_url,
                                       self._onok_pressed_event)
            # cancel pressed url rule
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == cancel_pressed_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + cancel_pressed_url, cancel_pressed_url,
                                       self._oncancel_pressed_event)
        script = ""
        if dlg_type == DialogTypes.DEFAULT:
            script = """<script>
                            $(function(){
                                $("#%s").dialog({
                                    autoOpen: false,
                                    resizable: true,
                                    beforeClose: function(event, ui){
                                        $.ajax({
                                            url: '/%s',
                                            type: 'get',
                                            dataType: "json",
                                            success: function(status){},
                                            error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            }
                                        });
                                    }
                                });
                            });
                        </script>
                    """ % (self._name, before_close_url)
        elif dlg_type == DialogTypes.MODAL_CONFIRM:
            script = """<script>
                            $(function(){
                                $("#%s").dialog({
                                    autoOpen: false,
                                    resizable: false,
                                    height: %d,
                                    width: %d,
                                    modal: true,
                                    buttons: {
                                        "Ok": function(){
                                            //Call the OK pressed callback or endpoint
                                            $.ajax({
                                                url: '/%s',
                                                type: 'get',
                                                dataType: 'json',
                                                success: function(status){},
                                                error: function(err_status){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                                }
                                            });
                                            $(this).dialog('close');
                                        },
                                        "Cancel": function(){
                                            //Call the CANCEL pressed callback or endpoint
                                            $.ajax({
                                                url: '/%s',
                                                type: 'get',
                                                dataType: 'json',
                                                success: function(status){},
                                                error: function(err_status){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                                }
                                            });
                                            $(this).dialog('close');
                                        }
                                    },
                                    beforeClose: function(event, ui){
                                        $.ajax({
                                            url: '/%s',
                                            type: 'get',
                                            dataType: "json",
                                            success: function(status){},
                                            error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            }
                                        });
                                    }
                                });
                            });
                        </script>
                    """ % (self._name, self._height, self._width, ok_pressed_url,
                           cancel_pressed_url, before_close_url)
        elif dlg_type == DialogTypes.MODAL_FORM:
            script = """<script>
                            $(function(){
                                $("#%s").dialog({
                                    autoOpen: false,
                                    resizable: true,
                                    height: %d,
                                    width: %d,
                                    modal: true,
                                    buttons: {
                                        "Ok": function(){
                                            //Call the OK pressed callback or endpoint
                                            $.ajax({
                                                url: '/%s',
                                                type: 'get',
                                                dataType: 'json',
                                                success: function(status){},
                                                error: function(err_status){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                                }
                                            });
                                            $(this).dialog('close');
                                        },
                                        "Cancel": function(){
                                            //Call the CANCEL pressed callback or endpoint
                                            $.ajax({
                                                url: '/%s',
                                                type: 'get',
                                                dataType: 'json',
                                                success: function(status){},
                                                error: function(err_status){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                                }
                                            });
                                            $(this).dialog('close');
                                        }
                                    },
                                    beforeClose: function(event, ui){
                                        $.ajax({
                                            url: '/%s',
                                            type: 'get',
                                            dataType: "json",
                                            success: function(status){},
                                            error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            }
                                        });
                                    }

                                });
                            });
                        </script>
                    """ % (self._name, self._height, self._width, ok_pressed_url,
                           cancel_pressed_url, before_close_url)
        elif dlg_type == DialogTypes.MODAL_MESSAGE:
            script = """<script>
                            $(function(){
                                $("#%s").dialog({
                                    autoOpen: false,
                                    modal: true,
                                    buttons: {
                                        "Ok": function(){
                                            //Call the OK pressed callback or endpoint
                                            $.ajax({
                                                url: '/%s',
                                                type: 'get',
                                                dataType: 'json',
                                                success: function(status){},
                                                error: function(err_status){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                                }
                                            });
                                            $(this).dialog('close');
                                        }
                                    },
                                    beforeClose: function(event, ui){
                                        $.ajax({
                                            url: '/%s',
                                            type: 'get',
                                            dataType: "json",
                                            success: function(status){},
                                            error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            }
                                        });
                                    }

                                });
                            });
                        </script>
                    """ % (self._name, ok_pressed_url, before_close_url)
        return script

    def render(self):
        content = self._render_pre_content('div')
        for widget in self._child_widgets:
            content += "\n" + widget.render()
        content += self._render_post_content('div')
        content += "\n" + self._attach_script(self._dialog_type)
        self._widget_content = content + "\n" + self._attach_polling()
        return self._widget_content


class MenuItem(Widget):
    """A menuitem represents the action item that is clickable or
    executable. A menuitem can have label, icon or submenus.
    Seperator's are built using dash or space as item
    """
    _title = None
    _icon = None
    _menu_clicked_callback = None
    _app = None
    _disabled = None

    def __init__(self, name, title, icon=None, desc=None, prop=None, style=None, attr=None,
                 menu_clicked_callback=None, app=None, css_cls=None, disabled=None):
        """Default constructor of the Menuitem widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the Checkbox button group
                icon (string, optional): whether to show icon or not, default is None
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                menu_clicked_callback (function, optional): A function to be called back on onclick event
                app (Flask, optional): An instance of Flask class
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls)
        self._title = title
        self._icon = icon
        self._menu_clicked_callback = menu_clicked_callback
        self._app = app
        self._disabled = disabled
        if disabled:
            self.add_property('class', 'ui-state-disabled')
        self._attach_onclick()

    def set_disabled(self, val):
        """Sets the menu item enabled or disabled based on the value passed as parameter

            Args:
                val (boolean): True or False to widget enabled or disabled
        """
        self._disabled = val

    def get_disabled(self):
        """Gets the state of MenuItem widget i.e., whether it is enabled or disabled

            Returns:
                boolean: True or False
        """
        return self._disabled

    def set_title(self, val):
        """Sets the title of the MenuItem widget as the value passed as parameter

            Args:
                val (string): title that needs to be set on MenuItem
        """
        self._title = val

    def get_title(self):
        """Returns the value of the title of current MenuItem

            Returns:
                string: The title of the MenuItem widget
        """
        return self._title

    def set_icon(self, val):
        """Sets the icon to be used on the MenuItem. The passed value should be a valid
        jquery-ui icon style class e.g., ui-icon-stop

            Args:
                val (string): A valid jquery-ui icon class name
        """
        self._icon = val

    def get_icon(self):
        """Returns the name of the jquery-ui icon style class used for current widget

            Returns:
                string: Jquey-UI icon style class name
        """
        return self._icon

    def _attach_onclick(self):
        if self._app is not None and self._menu_clicked_callback is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """$.ajax({
                                url: "/%s",
                                dataType: "json",
                                data: {
                                    "name": "%s",
                                    "title": "%s",
                                    "disabled": %s
                                    },
                                type: "get",
                                success: function(status){alertify.success("Action completed successfully!");},
                                error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);}
                                                });
            """ % (url, self._name, self._title, "true" if self._disabled else "false")
            self.add_property('onclick', ajax)
            if not found:
                self._app.add_url_rule("/" + url, url, self._process_menu_clicked_callback)

    def on_menu_clicked(self, menu_clicked_callback, app=None):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function. If no app is associated with current widget, it should be
        linked by passing `app` param

            Args:
                menu_clicked_callback (function): The function/callback that will be
                                                    called for this event
                app (Flask, optional): An instance of Flask app, though this param is optional, it is
                                        required to have events work properly. So, it should be passed
                                        during creation of widget in the constructor or should be
                                        passed in this function
        """
        if app is not None:
            self._app = app
        self._menu_clicked_callback = menu_clicked_callback
        self._attach_onclick()

    def _process_menu_clicked_callback(self):
        if request.args.__len__() > 0:
            tit = request.args['title']
            if tit is not None:
                self._title = tit
            dsbld = request.args['disabled']
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
        if self._menu_clicked_callback is not None:
            return json.dumps({'result': self._menu_clicked_callback()})
        return json.dumps({'result': ''})

    def _sync_properties(self):
        return json.dumps({'title': self._title,
                           'disabled': self._disabled if self._disabled is not None else False,
                           'icon': self._icon
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
                                        //Sets the title of MenuItem
                                        //selector.text(props.title);
                                        //Set disable or enable
                                        if(props.disabled){
                                            if(!selector.hasClass('ui-state-disabled')){
                                                selector.addClass('ui-state-disabled');
                                            }
                                        } else {
                                            if(selector.hasClass('ui-state-disabled')){
                                                selector.removeClass('ui-state-disabled');
                                            }
                                        }
                                        if(props.icon != undefined && props.icon != ""){
                                            icon_selector = $('#%s_icon');
                                            if(icon_selector != undefined){
                                                if(!icon_selector.hasClass(props.icon)){
                                                    icon_selector.addClass(props.icon)
                                                }
                                            }
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
                            },10000);
                        })();
                    </script>
                """ % (url, url, self._name, self._name, url)
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == url:
                found = True
        if not found:
            self._app.add_url_rule('/' + url, url,
                                   self._sync_properties)
        return script

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
        self._widget_content = content + "\n" + self._attach_polling()
        return self._widget_content


class SubMenu(MenuItem):
    """SubMenu is an MenuItem with title and further have its child menuitems which appears as
    dropdown panel.
    """

    def __init__(self, name, title, icon=None, desc=None, prop=None, style=None, attr=None,
                 menu_clicked_callback=None, app=None, css_cls=None):
        """Default constructor of the Menuitem widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the Checkbox button group
                icon (string, optional): whether to show icon or not, default is None
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                menu_clicked_callback (function, optional): A function to be called back on onclick event
                app (Flask, optional): An instance of Flask class
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        MenuItem.__init__(self, name, title, icon=icon, desc=desc, prop=prop, style=style, attr=attr,
                          menu_clicked_callback=menu_clicked_callback, app=app, css_cls=css_cls)

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


class Menu(Widget):
    """The root of the menu used to layout menu in the desired position and uses various options to
    customize the menu. This is the class that will init the menu system and renders to its parent
    widget
    """

    _app = None
    _menu_type = None

    def __init__(self, name, menu_type=None, desc=None, prop=None, style=None, attr=None,
                 app=None, css_cls=None):
        """Default constructor of the Menu widget class

            Args:
                name (string): name of the widget for internal use
                menu_type (MenuTypes): Specify which menu type to render, default is vertical
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                app (Flask, optional): An instance of Flask class
                css_cls (list, optional): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._app = app
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
                            },10000);
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
                            },10000);
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
    _value = None
    _app = None
    _disabled = None

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 app=None, css_cls=None, collapsible=None, open_on_mouseover=None,
                 sortable=None, v_orient=None, tab_activated_callback=None,
                 disabled=None):
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
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        if collapsible is not None and collapsible:
            self._collapsible = "true"
        else:
            self._collapsible = "false"
        if open_on_mouseover is not None and open_on_mouseover:
            self._open_on_mouseover = "mouseover"
        else:
            self._open_on_mouseover = "click"
        if sortable is not None and sortable:
            self._sortable = "true"
        else:
            self._sortable = "false"
        if v_orient is not None and v_orient:
            self._v_orient = "true"
        else:
            self._v_orient = "false"
        self._tab_activated_callback = tab_activated_callback
        self._app = app
        self._disabled = disabled

    @property
    def value(self):
        """Value or Index of the selected section or panel under Tab widget
        """
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

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
                            }""" % (self._name, self._collapsible, self._open_on_mouseover, self._sortable,
                                    self._v_orient)
        if self._app is not None and self._tab_activated_callback is not None:
            script += """function tabActivated(event, ui){
                            $.ajax({
                                url: "/%s",
                                type: "get",
                                dataType: "json",
                                data: {'value': selector.tabs("option", "active")},
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
            val = request.args['value']
            if val is not None:
                self._value = val
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
        return json.dumps({'collapsible': True if self._collapsible == "true" else False,
                           'open_on_mouseover': self._open_on_mouseover,
                           'sortable': True if self._sortable == "true" else False,
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
                                            var existing_val = selector.tabs('option', 'active');
                                            if(existing_val != props.value){
                                                selector.tabs('option', 'active', props.value);
                                            }
                                        }
                                        if(props.collapsible != undefined){
                                            selector.tabs('option', 'collapsible', props.max);
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
                            },10000);
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
