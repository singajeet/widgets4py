"""
This module contains the basic widgets for building
GUI apps
Author: Ajeet Singh
Date: 06/25/2019
"""
import os
from widgets4py.base import Widget
from flask import json, request


class Button(Widget):
    """A standard `Button` to be displayed in the parent container. The required fields for
    this class are `name` and `title`. The name parameter is the identifier to refer this button
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
        ...        sg = SimpleGridLayout("Grid", 1, 2)
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
                onclick_callback (callable): A function to be called back on onclick event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onclick_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
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
        else:
            self._disabled = False
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
        props = {}
        if request.args.__len__() > 0:
            tit = request.args['title']
            if tit is not None:
                self._title = tit
                props['title'] = tit
            dsbld = request.args['disabled']
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
                props['disabled'] = self._disabled
        return json.dumps({"result": self._onclick_callback(self._name, props)})

    def _set_title(self, title):
        self._title = title

    def _get_title(self):
        return self._title

    title = property(_get_title, _set_title, doc="Title of the button widget")

    def _set_disabled(self, disabled):
        self._disabled = disabled

    def _get_disabled(self):
        return self._disabled

    disabled = property(_get_disabled, _set_disabled, doc="Returns the disabled state of the Button")

    def _sync_properties(self):
        return json.dumps({'title': self._title,
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
                                        selector.val(props.title);
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
        """Renders the content of button class and returns it back to the parent widget
        for final rendering to the `Page`
        """
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
        """
            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                desc (string): description of the button widget
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                required (Boolean): Widget is required to be filled-in or not
                onchange_callback (callable): A function to be called back on onchange event of textbox.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the textbox for which this event is fired
                        props: Dict object having three props: Text, Disabled & ReadOnly
                app (Flask): An instance of Flask class
                css_cls (list): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'text')
        if text is not None:
            self.add_property('value', text)
            self._text = text
        if readonly:
            self.add_attribute('readonly')
            self._readonly = readonly
        else:
            self._readonly = False
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        else:
            self._disabled = False
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
        props = {}
        if request.args.__len__() > 0:
            txt = request.args['text']
            if txt is not None:
                self._text = txt
                props['text'] = txt
            rdOnly = request.args['readOnly']
            if rdOnly is not None:
                self._readonly = True if rdOnly == "true" else False
                props['readonly'] = self._readonly
            dsbld = request.args['disabled']
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
                props['disabled'] = self._disabled
        return json.dumps({"result": self._onchange_callback(self._name, props)})

    def on_change(self, onchange_callback, app=None):
        """Attaches an callback handler to an Textbox"""
        self._onchange_callback = onchange_callback
        self._app = app
        self._attach_onchange()

    def _set_text(self, txt):
        self._text = txt

    def _get_text(self):
        return self._text

    text = property(_get_text, _set_text, doc="Text value of the Textbox widget")

    def _set_readonly(self, readonly):
        self._readonly = readonly

    def _get_readonly(self):
        return self._readonly

    readonly = property(_get_readonly, _set_readonly, doc="Set or Get whether the widget is in readonly mode or not")

    def _set_disabled(self, disabled):
        self._disabled = disabled

    def _get_disabled(self):
        return self._disabled

    disabled = property(_get_disabled, _set_disabled, doc="Set or get whether textbox is enabled or disabled")

    def _sync_properties(self):
        return json.dumps({'text': self._text,
                           'readonly': self._readonly,
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
        """
            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                value (string): Value of checkbox when checked else empty
                check (boolean): Whether the checkbox is chexked or not
                desc (string): description of the button widget
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                required (Boolean): Widget is required to be filled-in or not
                onclick_callback (callable): A function to be called back on onclick event of checkbox.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the checkbox for which this event is fired
                        props: Dict object having four props: title, value, checked & disabled
                app (Flask): An instance of Flask class
                css_cls (list): An list of CSS class names to be added to current widget
        """
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
        else:
            self._disabled = False
        if required:
            self.add_attribute('required')
        if checked:
            self.add_attribute('checked')
            self._checked = checked
        else:
            self._checked = False
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
        props = {}
        if request.args.__len__() > 0:
            tit = request.args['title']
            if tit is not None:
                self._title = tit
                props['title'] = self._title
            chk = request.args['checked']
            if chk is not None:
                self._checked = True if chk == "true" else False
                props['checked'] = self._checked
            dsbl = request.args["disabled"]
            if dsbl is not None:
                self._disabled = True if dsbl == "true" else False
                props['disabled'] = self._disabled
            val = request.args["value"]
            if val is not None:
                self._value = val
                props['value'] = self._value
        return json.dumps({"result": self._onclick_callback(self._name, props)})

    def _set_title(self, title):
        self._title = title

    def _get_title(self):
        return self._title

    title = property(_get_title, _set_title, doc="The title or label of the checkbox")

    def _set_disabled(self, disabled):
        self._disabled = disabled

    def _get_disabled(self):
        return self._disabled

    disabled = property(_get_disabled, _set_disabled, doc="Enabled or Disabled state of the checkbox")

    def _set_value(self, val):
        self._value = val

    def _get_value(self):
        return self._value

    value = property(_get_value, _set_value, doc="The current value of the checkbox")

    def _set_checked(self, chk):
        self._checked = chk

    def _get_checked(self):
        return self._checked

    checked = property(_get_checked, _set_checked, doc="Checked or Unchecked state of checkbox")

    def _sync_properties(self):
        return json.dumps({'title': self._title,
                           'checked': self._checked,
                           'disabled': self._disabled,
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
                                        selector.prop('checked', props.checked);
                                        selector.prop('disabled', props.disabled);
                                        selector.val(props.value);
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
        """To register the callback handler to the checkbox

            Args:
                onclick_callback (callable): Method or function to be called on mouse click event
                app (Flask): An instance of the Flask app
        """
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
        """
            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                value (string): Value of checkbox when checked else empty
                desc (string): description of the button widget
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                required (Boolean): Widget is required to be filled-in or not
                onclick_callback (callable): A function to be called back on onclick event of color.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onclick_handler(source, props):
                            pass

                        source: Name of the color widget for which this event is fired
                        props: Dict object having four props: value & disabled
                onchange_callback (callback): Similar to `onclick_callback` but fires on change event
                app (Flask): An instance of Flask class
                css_cls (list): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._value = value
        self._app = app
        self.add_property('type', 'color')
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        else:
            self._disabled = False
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
        props = {}
        return json.dumps({'result': self._onclick_callback(self._name, props)})

    def _process_onchange_callback(self):
        props = {}
        if request.args.__len__() > 0:
            val = request.args["value"]
            if val is not None:
                self._value = val
                props['value'] = self._value
            dsbld = request.args["disabled"]
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
                props['disabled'] = self._disabled
        return json.dumps({'result': self._onchange_callback(self._name, props)})

    def _set_value(self, val):
        self._value = val

    def _get_value(self):
        return self._value

    value = property(_get_value, _set_value, doc="Current value of the color widget")

    def _set_disabled(self, val):
        self._disabled = val

    def _get_disabled(self):
        return self._disabled

    disabled = property(_get_disabled, _set_disabled, doc="Enabled or disabled state of the widget")

    def on_click(self, onclick_callback, app=None):
        """Attaches the onclick callback handler to the onclick event

            Args:
                onclick_callback (callable): The function or method that needs to be called
                                    The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                                def onclick_handler(source, props):
                                    pass

                                source: Name of the color widget for which this event is fired
                                props: Dict object having two props: value & disabled
                app (Flask): An instance of the Flask app
        """
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self._attach_onclick()

    def on_change(self, onchange_callback, app=None):
        """Attaches the onchange callback handler to the onclick event

            Args:
                onchange_callback (callable): The function or method that needs to be called
                                    The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                                def onchange_handler(source, props):
                                    pass

                                source: Name of the color widget for which this event is fired
                                props: Dict object having two props: value & disabled
                app (Flask): An instance of the Flask app
        """
        if app is not None:
            self._app = app
        self._onchange_callback = onchange_callback
        self._attach_onchange()

    def _sync_properties(self):
        return json.dumps({'disabled': self._disabled,
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
                                        selector.prop('disabled', props.disabled);
                                        selector.val(props.value);
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
        """
            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                value (string): Value of checkbox when checked else empty
                desc (string): description of the button widget
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                min (string): The minimum date range. Value less than it can't be selected
                                Format: YYYY-MM-DD
                max (string): The maximum date range. Value above it can't be selected
                                Format: YYYY-MM-DD
                disabled (Boolean): Enabled or Disabled state of widget
                required (Boolean): Widget is required to be filled-in or not
                onclick_callback (callable): A function to be called back on onclick event of date widget.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onclick_handler(source, props):
                            pass

                        source: Name of the date widget for which this event is fired
                        props: Dict object having five props: value, disabled, min, max & readOnly
                onchange_callback (callback): Similar to `onclick_callback` but fires on change event
                app (Flask): An instance of Flask class
                css_cls (list): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'date')
        if value is not None:
            self.add_property('value', value)
            self._value = value
        if min is not None:
            self.add_property('min', min)
            self._min = min
        else:
            self._min = ""
        if max is not None:
            self.add_property('max', max)
            self._max = max
        else:
            self._max = ""
        if readonly:
            self.add_attribute('readonly')
            self._readonly = readonly
        else:
            self._readonly = False
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        else:
            self._disabled = False
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
        props = {}
        return json.dumps({'result': self._onclick_callback(self._name, props)})

    def _process_onchange_callback(self):
        props = {}
        if request.args.__len__() > 0:
            val = request.args["value"]
            if val is not None:
                self._value = val
                props['value'] = self._value
            dsbld = request.args["disabled"]
            if dsbld is not None:
                self._disabled = True if dsbld == 'true' else False
                props['disabled'] = self._disabled
            min = request.args["min"]
            if min is not None:
                self._min = min
                props['min'] = self._min
            max = request.args["max"]
            if max is not None:
                self._max = max
                props['max'] = self._max
            rdOnly = request.args["readOnly"]
            if rdOnly is not None:
                self._readonly = True if rdOnly == 'true' else False
                props['readOnly'] = self._readonly
        return json.dumps({'result': self._onchange_callback(self._name, props)})

    def _set_value(self, val):
        self._value = val

    def _get_value(self):
        return self._value

    value = property(_get_value, _set_value, doc="Current value of the date widget")

    def _set_min(self, val):
        self._min = val

    def _get_min(self):
        return self._min

    min = property(_get_min, _set_min, doc="The minimum date allowed to be selected")

    def _set_max(self, val):
        self._max = val

    def _get_max(self):
        return self._max

    max = property(_get_max, _set_max, doc="The maximum date allowed to be selected")

    def _set_readonly(self, val):
        self._readonly = val

    def _get_readonly(self):
        return self._readonly

    readonly = property(_get_readonly, _set_readonly, doc="The readonly state of the widget")

    def _set_disabled(self, val):
        self._disabled = val

    def _get_disabled(self):
        return self._disabled

    disabled = property(_get_disabled, _set_disabled, doc="Enabled or disabled state of the widget")

    def on_click(self, onclick_callback, app=None):
        """
        Attaches the onclick handler to this widget
        Args:
            onclick_callback (callable): A function to be called back on onclick event of date.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onclick_handler(source, props):
                            pass

                        source: Name of the date widget for which this event is fired
                        props: Dict object having five props: value, disabled, min, max & readOnly
        """
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self._attach_onclick()

    def on_change(self, onchange_callback, app=None):
        """
        Attaches the onchange handler to this widget
        Args:
            onchange_callback (callable): A function to be called back on onchange event of date.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the date widget for which this event is fired
                        props: Dict object having five props: value, disabled, min, max & readOnly
        """
        if app is not None:
            self._app = app
        self._onchange_callback = onchange_callback
        self._attach_onchange()

    def _sync_properties(self):
        return json.dumps({'disabled': self._disabled,
                           'value': self._value,
                           'min': self._min,
                           'max': self._max,
                           'readOnly': self._readonly
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
                                        selector.prop('disabled', props.disabled);
                                        selector.val(props.value);
                                        selector.prop('readOnly', props.readOnly);
                                        selector.prop('min', props.min);
                                        selector.prop('max', props.max);
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
        """Renders the content of date class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_polling()
        return self._widget_content


class DateTimeLocal(Date):
    """A simple HTML datetime-local / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None,
                 onclick_callback=None, onchange_callback=None, app=None, min=None,
                 max=None):
        Date.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                      css_cls=css_cls, readonly=readonly, disabled=disabled,
                      required=required, onclick_callback=onclick_callback,
                      onchange_callback=onchange_callback, app=app, min=min, max=max)
        self.add_property('type', 'datetime-local')


class Email(TextBox):
    """A simple HTML email / input field"""

    def __init__(self, name, text=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None,
                 onchange_callback=None, app=None):
        TextBox.__init__(self, name, text=text, desc=desc, prop=prop, style=style, attr=attr,
                         css_cls=css_cls, readonly=readonly, disabled=disabled,
                         required=required, onchange_callback=onchange_callback,
                         app=app)
        self.add_property('type', 'email')


class File(Widget):
    """A simple HTML file / input field"""

    _app = None
    _onclick_callback = None
    _onchange_callback = None
    _disabled = None
    _multiple = None
    _upload_folder = None
    _allowed_extensions = None

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, multiple=False,
                 css_cls=None, onclick_callback=None, onchange_callback=None, app=None,
                 upload_folder=None, allowed_extensions=None):
        """
            Args:
                name (string): name of the widget for internal use
                desc (string): description of the button widget
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                required (Boolean): Widget is required to be filled-in or not
                multiple (Boolean): Whether to allow multiple selection of files or not
                onclick_callback (callable): A function to be called back on onclick event of date widget.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onclick_handler(source, props):
                            pass

                        source: Name of the date widget for which this event is fired
                        props: Dict object having five props: value, disabled, min, max & readOnly
                onchange_callback (callback): Similar to `onclick_callback` but fires on change event
                app (Flask): An instance of Flask class
                css_cls (list): An list of CSS class names to be added to current widget
                upload_folder (string): The folder path of server where uploaded files will be saved
                allowed_extensions (string): List of comma separated file ext which are allowed
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self.add_property('type', 'file')
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        else:
            self._disabled = False
        if required:
            self.add_attribute('required')
        if multiple:
            self.add_attribute('multiple')
            self._multiple = multiple
        else:
            self._multiple = False
        if upload_folder is not None:
            self._upload_folder = upload_folder
        else:
            self._upload_folder = "uploads/"
        if allowed_extensions is not None:
            self._allowed_extensions = allowed_extensions
        else:
            self._allowed_extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg',
                                            'gif', 'doc', 'docx', 'xls', 'xlsx'])
        self._app = app
        self._onchange_callback = onchange_callback
        self._onclick_callback = onclick_callback
        self._attach_onclick()
        self._attach_onchange()

    def _allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self._allowed_extensions

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
                var formData = new FormData();
                formData.append("disabled", $("#%s").prop("disabled"));
                formData.append("multiple", $("#%s").prop("multiple"));
                formData.append("file", $("#%s").prop("files")[0])
                $.ajax({
                    url: "/%s",
                    data: formData,
                    type: "post",
                    processData: false,
                    contentType: false,
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
            """ % (self._name, self._name, self._name, url)
            self.add_property('onchange', ajax)
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_onchange_callback, methods=['GET', 'POST'])

    def _process_onclick_callback(self):
        props = {}
        return json.dumps({'result': self._onclick_callback(self._name, props)})

    def _process_onchange_callback(self):
        props = {}
        if request.args.__len__() > 0:
            dsbld = request.args["disabled"]
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
                props['disabled'] = self._disabled
            multi = request.args["multiple"]
            if multi is not None:
                self._multiple = True if multi == "true" else False
                props['multiple'] = self._multiple
        if request.files.__len__() > 0:
            file = request.files['file']
            if file and self._allowed_file(file.filename):
                filename = file.filename
                if not os.path.exists(self._upload_folder):
                    os.mkdir(self._upload_folder)
                file.save(os.path.join(self._upload_folder, filename))
                props['filename'] = filename
                props['upload_path'] = self._upload_folder
        return json.dumps({'result': self._onchange_callback(self._name, props)})

    def _set_upload_folder(self, upload_folder):
        self._upload_folder = upload_folder

    def _get_upload_folder(self):
        return self._upload_folder

    upload_folder = property(_get_upload_folder, _set_upload_folder,
                             doc="Folder path on serve where files will be stored")

    def _set_allowed_ext(self, extensions):
        self._allowed_extensions = extensions

    def _get_allowed_ext(self):
        return self._allowed_extensions

    allowed_extensions = property(_get_allowed_ext, _set_allowed_ext, doc="File extensions allowed for upload")

    def _set_disabled(self, val):
        self._disabled = val

    def _get_disabled(self):
        return self._disabled

    disabled = property(_get_disabled, _set_disabled, doc="Enabled or disabled state of the widget")

    def _set_multiple(self, val):
        self._multiple = val

    def _get_multiple(self):
        return self._multiple

    multiple = property(_get_multiple, _set_multiple, doc="Whether to allow multi files upload")

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
        return json.dumps({'disabled': self._disabled,
                           'multiple': self._multiple
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
                                        selector.prop('disabled', props.disabled);
                                        selector.prop('multiple', props.multiple);
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
        """Renders the content of file class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_polling()
        return self._widget_content


class Image(Button):
    """A simple HTML image / input field"""

    def __init__(self, name, src, desc=None, prop=None, style=None, attr=None,
                 alt_text=None, readonly=False, disabled=False, required=False,
                 css_cls=None, onclick_callback=None, app=None):
        Button.__init__(self, name, "image", desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls, onclick_callback=onclick_callback,
                        app=app)
        self.add_property('type', 'image')
        self.add_property('src', src)
        if alt_text is not None:
            self.add_property('value', alt_text)


class Month(Date):
    """A simple HTML month / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None,
                 onclick_callback=None, onchange_callback=None, app=None, min=None, max=None):
        Date.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                      css_cls=css_cls, readonly=readonly, disabled=disabled,
                      required=required, onclick_callback=onclick_callback,
                      onchange_callback=onchange_callback, app=app, min=min, max=max, value=value)
        self.add_property('type', 'month')


class Number(TextBox):
    """A simple HTML number / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, onchange_callback=None,
                 css_cls=None, app=None):
        TextBox.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                         css_cls=css_cls, readonly=readonly, disabled=disabled,
                         required=required, text=value, onchange_callback=onchange_callback,
                         app=app)
        self.add_property('type', 'number')

    def _set_number(self, numb):
        self.set_text(numb)

    def _get_number(self):
        return self.get_text()

    number = property(_get_number, _set_number, doc="Value of the number textbox")


class Password(TextBox):
    """A simple HTML password / input field"""

    def __init__(self, name, password=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None,
                 onchange_callback=None, app=None):
        TextBox.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                         css_cls=css_cls, readonly=readonly, disabled=disabled,
                         required=required, text=password, onchange_callback=onchange_callback,
                         app=app)
        self.add_property('type', 'password')

    def _set_password(self, passwd):
        self.set_text(passwd)

    def _get_password(self):
        return self.get_text()

    password = property(_get_password, _set_password, doc="Value of the password textbox")


class Radio(CheckBox):
    """A simple HTML radio / input field"""

    def __init__(self, name, title, value=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, css_cls=None, onclick_callback=None,
                 app=None):
        CheckBox.__init__(self, name, title, value=value, desc=desc, prop=prop, style=style, attr=attr,
                          css_cls=css_cls, disabled=disabled, required=required,
                          onclick_callback=onclick_callback, app=app)
        self.add_property('type', 'radio')


class Range(Date):
    """A simple HTML range / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 min=None, max=None, readonly=False, disabled=False, required=False,
                 css_cls=None, onchange_callback=None, app=None):
        Date.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                      css_cls=css_cls, value=value, readonly=readonly, disabled=disabled,
                      required=required, onchange_callback=onchange_callback, app=app,
                      min=min, max=max)
        self.add_property('type', 'range')


