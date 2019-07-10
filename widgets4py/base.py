"""The base widget module. All other widgets should inherit
from Widget class.

Author: Ajeet Singh
Date: 06/24/2019
"""


class Widget:
    """
    The `Widget` class will server as the base class to all the `Widget`(s) in this module.
    An widget can be a simple HTML element to be rendered on the web page or it can be an
    `AJAX` based widget which can be used in either web or desktop application. All widgets
    in this package should have structure shown below and it can have more attributes apart
    from the attributes/properties shown in the below structure...:
      \n  {
      \n      'tag': 'HTML tag name',
            'id': 'id of html node',
            'name': 'name of the element',
            'desc': 'description of widget',
            'styles': {
                        'style1': 'stylevalue1',
                        'style2': 'stylevalue2'
                        },
            'parent_tag': 'parent tag'
            'properties': {
                            'attribute1': 'value1',
                            'attribute2': 'value2'
                            ...
                            },
            'children': [
                            'child1',
                            'child2',
                            ...
                        ],
            'on_xxx_event_callback',
            'app' (instance of `Flask` app)
            ...
        }
    """
    _id = None
    _name = None
    _description = None

    _tag = "div"
    _widget_type = "DIV"

    _parent_widget = None
    _style = None  # {"height": "100%", "width": "100%"}
    _properties = None
    _child_widgets = None
    _widget_content = None
    _attributes = None
    _css_classes = None

    _root_widget = None

    def __init__(self, name, desc=None, tag=None, prop=None, style=None, attr=None, css_cls=None):
        """The default constructor have the following arguments...

            Parameters
            ----------
                name : str
                    Name of the widget to be used internally by the framework
                desc : str, optional
                    Description of the widget to be shown in tooltip
                tag : str, optional
                    HTML tag of the widget, by default it will be populated
                    with the respective class but can be used to create
                    custom widget if one is not available in the package
                prop : dict, optionl
                    A dictionary object containing the properties to be added to the
                    HTML tag. For example, {'type': 'submit'} will be rendered as
                    "type='submit'" in the HTML tag generated for this class
                style : dict, optional
                    Similar to the `prop` parameter, but render dict elements as
                    "style={color: red}" if following dict element is available in
                    the style parameter: {color: red}
                attr : list, optional
                    It will render the list elements as-is in the HTML tag for this
                    class. For example, ['required', 'disabled'] will be rendered as
                    "<... required disabled />" in the HTML tag
                css_cls : list, optional
                    This will render the class names inside the HTML tag, For example,
                    the value of css_cls is ['class1', 'class2'], same will be rendered
                    as "<... class='class1 class2' />" in the HTML tag
        """
        self._name = name
        self._id = name
        self._description = desc
        # init attributes
        self._child_widgets = []
        if tag is not None:
            self._tag = tag
            self._widget_type = str(tag).upper()

        if prop is not None:
            self._properties = prop
        else:
            self._properties = {}

        if style is not None:
            self._style = style
        else:
            self._style = {}

        if attr is not None:
            self._attributes = attr
        else:
            self._attributes = []

        if css_cls is not None:
            self._css_classes = css_cls
        else:
            self._css_classes = []

    def get_name(self):
        """Returns the name of this widget

            Returns:
                str: name of the widget
        """
        return self._name

    def set_root_widget(self, root_widget):
        """Sets the widget passed as arg as the root element of GUI structure

            Args:
                root_widget (Widget): An instance of the widget class to be set as
                                        root element
        """
        self._root_widget = root_widget

    def add(self, child):
        """Adds an child widget to the current widget

            Args:
                child (Widget): An child of the current widget
        """
        child.set_root_widget(self._root_widget)
        self._child_widgets.append(child)

    def remove(self, child):
        """Removes an child widget from the current parent widget. The child should
        exists as the member of children list of current widget

            Args:
                child (Widget): Child that needs to be removed from parent widget
        """
        self._child_widgets.remove(child)

    def set_properties(self, prop):
        """ Sets the list of properties to the current widget. The properties can be
        added to widget using the method `add_property` of the widget class

            Args:
                prop (list): A list of properties to be added to widget
        """
        self._properties.update(prop)

    def get_properties(self):
        """Returns all the properties associated with the current widget

            Returns:
                list: A list of properties that exists for an widget
        """
        return self._properties

    def add_property(self, key, value):
        """Adds an key-value property to the widget's properties. This will be rendered as
        shown, in the HTML tag, generated for the widget: "<... key='value' .../>"

            Args:
                key (str): Name or identifier of the record in the `dict` object
                value (object): A value that needs to be stored along the key
        """
        self._properties[key] = value

    def remove_property(self, key):
        """Removes an property from widget's properties matching the key passed as
        parameter

            Args:
                key (str): Name or identifier of the property
        """
        self._properties.pop(key)

    def set_styles(self, style):
        """Applies the dict of styles to the widget. The style names should be same as styles
        used in the CSS. All the styles will be rendered as CSS styles for the current widget
        in the HTML tag that will be generated for this widget. For example, if dict object
        is as follows : {'color': 'red'}, it will be rendered as "<... style='color: red;' ../>"

            Args:
                style (dict): A dict containing CSS style elements
        """
        self._style.update(style)

    def get_styles(self):
        """Returns the dict object containing the CSS style elements

            Returns:
                dict: A dict of CSS style elements
        """
        return self._style

    def add_style(self, style_name, style_value):
        """Add an CSS style element to the widget styles

            Args:
                style_name (str): Name or identifier of the CSS style to be applied
                style_value (str): Value of the style that needs to be applied on widget
        """
        self._style[style_name] = style_value

    def remove_style(self, style_name):
        """Removes an style from the widget's CSS style dict object

            Args:
                style_name (str): Name or identifier of the CSS style
        """
        self._style.pop(style_name)

    def set_attributes(self, attr):
        """Set's the list of attributes for an widget. The attributes will be rendered as
        follows, in the HTML tag for the widget: "<... readonly disabled .../>"

            Args:
                attr (list): A list of attributes to be rendered
        """
        self._attributes = attr

    def get_attributes(self):
        """Returns the attributes used for the current widget

            Returns:
                list: list of attributes for a given widget
        """
        return self._attributes

    def add_attribute(self, attr):
        """Adds an attribute to the list of attributes for a given widget

            Args:
                attr (str): An attribute to be added to attributes list
        """
        self._attributes.append(attr)

    def remove_attribute(self, attr):
        """Removes an attribute from the widget's attributes list

            Args:
                attr (str): Attribute that needs to be removed from list
        """
        self._attributes.pop(attr)

    def add_css_class(self, css_cls):
        """Adds an CSS class to the list of classes for a given widget

            Args:
                css_cls (str): Name of the class that needs to be added
        """
        self._css_classes.append(css_cls)

    def remove_css_class(self, css_cls):
        """Removes an CSS class from the list of classes for a given widget

            Args:
                css_cls (str): Name of the class that needs to be removed
        """
        self._css_classes.pop(css_cls)

    def _render_pre_content(self, tag):
        """Renders the pre markup code to write start HTML tag id,
        name, styles, properties, etc
        """
        # Render current nodes tag and id
        content = "\n<" + tag + " " \
            + "id='" + self._id + "' "\
            + "name='" + self._name + "' "

        # Render properties of the node
        for prop in self._properties:
            content += prop + "='" + self._properties.get(prop) + "' "
        # Render style attributes
        content += "style='"
        for style in self._style:
            content += style + ":" + self._style.get(style) + ";"
        content += "' "
        for attr in self._attributes:
            content += attr + " "
        content += "class='"
        for css_cls in self._css_classes:
            content += css_cls + " "
        content += "' "
        content += ">"
        return content

    def _render_post_content(self, tag):
        """Renders the post markup code to write the end HTML tag"""
        return "\n</" + tag + ">"

    def render(self):
        """Renders the widget as html markup and return same to the parent widget
        for final rendering
        """
        sub_content = ""
        # Get contents of child nodes
        for widget in self._child_widgets:
            sub_content += widget.render()
        main_content = self._render_pre_content(self._tag)
        # Merge sub content in the main content and add closing tag
        self._widget_content = main_content + sub_content + \
            self._render_post_content(self._tag)
        return self._widget_content


