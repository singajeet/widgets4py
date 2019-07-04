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

    def __init__(self, name, desc=None, prop=None, style=None, attr=None,
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
        self._app = app
        self._onclick_callback = onclick_callback
        self._disabled = disabled
        self._required = required

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
                            $("#%s").accordion();
                        });
                        </script>
                    """ % (self._name)
        self._widget_content = content
        return self._widget_content