class Reset(Button):
    """A Reset button helps in resetting the values of other widgets to default
    at the frontend but can also be used to reset variables at backend using the
    provided hook/event `onclick_callback`. Resetting widgets at frontend is
    built-in but the resetting logic needs to be written by users for backend by
    hooking up their custom logic `onclick_callback` event
    """

    def __init__(self, name, title, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, css_cls=None,
                 onclick_callback=None, app=None):
        Button.__init__(self, name, title, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls, disabled=disabled, required=required, app=app,
                        onclick_callback=onclick_callback)
        self.add_property('type', 'reset')


class Search(TextBox):
    """Works similar to TextBox widget. An `onchange_callback` event will be fired after
    widget lost the focus and that can be used to start the search operation at the
    backend
    """

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False, css_cls=None,
                 onchange_callback=None, app=None):
        TextBox.__init__(self, name, text=value, desc=desc, prop=prop, style=style, attr=attr,
                         css_cls=css_cls, readonly=readonly, disabled=disabled, required=required,
                         onchange_callback=onchange_callback, app=app)
        self.add_property('type', 'search')


class Submit(Button):
    """A submit button that submits the value of all widgets available under an `Form` to
    which this button is associated. Similar to `Button` class, this class also have an
    `onclick_event` which gets fired on the button click operation
    """

    def __init__(self, name, title, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, css_cls=None, onclick_callback=None,
                 app=None):
        Button.__init__(self, name, title, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls, disabled=disabled, required=required, app=app,
                        onclick_callback=onclick_callback)
        self.add_property('type', 'submit')


