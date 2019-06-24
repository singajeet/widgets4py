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
            'styles': 'css style',
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
    _style = "height: 100%; width: 100%; "
    _properties = {}
    _child_wigets = []
    _widget_content = None

    def __init__(self, name, desc=None, tag=None, prop=None, style=None):
        """Default constructor"""
        self._name = name
        self._id = name
        self._description = desc
        if tag is not None:
            self._tag = tag
            self._widget_type = str(tag).upper()

        if prop is not None:
            self._properties = prop

        if style is not None:
            self._style += style

    def add_to_parent(self, parent):
        """Adds the current object to provided widget
        instance

            Args:
                parent (Widget): An parent widget object
        """
        self._parent_widget = parent
        parent.add(self)

    def remove_from_parent(self, parent):
        """Removes the current object from the parent

            Args:
                parent (Widget): Parent widget object
        """
        parent.remove(self)
        self._parent_widget = None

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
        self._properties = prop

    def get_properties(self):
        """properties getter"""
        return self._properties

    def add_property(self, key, value):
        """Adds an property to object's properties"""
        self._properties[key] = value

    def remove_property(self, key):
        """Removes an property from object's properties"""
        self._properties.pop(key)

    def apply_style(self, style):
        """Applies an style to HTML node """
        self._style += style

    def remove_style(self):
        """Removes the whole style from HTML element"""
        self._style = None

    def render(self):
        """Renders the widget as html script and returns
        same"""
        sub_content = None
        # Get contents of child nodes
        for widget in self._child_wigets:
            sub_content += widget.render()
        # Remder current nodes tag and id
        main_content = ("<" + self._tag + " "
                        + "id='" + self._id + "' "
                        + "name='" + self._name + "' "
                        )
        # Render properties of the node
        for prop in self._properties:
            main_content += prop + "='" + self._properties.get(prop) + "' "
        main_content += "style='" + self._style if self._style is not None else "" + "' >"
        self._widget_content = main_content + sub_content + "</" + self._tag + ">"
        return self._widget_content
