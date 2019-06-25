"""The base widget module. All other widgets should inherit
from Widget class.

Author: Ajeet Singh
Date: 06/24/2019
"""


class Widget:
    """
    The object of this class should resemble the following
    structure...:
        {
            'tag': 'HTML tag name',
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
                            },
            'children': [
                        {
                            'tag': 'div'
                            'id': 'child1'
                            ...
                        },
                        {
                            'tag': 'div',
                            'id': 'child2'
                            ...
                        },
                        ...
            ]
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

    def __init__(self, name, desc=None, tag=None, prop=None, style=None, attr=None):
        """Default constructor"""
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

    def add(self, child):
        """Adds an child to current instance

            Args:
                child (Widget): An child of the current object
        """
        self._child_widgets.append(child)

    def remove(self, child):
        """Removes an child from the current object children

            Args:
                child (Widget): Child to be removed
        """
        self._child_widgets.remove(child)

    def set_properties(self, prop):
        """Properties setter"""
        self._properties.update(prop)

    def get_properties(self):
        """properties getter"""
        return self._properties

    def add_property(self, key, value):
        """Adds an property to object's properties"""
        self._properties[key] = value

    def remove_property(self, key):
        """Removes an property from object's properties"""
        self._properties.pop(key)

    def set_styles(self, style):
        """Applies an style to HTML node """
        self._style.update(style)

    def get_styles(self):
        """Removes the whole style from HTML element"""
        return self._style

    def add_style(self, style_name, style_value):
        """Add an style to object's styles"""
        self._style[style_name] = style_value

    def remove_style(self, style_name):
        """Removes an style from the object"""
        self._style.pop(style_name)

    def set_attributes(self, attr):
        """Attributes setter """
        self._attributes = attr

    def get_attributes(self):
        """Attributes getter"""
        return self._attributes

    def add_attribute(self, attr):
        """Adds an attribute to the object"""
        self._attributes.append(attr)

    def remove_attribute(self, attr):
        """Removes an attributes from the object"""
        self._attributes.pop(attr)

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
        content += ">"
        return content

    def _render_post_content(self, tag):
        """Renders the post markup code to write the end HTML tag"""
        return "\n</" + tag + ">"

    def render(self):
        """Renders the widget as html script and returns
        same"""
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
    """The page class represents an HTML page with options
    to include CSS AND JS libs
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

    def __init__(self, name, title, desc=None, j_cc=True, j_js=True, prop=None, style=None, attr=None):
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr)
        self._title = title
        self._jquery_css = j_cc
        self._jquery_js = j_js
        # init sections
        self._style_sections = []
        self._script_sections = []
        self._scripts = []
        # add script if required
        if self._jquery_css:
            self.add_css('https://code.jquery.com/ui/1.12.1/themes/black-tie/jquery-ui.css')
        if self._jquery_js:
            self.add_js('https://code.jquery.com/jquery-3.4.1.min.js')
            self.add_js('https://code.jquery.com/ui/1.12.1/jquery-ui.min.js')

    def add_js(self, path):
        """Adds an javascript file to the page """
        self._script_sections.append(path)

    def add_css(self, path):
        """Adds an css file to the page """
        self._style_sections.append(path)

    def add_script(self, script):
        """Adds an jquery script to page """
        self._scripts.append(script)

    def render(self):
        """Renders the page """
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
        content += "\n</head>\n<body style='width: 100%; height: 100%'>"
        script_content = ""
        for sc in self._scripts:
            script_content += sc + "\n"
        content += (self._jquery_section % script_content)
        content += "\n<div style='height:100%;width:100%'>"
        for widget in self._child_widgets:
            content += widget.render()
        content += "\n</div>\n</body>\n</html>"
        return content
