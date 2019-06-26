"""
This module contains the basic widgets for building
GUI apps
Author: Ajeet Singh
Date: 06/25/2019
"""
from widgets4py.base import Widget


class Button(Widget):
    """A simple button class"""

    _onclick_callback = None
    _app = None

    def __init__(self, name, title, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False,
                 onclick_callback=None, app=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
        self.add_property('type', 'button')
        self.add_property('value', title)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')
        self._onclick_callback = onclick_callback
        self._app = app
        self._attach_onclick()

    def _attach_onclick(self):
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name).replace('_', '.')
            ajax = """
                $.ajax({
                    url: "/%s",
                    success: function(status){alert("success");},
                    error: function(status){alert("failed");}
                });
            """ % url
            self.add_property('onclick', ajax)
            self._app.add_url_rule('/' + url, url, self._onclick_callback)

    def on_click(self, onclick_callback, app=None):
        if app is not None:
            self._app = app
        self._onclick_callback = onclick_callback
        self._attach_onclick()

    def render(self):
        """Renders the content of button class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class TextBox(Widget):
    """A simple HTML textbox / input field"""

    def __init__(self, name, text=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
        self.add_property('type', 'text')
        if text is not None:
            self.add_property('value', text)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of textbox class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class CheckBox(Widget):
    """A simple HTML chexkbox / input field"""

    _title = None

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 title=None, readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
        self._title = title
        self.add_property('type', 'checkbox')
        if value is not None:
            self.add_property('value', value)
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of chexkbox class"""
        if self._title is None:
            content = self._render_pre_content('input')
            content += self._render_post_content('input')
            self._widget_content = content
            return self._widget_content
        else:
            content = "<div class='ui-widget-content'>\n"
            content += self._render_pre_content('input')
            content += self._render_post_content('input')
            content += "\n<label for='" + self._name + "'>" + self._title + "</label>"
            content += "\n<div>"


class Color(Widget):
    """A simple HTML color / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
        self.add_property('type', 'color')
        if readonly:
            self.add_attribute('readonly')
        if disabled:
            self.add_attribute('disabled')
        if required:
            self.add_attribute('required')

    def render(self):
        """Renders the content of color claskey, values"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class Date(Widget):
    """A simple HTML date / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 min=None, max=None, readonly=False, disabled=False,
                 required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
        self.add_property('type', 'date')
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
        """Renders the content of date class"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content
        return self._widget_content


class DateTimeLocal(Widget):
    """A simple HTML datetime-local / input field"""

    def __init__(self, name, value=None, desc=None, prop=None, style=None, attr=None,
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False, multiple=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 value=None, readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 alt_text=None, readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 min=None, max=None, readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 min=None, max=None, readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 pattern=None, readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 readonly=False, disabled=False, required=False):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
                 submit_callback=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
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
            rule_str = str(__name__ + "_" + name).replace(".", "_")
            app.add_url_rule('/' + rule_str,
                             rule_str,
                             self._on_form_submitted)
            self.add_property('action', "/" + rule_str)
        else:
            if action is not None:
                self.add_property('action', action)

    def on_form_submitted(self, func):
        self._on_form_submitted = func
        if self._app is not None and self._on_form_submitted is not None:
            rule_str = str(__name__ + "_" + self._name).replace('.', '_')
            self._app.add_url_rule('/' + rule_str,
                                   rule_str,
                                   self._on_form_submitted)
            self.add_property('action', '/' + rule_str)

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

    def __init__(self, name, readonly=False, disabled=False, required=False):
        pass
