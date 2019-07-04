"""HTML Widgets based on the JQuery UI framework
Author: Ajeet Singh
Date: 06/25/2019
"""
from widgets4py.base import Widget
from flask import request, json


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
                var heading = $("#%s_h3").text()
                $.ajax({
                    url: "/%s",
                    dataType: "json",
                    data: {"title":  heading},
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
            tit = request.args['title']
            if tit is not None:
                self._title = tit
            dsbld = request.args['disabled']
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
        return json.dumps({"result": self._onclick_callback()})

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
        if self._disabled_buttons is None:
            self._disabled_buttons = {}
        self._disabled_buttons[btn] = state

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
            label = "<label for='" + name + "'>"\
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
