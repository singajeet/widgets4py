"""
This module provides the functionality to add an JavaScript Tree widget to the app. It is a
wrapper on top of the famous javascript tree component `JSTree` (https://www.jstree.com).
To get more information about this componenet please visit JSTree's web site included above.
This module will handle the functionality to render the tree at frontend and setup the
communication between the client and server side code.
"""
from widgets4py.base import Widget
from flask import json, request


class JSTreeNode(Widget):
    """This class represents an node with in the JSTree. JSTreeNode renders
    as an "li" HTML tag and have couple of options associated with it like
    icon, text, etc
    """

    _is_opened = None
    _is_selected = None
    _is_disabled = None
    _icon = None
    _text = None
    _is_leaf = None

    def __init__(self, name, text, icon=None, is_opened=None, is_selected=None, is_disabled=None,
                 child_nodes=None):
        Widget.__init__(self, name)
        self._icon = icon
        self._text = text
        if is_opened is not None:
            self._is_opened = is_opened
        else:
            self._is_opened = False
        if is_selected is not None:
            self._is_selected = is_selected
        else:
            self._is_selected = False
        if is_disabled is not None:
            self._is_disabled = is_disabled
        else:
            self._is_disabled = False
        if child_nodes is not None:
            self._child_widgets = child_nodes
        else:
            self._child_widgets = []

    def render(self):
        content = "<li id='" + self._name + "' "
        content += "data-jstree='{"
        if self._is_opened:
            content += "\"opened\": true, "
        else:
            content += "\"opened\": false, "
        if self._is_selected:
            content += "\"selected\": true, "
        else:
            content += "\"selected\": false, "
        if self._is_disabled:
            content += "\"disabled\": true, "
        else:
            content += "\"disabled\": false, "
        if self._icon is not None:
            content += "icon: \"" + self._icon + "\" "
        content += "}'>"
        content += self._text
        if self._child_widgets is not None and self._child_widgets.__len__() > 0:
            content += "<ul>\n"
            for child in self._child_widgets:
                content += child.render() + "\n"
            content += "</ul></li>"
        else:
            content += "</li>"
        return content


class JSTree(Widget):
    """The JSTree class collects all the child nodes and renders the HTML content. Also,
    it handles some of the events fired on JSTree and further calls the callbacks
    associated with the Tree
    """

    def __init__(self, name, child_nodes=None):
        Widget.__init__(self, name)
        if child_nodes is not None:
            self._child_widgets = child_nodes
        else:
            self._child_widgets = []

    def _attach_script(self):
        script = """
                    <script>
                        $(function(){
                            $('#%s').jstree();
                        })();
                    </script>
                """ % (self._name)
        return script

    def render(self):
        content = self._render_pre_content('div')
        content += "<ul>"
        for child in self._child_widgets:
            content += child.render() + "\n"
        content += "</ul>"
        content += self._render_post_content('div')
        content += self._attach_script()
        return content
