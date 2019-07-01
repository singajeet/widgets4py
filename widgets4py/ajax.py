"""
This module contains the basic widgets for building
GUI apps
Author: Ajeet Singh
Date: 06/25/2019
"""
from widgets4py.base import Widget
from flask import json, request


class Button(Widget):
    """A standard `Button` to be displayed in the parent container. The required fields for
    this class is `name` and `title`. The name parameter is the identifier to refer this button
    by the internal logic or can be referenced from outside using JScript. Below is an example of
    creating a button in an App:

        >>> from flask import Flask

        >>> from widgets4py.ajax import Button

        >>> from widgets4py.base import Page

        >>> from widgets4py.layouts import SimpleGridLayout

        >>> app = Flask("My Flask App")

        >>> class PageTest:
        ...
        ...    btn = None
        ...
        ...    def show_layout(self):
        ...        pg = Page('myPage', 'My Page')
        ...        sg = SimpleGridLayout("Grid", 3, 2)
        ...        self.btn = Button('btn', 'Push', app=app, onclick_callback=self.change_btn_title)
        ...        content = pg.render()
        ...        return content
        ...    def change_btn_title(self):
        ...        self.btn.set_title("New Title")
        ...        print("Btn title changed!")
        ...        return "success"
        ...

        >>> p = PageTest()

        >>> app.add_url_rule('/', 'index', p.show_layout)
    """

    _onclick_callback = None
    _app = None
    _title = None
    _disabled = None

    def __init__(self, name, title, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False,
                 onclick_callback=None, app=None, css_cls=None):
        """Default constructor of the Button widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                required (Boolean): Widget is required to be filled-in or not
                onclick_callback (function): A function to be called back on onclick event
                app (Flask): An instance of Flask class
                css_cls (list): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'button')
        self.add_property('value', title)
        self._title = title
        if disabled:
            self.add_attribute('disabled')
            self._disabled = True
        if required:
            self.add_attribute('required')
        self._onclick_callback = onclick_callback
        self._app = app
        self._attach_onclick()

    def _attach_onclick(self):
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """
                $.ajax({
                    url: "/%s",
                    dataType: "json",
                    data: {"title": $("#%s").val(),
                            "disabled": $("#%s").prop("disabled")},
                    type: "get",
                    success: function(status){alertify.success("Action completed successfully!");},
                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            }
                });
            """ % (url, self._name, self._name)
            self.add_property('onclick', ajax)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onclick_callback)

    def _process_onclick_callback(self):
        if request.args.__len__() > 0:
            tit = request.args['title']
            if tit is not None:
                self._title = tit
            dsbld = request.args['disabled']
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
        return json.dumps({"result": self._onclick_callback()})

    def set_title(self, title):
        """Sets the title of button widget

            Args:
                title (string): title of the button
        """
        self._title = title

    def get_title(self):
        """Returns the title of Button widget"""
        return self._title

    def set_disabled(self, disabled):
        """Sets Button widget as disabled

            Args:
                disabled (Boolean): state of the button
        """
        self._disabled = disabled

    def get_disabled(self):
        """Returns the disabled state of the Button"""
        return self._disabled

    def _sync_properties(self):
        return json.dumps({'title': self._title,
                           'disabled': self._disabled if self._disabled is not None else False
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

                                        selector.val(props.title);
                                        selector.prop('disabled', props.disabled);

                                        //alertify.success(props.title +"-" + props.readonly + "-" + props.disabled);
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

    def on_click(self, onclick_callback, app=None):
        """Attach the `on_click` event handler to the Button widget

            Args:
                onclick_callback (function): A reference to method or function that
                                                will be called when this event is fired
                app (Flask): An instance of the Flask application
        """
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self._attach_onclick()

    def render(self):
        """Renders the content of button class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_polling()
        return self._widget_content