class Telephone(TextBox):
    """Similar to TextBox, this widget take telephone numbers as input in specified
    pattern if one is provided as parameter to this class. If no pattern is given,
    this widget takes any sequence of digits as phone number
    """

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 pattern=None, readonly=False, disabled=False, required=False,
                 css_cls=None, onchange_callback=None, app=None):
        TextBox.__init__(self, name, text=value, desc=desc, prop=prop, style=style, attr=attr,
                         css_cls=css_cls, readonly=readonly, disabled=disabled,
                         required=required, onchange_callback=onchange_callback,
                         app=app)
        self.add_property('type', 'tel')


class Time(Date):
    """Helps in selecting the time to the user. Depending upon browser, this widget could
    be displayed as TextBox or an DropDown to select the desired time
    """

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, css_cls=None, onchange_callback=None,
                 app=None):
        Date.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                      css_cls=css_cls, disabled=disabled, required=required,
                      onchange_callback=onchange_callback, app=app)
        self.add_property('type', 'time')


class URL(TextBox):
    """The URL Widget is used for input fields that should contain a URL address.
    Depending on browser support, the url field can be automatically validated when submitted.
    Some smartphones recognize the url type, and adds ".com" to the keyboard to match url input.
    """

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, css_cls=None, onchange_callback=None,
                 app=None):
        TextBox.__init__(self, name, text=value, desc=desc, prop=prop, style=style, attr=attr,
                         css_cls=css_cls, disabled=disabled, required=required,
                         onchange_callback=onchange_callback, app=app)
        self.add_property('type', 'url')