class Page(Widget):
    """The page class represents an HTML page and the root container that will host all
    other widgets at its children. All the widgets or their parent widgets needs to be
    added to Page instance to be shown on the screen. Apart from that the hyper links to
    the CSS and JavaScript files can be added through this class. Apart from that, this
    class provides the option to add the inline JavaScript to the page, so both a reference
    to JavaScript file and inline JavaScript can be added to the page at same time.
    """

    _script_sections = None
    _style_sections = None
    _jquery_section = """
                        <script>
                        $(function(){
                        %s
                        });
                        </script>
                        """
    _scripts = None
    _title = "Home"
    _jquery_css = True
    _jquery_js = True

    def __init__(self, name, title, desc=None, j_cc=True, j_js=True, prop=None,
                 style=None, attr=None, css_cls=None):
        """The default constructor have the following arguments...

            Parameters
            ----------
                name : str
                    Name of the widget to be used internally by the framework
                title : str
                    Title of the page to be rendered using this class
                desc : str, optional
                    Description of the widget to be shown in tooltip
                prop : dict, optionl
                    A dictionary object containing the properties to be added to the
                    HTML tag. For example, {'type': 'submit'} will be rendered as
                    "type='submit'" in the HTML tag generated for this class
                style : dict, optional
                    Similar to the `prop` parameter, but render dict elements as
                    "style={color: red}" if following dict element is available in
                    the style parameter: {color: red}
                attr : list, optional
                    It will render the list elements as-is in the HTML tag for this
                    class. For example, ['required', 'disabled'] will be rendered as
                    "<... required disabled />" in the HTML tag
                css_cls : list, optional
                    This will render the class names inside the HTML tag, For example,
                    the value of css_cls is ['class1', 'class2'], same will be rendered
                    as "<... class='class1 class2' />" in the HTML tag
                j_cc : boolean, optional
                    If set to true, it will add the CSS (CDN) URL to the page itself. The
                    URLS that will be added are for JQuery-UI, Alertify and JQuery Themes.
                    This option is `True` by default
                j_js : boolean, optional
                    If set to true, it will add the JQuery JavaScript URLs pointing to CDN,
                    to the current page. By default, this option is true and will add the
                    URL to following libraries: JQuery, JQuery-UI and Alertify
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._title = title
        self._jquery_css = j_cc
        self._jquery_js = j_js
        # init sections
        self._style_sections = []
        self._script_sections = []
        self._scripts = []
        self.set_root_widget(self)
        # add script if required
        if self._jquery_css:
            self.add_css('https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css')
            self.add_css('https://cdn.jsdelivr.net/npm/alertifyjs@1.11.4/build/css/alertify.min.css')
            self.add_css('https://cdn.jsdelivr.net/npm/alertifyjs@1.11.4/build/css/themes/bootstrap.min.css')
            self.add_css('http://w2ui.com/src/w2ui-1.5.rc1.min.css')
        if self._jquery_js:
            self.add_js('https://code.jquery.com/jquery-3.4.1.min.js')
            self.add_js('https://code.jquery.com/ui/1.12.1/jquery-ui.min.js')
            self.add_js('https://cdn.jsdelivr.net/npm/alertifyjs@1.11.4/build/alertify.min.js')
            self.add_js('http://code.jquery.com/jquery-2.1.1.min.js')
            self.add_js('http://w2ui.com/src/w2ui-1.5.rc1.min.js')

    def add_js(self, path):
        """Adds an reference to javascript file to the page. The JS file could from the available
        CDNs or can be from locally hosted static files. The PATH should be an full URL to JS file
        if it's hosted on CDN or it should be relative if hosted locally

            Args:
                path (str): Relative or absolute URL to the JS File
        """
        self._script_sections.append(path)

    def add_css(self, path):
        """Adds an reference to css file to the page. It works similar to `add_js` method but it works
        with CSS files instead of JS files.

            Args:
                path (str): Relative or absolute URL to the CSS file
        """
        self._style_sections.append(path)

    def add_script(self, script):
        """Adds an jquery code or script to the current page. The script will be rendered in the
        script section which exists inside the `Body` HTML tags of the page

            Args:
                script (str): The script or JS code that needs to be included in the page
        """
        self._scripts.append(script)

    def render(self):
        """Renders the page along with the links to various JS and CSS files, scripts in the script
        section and all of its children inside the `Body` tag of the page. This is the method that
        will send the compiled HTML page to the HTTP server for final rendering on the user's browser.
        """
        content = "<html style='height:100%;width:100%'>\n<head>\n"
        content += "<title>" + self._title + "</title>\n"
        css_content = "\n"
        for cssp in self._style_sections:
            css_content += "<link rel='stylesheet' href='" + cssp + "' />\n"
        js_content = "\n"
        for jsp in self._script_sections:
            js_content += "<script src='" + jsp + "'></script>\n"
        content += css_content
        content += js_content
        content += """  <script>
                            var $2 = jQuery.noConflict();
                        </script>
                    </head>
                    <body style='width: 100%; height: 100%'>
                    """
        script_content = ""
        for sc in self._scripts:
            script_content += sc + "\n"
        content += (self._jquery_section % script_content)
        content += "\n<div style='height:100%;width:100%;margin-top: 40px;' class='ui-widget'>"
        for widget in self._child_widgets:
            content += widget.render()
        content += "\n</div>\n</body>\n</html>"
        return content