class TextBox(Widget):
    """A simple HTML textbox / input field"""

    _app = None
    _onchange_callback = None
    _text = None
    _disabled = None
    _readonly = None

    def __init__(self, name, text=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None,
                 app=None, onchange_callback=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'text')
        if text is not None:
            self.add_property('value', text)
            self._text = text
        if readonly:
            self.add_attribute('readonly')
            self._readonly = readonly
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        if required:
            self.add_attribute('required')
        self._app = app
        self._onchange_callback = onchange_callback
        self._attach_onchange()

    def _attach_onchange(self):
        if self._app is not None and self._onchange_callback is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            ajax = """
                $.ajax({
                    url: "/%s",
                    data: {"text": $("#%s").val(),
                            "readOnly": $("#%s").prop("readOnly"),
                            "disabled": $("#%s").prop("disabled")},
                    type: "get",
                    dataType: "json",
                    success: function(status){alertify.success("Action completed successfully!");},
                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            }
                });
            """ % (url, self._name, self._name, self._name)
            self.add_property('onchange', ajax)
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + url, url, self._process_onchange_callback)

    def _process_onchange_callback(self):
        if request.args.__len__() > 0:
            txt = request.args['text']
            if txt is not None:
                self._text = txt
            rdOnly = request.args['readOnly']
            if rdOnly is not None:
                self._readonly = True if rdOnly == "true" else False
            dsbld = request.args['disabled']
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
        return json.dumps({"result": self._onchange_callback()})

    def on_change(self, onchange_callback, app=None):
        """Attaches an callback handler to an Textbox"""
        self._onchange_callback = onchange_callback
        self._app = app
        self._attach_onchange()

    def set_text(self, txt):
        self._text = txt

    def get_text(self):
        return self._text

    def set_readonly(self, readonly):
        self._readonly = readonly

    def get_readonly(self):
        return self._readonly

    def set_disabled(self, disabled):
        self._disabled = disabled

    def get_disabled(self):
        return self._disabled

    def _sync_properties(self):
        return json.dumps({'text': self._text,
                           'readonly': self._readonly if self._readonly is not None else False,
                           'disabled': self._disabled if self._disabled is not None else False
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
                                        selector.val(props.text);
                                        selector.prop('readOnly', props.readonly);
                                        selector.prop('disabled', props.disabled);

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
        """Renders the content of textbox class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_polling()
        return self._widget_content


class CheckBox(Widget):
    """A simple HTML chexkbox / input field"""

    _title = None
    _value = None
    _checked = None
    _disabled = None
    _app = None
    _onclick_callback = None

    def __init__(self, name, title, value=None, checked=False, desc=None,
                 prop=None, style=None, attr=None, disabled=False,
                 required=False, css_cls=None, app=None, onclick_callback=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._title = title
        self._app = app
        self._onclick_callback = onclick_callback
        self.add_property('type', 'checkbox')
        if value is not None:
            self.add_property('value', value)
            self._value = value
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        if required:
            self.add_attribute('required')
        if checked:
            self.add_attribute('checked')
            self._checked = checked
        self._attach_onclick()

    def _attach_onclick(self):
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """
                $.ajax({
                    url: "/%s",
                    data: {
                            "title": $("#%s_lbl").text(),
                            "checked": $("#%s").is(":checked"),
                            "disabled": $("#%s").prop("disabled"),
                            "value": $("#%s").val()
                            },
                    type: "get",
                    success: function(status){
                                                alertify.success("Action completed successfully!");
                                            },
                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            },
                    dataType: "json"
                });
            """ % (url, self._name, self._name, self._name, self._name)
            self.add_property('onclick', ajax)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onclick_callback)

    def _process_onclick_callback(self):
        if request.args.__len__() > 0:
            tit = request.args['title']
            if tit is not None:
                self._title = tit
            chk = request.args['checked']
            if chk is not None:
                self._checked = chk
            dsbl = request.args["disabled"]
            if dsbl is not None:
                self._disabled = dsbl
            val = request.args["value"]
            if val is not None:
                self._value = val
        return json.dumps({"result": self._onclick_callback()})

    def set_title(self, title):
        self._title = title

    def get_title(self):
        return self._title

    def set_disabled(self, disabled):
        self._disabled = disabled

    def get_disabled(self):
        return self._disabled

    def set_value(self, val):
        self._value = val

    def get_value(self):
        return self._value

    def set_checked(self, chk):
        self._checked = chk

    def get_checked(self):
        return self._checked

    def _sync_properties(self):
        return json.dumps({'title': self._title,
                           'checked': self._checked if self._checked is not None else 'false',
                           'disabled': self._disabled if self._disabled is not None else 'false',
                           'value': self._value
                           })

    def _attach_polling(self):
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                        (function %s_poll(){
                            setTimeout(function(){
                                $.ajax({
                                    url: "/%s",
                                    type: "get",
                                    success: function(props){
                                        selector = $('#%s');
                                        selector_lbl = $('#%s_lbl');
                                        selector_lbl.text(props.title);
                                        if(props.checked == true){
                                            selector.attr('checked', props.checked);
                                        }
                                        if(props.disabled == true){
                                            selector.prop('disabled', props.disabled);
                                        }
                                        if(props.value != undefined){
                                            selector.val(props.value);
                                        }
                                        //alertify.success(props.title+ "<br />" + props.checked);
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

    def on_click(self, onclick_callback, app=None):
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self._attach_onclick()

    def render(self):
        """Renders the content of chexkbox class"""
        if self._title is None:
            content = self._render_pre_content('input')
            content += self._render_post_content('input')
            self._widget_content = content + "\n" + self._attach_polling()
            return self._widget_content
        else:
            content = "<div class='ui-widget-content'>\n"
            content += self._render_pre_content('input')
            content += self._render_post_content('input')
            content += "\n<label for='" + self._name + "' id='" +\
                       self._name + "_lbl'>" + self._title + "</label>"
            content += "\n<div>" + "\n" + self._attach_polling()
            self._widget_content = content
            return self._widget_content


class Color(Widget):
    """A simple HTML color / input field"""

    _value = None
    _disabled = None
    _onclick_callback = None
    _onchange_callback = None
    _app = None

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, css_cls=None, onclick_callback=None,
                 onchange_callback=None, app=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._value = value
        self._app = app
        self.add_property('type', 'color')
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        if required:
            self.add_attribute('required')
        self._onchange_callback = onchange_callback
        self._onclick_callback = onclick_callback
        self._attach_onclick()
        self._attach_onchange()

    def _attach_onclick(self):
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name + "_onclick").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """
                $.ajax({
                    url: "/%s",
                    data: {},
                    type: "get",
                    success: function(status){
                                                alertify.success("Action completed successfully!");
                                            },
                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            },
                    dataType: "json"
                });
            """ % (url)
            self.add_property('onclick', ajax)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onclick_callback)

    def _attach_onchange(self):
        if self._app is not None and self._onchange_callback is not None:
            url = str(__name__ + "_" + self._name + "_onchange").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """
                $.ajax({
                    url: "/%s",
                    data: {
                            "disabled": $("#%s").prop("disabled"),
                            "value": $("#%s").val()
                            },
                    type: "get",
                    success: function(status){
                                                alertify.success("Action completed successfully!");
                                            },
                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            },
                    dataType: "json"
                });
            """ % (url, self._name, self._name)
            self.add_property('onchange', ajax)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onchange_callback)

    def _process_onclick_callback(self):
        return json.dumps({'result': self._onclick_callback()})

    def _process_onchange_callback(self):
        if request.args.__len__() > 0:
            val = request.args["value"]
            if val is not None:
                self._value = val
            dsbld = request.args["disabled"]
            if dsbld is not None:
                self._disabled = dsbld
        return json.dumps({'result': self._onchange_callback()})

    def set_value(self, val):
        self._value = val

    def get_value(self):
        return self._value

    def set_disabled(self, val):
        self._disabled = val

    def get_disabled(self):
        return self._disabled

    def on_click(self, onclick_callback, app=None):
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self._attach_onclick()

    def on_change(self, onchange_callback, app=None):
        if app is not None:
            self._app = app
        self._onchange_callback = onchange_callback
        self._attach_onchange()

    def _sync_properties(self):
        return json.dumps({'disabled': self._disabled if self._disabled is not None else 'false',
                           'value': self._value
                           })

    def _attach_polling(self):
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                        (function %s_poll(){
                            setTimeout(function(){
                                $.ajax({
                                    url: "/%s",
                                    type: "get",
                                    success: function(props){
                                        selector = $('#%s');
                                        if(props.disabled == true){
                                            selector.prop('disabled', props.disabled);
                                        }
                                        if(props.value != undefined){
                                            selector.val(props.value);
                                        }
                                        //alertify.success(props.title+ "<br />" + props.checked);
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
        """Renders the content of color claskey, values"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_polling()
        return self._widget_content