class Week(Date):
    """The Week widget allows the user to select a week and year.
    Depending on browser support, a date picker can show up in the input field.
    """

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 disabled=None, required=False, css_cls=None, onchange_callback=None,
                 app=None):
        Date.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                      css_cls=css_cls, disabled=disabled, required=required,
                      onchange_callback=onchange_callback, app=app)
        self.add_property('type', 'week')


class Form(Widget):
    """The Form widget defines a form that is used to collect user input. An form contains form
    elements. Form elements are different types of input elements, like text fields, checkboxes,
    radio buttons, submit buttons, and more. By default, this widget will display an submit
    button for the form, and form will get submitted with all the data from it's child elements,
    when the button will be pressed by the user. The submitted data can be fetched from form at
    server side using the followig method of this class: `get_submitted_form_data`. This method
    will return an dict of key-value pairs submitted from the frontend.
    """

    _use_fieldset = False
    _legend = None
    _form_submit_callback = None
    _app = None
    _action = None
    _url = None
    _submitted_form_data = None

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
                 use_fieldset=False, legend=None, app=None,
                 on_form_submit=None):
        """Default constructor for Form class with below parameters...
        Args:
                name (string): name of the widget for internal use
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                app (Flask, optional): An instance of `Flask` class
                use_fieldset (boolean, optional): Whether to use the fieldset to group the fields
                legend (string, optional): The legend/title of the fieldset to be shown on top of frame
                on_form_submit (func, optional): A reference to callback function/method that \
                will be called once the form is submitted successfully
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
        if on_form_submit is not None:
            self._form_submit_callback = on_form_submit
        if app is not None:
            self._app = app
        if use_fieldset is not None:
            self._use_fieldset = use_fieldset
        else:
            self._use_fieldset = False
        self._legend = legend
        if app is not None:
            self._url = self._register_rule()

    #  Event for the on form submit
    def on_form_submit(self, submit_callback, app=None):
        """An event handler that will be called once the form is submitted successfully.
        The parameter `submit_callback` should be an reference to method or function,
        which will be called after this event is triggered. The submitted form data
        can be collected using the method `get_submitted_form_data`, which will return
        an dict object with key-value pair of the submitted data
        """
        if app is not None:
            self._app = app
        self._form_submit_callback = submit_callback
        if self._app is not None:
            self._url = self._register_rule()

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
                                   self._process_on_form_submitted, methods=['GET', 'POST'])
        return rule_str
        # self.add_property('action', "/" + rule_str)

    def _attach_submit_button(self, url):
        content = """\n<button id="%s_btn" type="button" name="%s_btn"
                        onclick="
                            $.ajax({
                                url: '/%s',
                                data: $('#%s').serialize(),
                                type: 'post',
                                success: function(response){alertify.success('Form submitted successfully!')},
                                error: function(response){
                                                            alertify.error('Status Code: '
                                                                + err_status.status + '<br />' + 'Error Message:'
                                                                + err_status.statusText);
                                                            }
                            });
                        ">Submit</button>
                """ % (self._name, self._name, url, self._name)
        return content

    def _process_on_form_submitted(self):
        if request.form.__len__() > 0:
            self._submitted_form_data = request.form
        if self._form_submit_callback is not None:
            return json.dumps({'result': self._form_submit_callback(self._name, request.form)})
        return json.dumps({'result': ''})

    def get_submitted_form_data(self):
        """Returns the data submitted by the form in `dict` format. Value of each form elemet
        can be extracted from this `dict`. This function should be called only once the
        `submit_callback` is fired
        """
        return self._submitted_form_data

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
        self._widget_content = content + self._render_post_content('form')\
                                       + self._attach_submit_button(self._url)
        return self._widget_content


class DropDown(Widget):
    """Renders an dropdown widget with options passed as dict object or options added through
    `add_option` method of this class. This class has an another property known as `size`
    which helps in determining the number of options to be visible at a time in the dropdown.
    """

    _options = None
    _size = None
    _required = None
    _disabled = None
    _onclick_callback = None
    _onchange_callback = None
    _app = None
    _value = None

    def __init__(self, name, options=None, size=None, desc=None, prop=None, style=None, attr=None,
                 disabled=False, required=False, css_cls=None, onclick_callback=None, app=None,
                 onchange_callback=None):
        """Default constructor with the below given arguments...

            Args:
                name (str): Name or identifier of the widget
                options (dict, optional): A `dict` object containing options in key-value pair
                size (int, optional): The number of options to be displayed in dropdown
                desc (str, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                app (Flask, optional): An instance of `Flask` class
                disabled (boolean, optional): Sets the widget in disabled mode
                required (boolean, optional): Makes the widget as required field
                css_cls (list, optional): A list of CSS Classes to be used with widget
                onclick_callback (func, optional): A callback function or method to be called once
                                                    click event is triggered on widget
                onchange_callback (func, optional): A callback function or method to be called once
                                                    a change is done in the widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        if disabled:
            self.add_attribute('disabled')
            self._disabled = disabled
        else:
            self._disabled = False
        if required:
            self.add_attribute('required')
            self._required = required
        if size is not None:
            self.add_property('size', size)
            self._size = size
        else:
            self._size = 4
        if options is not None:
            self._options = options
        else:
            self._options = {}
        self._onchange_callback = onchange_callback
        self._onclick_callback = onclick_callback
        self._app = app
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
                    data: {'value': $('#%s').val()},
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
                        "value": $("#%s").val(),
                        "disabled": $("#%s").prop("disabled")
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
            dsbld = request.args["disabled"]
            if dsbld is not None:
                self._disabled = True if dsbld == "true" else False
            val = request.args["value"]
            if val is not None:
                self._value = val
        return json.dumps({'result': self._onchange_callback()})

    def _set_size(self, size):
        """Sets the size of the dropdown's height based on number of rows passed
        in `size` param. Ex, if size=3, 3 rows will be displayed in dropdown at a
        time and rest of it can be scrolled

            Args:
                size (int): Number of rows to be displayed in dropdown
        """
        self._size = size

    def _get_size(self):
        """Returns the number of rows that are displayed in the dropdown

            Returns:
                int: Number of rows that are displayed by dropdown
        """
        return self._size

    size = property(_get_size, _set_size, doc="Set or returns the number of rows that are displayed in the dropdown")

    def add_option(self, value, title=None, is_selected=False):
        """Adds a new option to the list of dropdown and
        can be marked as selected by passing the
        `is_selected` param as True

            Args:
                value (str): The value of the option to be added
                title (str, optional): The title of the value that will be shown in
                                        dropdown list. If it is blank, value will be
                                        used as title to be shown in the list
                is_selected (boolean, optional): Whether to show the current
                                                value as selected or not
        """
        self._options[value] = [title if title is not None else value, is_selected]

    def remove_options(self, value):
        """Removes the given option from the list

            Args:
                value (str): The value to be removed from the list
        """
        self._options.pop(value)

    def on_click(self, onclick_callback, app=None):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function. If no app is associated with current widget, it should be
        linked by passing `app` param

            Args:
                onclick_callback (function): The function/callback that will be called for this event
                app (Flask, optional): An instance of Flask app, though this param is optional, it is
                                        required to have events work properly. So, it should be passed
                                        during creation of widget in the constructor or should be passed
                                        in this function
        """
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self._attach_onclick()

    def on_change(self, onchange_callback, app=None):
        """Adds an event handler to on_change event of the widget. The event handler can be
        a method or function. If no app is associated with current widget, it should be
        linked by passing `app` param

            Args:
                onchange_callback (function): The function/callback that will be called for this event
                app (Flask, optional): An instance of Flask app, though this param is optional, it is
                                        required to have events work properly. So, it should be passed
                                        during creation of widget in the constructor or should be passed
                                        in this function
        """
        if app is not None:
            self._app = app
        self._onchange_callback = onchange_callback
        self._attach_onchange()

    def _sync_properties(self):
        return json.dumps({'disabled': self._disabled,
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
                                        selector.prop('disabled', props.disabled);
                                        selector.val(props.value)

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
        """Renders the dropdown list widget under its parent container
        using the `size` param to manage the height of dropdown
        """
        content = self._render_pre_content('select')
        content += "\n"
        for opt in self._options:
            opt_list = self._options.get(opt)
            title = str(opt_list[0])
            is_selected = opt_list[1]
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
        self._widget_content += "\n" + self._attach_polling()
        return self._widget_content


class Label(Button):
    """An label widget to display a text on the screen. The style can be handled
    by passing the `style` dict or the CSS class list to the constructor of the
    label
    """

    _text = None
    _for_widget = None

    def __init__(self, name, text, for_widget, desc=None, prop=None, style=None, attr=None,
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
        Button.__init__(self, name, text, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls, disabled=disabled, required=required,
                        onclick_callback=onclick_callback, app=app)
        self._text = text
        self._for_widget = for_widget
        self.add_property('for', for_widget.get_name())

    def render(self):
        """Renders the label content and associate it with other component if `for`
        param is passed and returns the content to parent widget for final rendering
        """
        content = self._render_pre_content('label')
        content += self._text
        self._widget_content = content + self._render_post_content('label')
        if self._app is not None and self._onclick_callback is not None:
            self._widget_content += "\n" + self._attach_polling()
        return self._widget_content