class Date(Widget):
    """A simple HTML date / input field"""

    _value = None
    _disabled = None
    _readonly = None
    _onclick_callback = None
    _onchange_callback = None
    _min = None
    _max = None
    _app = None

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 min=None, max=None, readonly=False, disabled=False,
                 required=False, css_cls=None, onclick_callback=None, onchange_callback=None,
                 app=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'date')
        if value is not None:
            self.add_property('value', value)
            self._value = value
        if min is not None:
            self.add_property('min', min)
            self._min = min
        if max is not None:
            self.add_property('max', max)
            self._max = max
        if readonly:
            self.add_attribute('readonly')
            self._readonly = readonly
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        if required:
            self.add_attribute('required')
        self._app = app
        self._onchange_callback = onchange_callback
        self._onclick_callback = onclick_callback
        self._attach_onclick()
        self._attach_onchange()

    def _attach_onclick(self):
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name + "_onclick").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """
                $.ajax({
                    url: "/%s",
                    data: {},
                    type: "get",
                    success: function(status){
                                                alertify.success("Action completed successfully!");
                                            },
                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            },
                    dataType: "json"
                });
            """ % (url)
            self.add_property('onclick', ajax)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onclick_callback)

    def _attach_onchange(self):
        if self._app is not None and self._onchange_callback is not None:
            url = str(__name__ + "_" + self._name + "_onchange").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            ajax = """
                $.ajax({
                    url: "/%s",
                    data: {
                            "min": $("#%s").prop("min"),
                            "max": $("#%s").prop("max"),
                            "readOnly": $("#%s").prop("readOnly"),
                            "disabled": $("#%s").prop("disabled"),
                            "value": $("#%s").val()
                            },
                    type: "get",
                    success: function(status){
                                                alertify.success("Action completed successfully!");
                                            },
                    error: function(err_status){
                                                alertify.error("Status Code: "
                                                + err_status.status + "<br />" + "Error Message:"
                                                + err_status.statusText);
                                            },
                    dataType: "json"
                });
            """ % (url, self._name, self._name, self._name, self._name, self._name)
            self.add_property('onchange', ajax)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onchange_callback)

    def _process_onclick_callback(self):
        return json.dumps({'result': self._onclick_callback()})

    def _process_onchange_callback(self):
        if request.args.__len__() > 0:
            val = request.args["value"]
            if val is not None:
                self._value = val
            dsbld = request.args["disabled"]
            if dsbld is not None:
                self._disabled = dsbld
            min = request.args["min"]
            if min is not None:
                self._min = min
            max = request.args["max"]
            if max is not None:
                self._max = max
            rdOnly = request.args["readOnly"]
            if rdOnly is not None:
                self._readonly = rdOnly
        return json.dumps({'result': self._onchange_callback()})

    def set_value(self, val):
        self._value = val

    def get_value(self):
        return self._value

    def set_min(self, val):
        self._min = val

    def get_min(self):
        return self._min

    def set_max(self, val):
        self._max = val

    def get_max(self):
        return self._max

    def set_readonly(self, val):
        self._readonly = val

    def get_readonly(self):
        return self._readonly

    def set_disabled(self, val):
        self._disabled = val

    def get_disabled(self):
        return self._disabled

    def on_click(self, onclick_callback, app=None):
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self._attach_onclick()

    def on_change(self, onchange_callback, app=None):
        if app is not None:
            self._app = app
        self._onchange_callback = onchange_callback
        self._attach_onchange()

    def _sync_properties(self):
        return json.dumps({'disabled': self._disabled if self._disabled is not None else 'false',
                           'value': self._value,
                           'min': self._min,
                           'max': self._max,
                           'readOnly': self._readonly if self._readonly is not None else "false"
                           })

    def _attach_polling(self):
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                        (function %s_poll(){
                            setTimeout(function(){
                                $.ajax({
                                    url: "/%s",
                                    type: "get",
                                    success: function(props){
                                        selector = $('#%s');
                                        if(props.disabled == true){
                                            selector.prop('disabled', props.disabled);
                                        }
                                        if(props.value != undefined){
                                            selector.val(props.value);
                                        }
                                        if(props.readOnly == true){
                                            selector.prop('readOnly', props.readOnly);
                                        }
                                        if(props.min != undefined){
                                            selector.prop('min', props.min);
                                        }
                                        if(props.max != undefined){
                                            selector.prop('max', props.max);
                                        }
                                        //alertify.success(props.title+ "<br />" + props.checked);
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
        """Renders the content of date class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_polling()
        return self._widget_content


class DateTimeLocal(Widget):
    """A simple HTML datetime-local / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'datetime-local')
        if value is not None:
            self.add_property('value', value)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of datetime-local class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Email(Widget):
    """A simple HTML email / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'email')
        if value is not None:
            self.add_property('value', value)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of email class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class File(Widget):
    """A simple HTML file / input field"""

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, multiple=False,
                 css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'file')
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')
        if multiple:
            self.add_attribute('multiple')

    def render(self):
        """Renders the content of file class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Hidden(Widget):
    """A simple HTML hidden / input field"""

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 value=None, readonly=False, disabled=False, required=False,
                 css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'hidden')
        if value is not None:
            self.add_property('value', value)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of hidden class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Image(Widget):
    """A simple HTML image / input field"""

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 alt_text=None, readonly=False, disabled=False, required=False,
                 css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'image')
        if alt_text is not None:
            self.add_property('value', alt_text)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of image class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Month(Widget):
    """A simple HTML month / input field"""

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'month')
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of month class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Number(Widget):
    """A simple HTML number / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 min=None, max=None, readonly=False, disabled=False, required=False,
                 css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'number')
        if value is not None:
            self.add_property('value', value)
        if min is not None:
            self.add_property('min', min)
        if max is not None:
            self.add_property('max', max)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of number class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Password(Widget):
    """A simple HTML password / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'password')
        if value is not None:
            self.add_property('value', value)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of password class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Radio(Widget):
    """A simple HTML radio / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'radio')
        if value is not None:
            self.add_property('value', value)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of radio class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Range(Widget):
    """A simple HTML range / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 min=None, max=None, readonly=False, disabled=False, required=False,
                 css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'range')
        if value is not None:
            self.add_property('value', value)
        if min is not None:
            self.add_property('min', min)
        if max is not None:
            self.add_property('max', max)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of range class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Reset(Widget):
    """A simple HTML reset / input field"""

    def __init__(self, name, title, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'reset')
        self.add_property('value', title)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of reset class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Search(Widget):
    """A simple HTML search / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'search')
        if value is not None:
            self.add_property('value', value)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of search class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Submit(Widget):
    """A simple HTML submit / input field"""

    def __init__(self, name, title, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'submit')
        self.add_property('value', title)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of submit class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Telephone(Widget):
    """A simple HTML telephone / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 pattern=None, readonly=False, disabled=False, required=False,
                 css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'tel')
        if value is not None:
            self.add_property('value', value)
        if pattern is not None:
            self.add_property('pattern', pattern)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of telephone class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Time(Widget):
    """A simple HTML time / input field"""

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'time')
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of time class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class URL(Widget):
    """A simple HTML url / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'url')
        if value is not None:
            self.add_property('value', value)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of url class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Week(Widget):
    """A simple HTML week / input field"""

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'week')
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of week class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Form(Widget):
    """An HTML form widget class"""

    _use_fieldset = False
    _legend = None
    _on_form_submitted = None
    _app = None

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 action=None, target=None, method=None,
                 use_fieldset=False, legend=None, app=None,
                 submit_callback=None, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        if submit_callback is not None:
            self._on_form_submitted = submit_callback
        if app is not None:
            self._app = app
        if target is not None:
            self.add_property('target', target)
        if method is not None:
            self.add_property('method', method)
        self._use_fieldset = use_fieldset
        self._legend = legend
        if app is not None and submit_callback is not None:
            self._register_rule()
        else:
            if action is not None:
                self.add_property('action', action)

    #  Event for the on form submit
    def on_form_submit(self, submit_callback, app=None):
        if app is not None:
            self._app = app
        self._on_form_submitted = submit_callback
        if self._app is not None and self._on_form_submitted is not None:
            self._register_rule()

    def _register_rule(self):
        # Prepare endpoint name and URL
        rule_str = str(__name__ + "_" + self._name).replace(".", "_")
        # Check if rule already exists? If not add it to rule map
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == rule_str:
                found = True
        if not found:
            self._app.add_url_rule('/' + rule_str,
                                   rule_str,
                                   self._process_on_form_submitted)
        self.add_property('action', "/" + rule_str)

    def _process_on_form_submitted(self):
        # call the callback handler
        self._on_form_submitted()
        return self._root_widget.render()

    def render(self):
        """Renders the content of the form"""
        content = self._render_pre_content('form')
        if self._use_fieldset is True:
            content += "\n<fieldset>"
        if self._legend is not None:
            content += "\n<legend>" + self._legend + "</legend>"
        for widget in self._child_widgets:
            content += widget.render()
        if self._use_fieldset is True:
            content += "\n</fieldset>"
        self._widget_content = content + self._render_post_content('form')
        return self._widget_content


class DropDown(Widget):
    """A dropdown widget class"""

    _options = None

    def __init__(self, name, options=None, size=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')
        if size is not None:
            self.add_property('size', size)
        if options is not None:
            self._options = options
        else:
            self._options = {}

    def add_option(self, value, title, is_selected=False):
        """Adds an options to the select list"""
        self._options[value] = [title, is_selected]

    def remove_options(self, value):
        """Removes an option from the select list"""
        self._options.pop(value)

    def render(self):
        """Renders the select list on the page"""
        content = self._render_pre_content('select')
        content += "\n"
        for opt in self._options:
            title = self._options.get(opt)[0]
            is_selected = self._options.get(opt)[1]
            content += "<option value='" + opt + "' "
            if is_selected:
                content += "selected "
            content += ">"
            if title is not None:
                content += title
            else:
                content += opt
            content += "</option>"
        self._widget_content = content + self._render_post_content('select')
        return self._widget_content


class Label(Widget):
    """An label widget to be use for other widgets"""

    _text = None
    _for_widget = None

    def __init__(self, name, text, for_widget):
        Widget.__init__(self, name)
        self._text = text
        self._for_widget = for_widget
        self.add_property('for', for_widget.get_name())

    def render(self):
        """Renders the label for a given widget"""
        content = self._render_pre_content('label')
        content += self._text
        self._widget_content = content + self._render_post_content('label')
        return self._widget_content
