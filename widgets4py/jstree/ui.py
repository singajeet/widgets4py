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
    li_attr = None
    a_attr = None

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
        content = "{\n"
        content += "id: '" + self._name + "',\n"
        content += "text: '" + self._text + "',\n"
        if self._icon is not None:
            content += "icon: '" + self._icon + "',"
        content += "state: {\n"
        content += "    opened: " + json.dumps(self._is_opened) + ",\n"
        content += "    disabled: " + json.dumps(self._is_disabled) + ",\n"
        content += "    selected: " + json.dumps(self._is_selected) + ",\n"
        content += "\n},\n"
        content += "children: [\n"
        for child in self._child_widgets:
            content += child.render() + ",\n"
        content += "],\n"
        content += "li_attr: {},\n"
        content += "a_attr: {}"
        content += "\n}"
        return content

    # def render(self):
    #    content = "<li id='" + self._name + "' "
    #    content += "data-jstree='{"
    #    if self._is_opened:
    #        content += "\"opened\": true, "
    #    else:
    #        content += "\"opened\": false, "
    #    if self._is_selected:
    #        content += "\"selected\": true, "
    #    else:
    #        content += "\"selected\": false, "
    #    if self._is_disabled:
    #        content += "\"disabled\": true, "
    #    else:
    #        content += "\"disabled\": false, "
    #    if self._icon is not None:
    #        content += "\"icon\": \"" + self._icon + "\" "
    #    content += "}'>"
    #    content += self._text
    #    if self._child_widgets is not None and self._child_widgets.__len__() > 0:
    #        content += "\n<ul>\n"
    #        for child in self._child_widgets:
    #            content += child.render() + "\n"
    #        content += "\n</ul>\n</li>"
    #    else:
    #        content += "\n</li>"
    #    return content


class JSTree(Widget):
    """The JSTree class collects all the child nodes and renders the HTML content. Also,
    it handles some of the events fired on JSTree and further calls the callbacks
    associated with the Tree
    """

    _plugin_whole_row = None
    _plugin_checkbox = None
    _core_themes_variant = None
    _core_multiple = None
    _core_animation = None
    _core_chk_callbk_create_node = None
    _core_chk_callbk_rename_node = None
    _core_chk_callbk_delete_node = None
    _core_chk_callbk_move_node = None
    _core_chk_callbk_copy_node = None
    _core_chk_callbk_edit = None
    _checkbox_keep_selected_style = None

    def __init__(self, name, child_nodes=None, plugin_whole_row=None, plugin_checkbox=None, core_themes_variant=None,
                 core_multiple=None, core_animation=None, core_chk_callbk_create_node=None,
                 core_chk_callbk_rename_node=None, core_chk_callbk_delete_node=None, core_chk_callbk_move_node=None,
                 core_chk_callbk_copy_node=None, core_chk_callbk_edit=None, checkbox_keep_selected_style=None, ):
        Widget.__init__(self, name)
        if child_nodes is not None:
            self._child_widgets = child_nodes
        else:
            self._child_widgets = []
        self._plugin_whole_row = plugin_whole_row
        self._plugin_checkbox = plugin_checkbox
        self._core_themes_variant = core_themes_variant
        self._core_multiple = core_multiple
        self._core_animation = core_animation
        self._core_chk_callbk_create_node = core_chk_callbk_create_node
        self._core_chk_callbk_rename_node = core_chk_callbk_rename_node
        self._core_chk_callbk_delete_node = core_chk_callbk_delete_node
        self._core_chk_callbk_move_node = core_chk_callbk_move_node
        self._core_chk_callbk_copy_node = core_chk_callbk_copy_node
        self._core_chk_callbk_edit = core_chk_callbk_edit
        self._checkbox_keep_selected_style = checkbox_keep_selected_style

    def _attach_script(self):
        data = ""
        plugins = ""
        if self._plugin_whole_row is not None and self._plugin_whole_row:
            plugins += "'wholerow', "
        if self._plugin_checkbox is not None and self._plugin_checkbox:
            plugins += "'checkbox', "
        for child in self._child_widgets:
            data += child.render() + ",\n"
        script = """
                    <script>
                        $(function(){
                            $('#%s').jstree({
                                core: {
                                    data: [%s],
                                    themes: {
                                        variant: '%s'
                                    },
                                    multiple: %s,
                                    animation: %d,
                                    check_callback: function(operation, node, node_parent, node_position, more){
                                        if(operation === 'create_node'){
                                            return %s
                                        }
                                        if(operation === 'rename_node'){
                                            return %s
                                        }
                                        if(operation === 'delete_node'){
                                            return %s
                                        }
                                        if(operation === 'move_node'){
                                            return %s
                                        }
                                        if(operation === 'copy_node'){
                                            return %s
                                        }
                                        if(operation === 'edit'){
                                            return %s
                                        }
                                    }
                                },
                                plugins: [%s],
                                checkbox: {
                                    keep_selected_style: %s
                                }
                            });
                        })();
                    </script>
                """ % (self._name, data,
                       self._core_themes_variant if self._core_themes_variant is not None else 'large',
                       json.dumps(self._core_multiple if self._core_multiple is not None else False),
                       self._core_animation if self._core_animation is not None else 0,
                       json.dumps(self._core_chk_callbk_create_node
                                  if self._core_chk_callbk_create_node is not None else False),
                       json.dumps(self._core_chk_callbk_rename_node
                                  if self._core_chk_callbk_rename_node is not None else False),
                       json.dumps(self._core_chk_callbk_delete_node
                                  if self._core_chk_callbk_delete_node is not None else False),
                       json.dumps(self._core_chk_callbk_move_node
                                  if self._core_chk_callbk_move_node is not None else False),
                       json.dumps(self._core_chk_callbk_copy_node
                                  if self._core_chk_callbk_copy_node is not None else False),
                       json.dumps(self._core_chk_callbk_edit
                                  if self._core_chk_callbk_edit is not None else False),
                       plugins,
                       json.dumps(self._checkbox_keep_selected_style
                                  if self._checkbox_keep_selected_style is not None else False),
                       )
        return script

    def render(self):
        content = self._render_pre_content('div')
        # content += "\n<ul>\n"
        # for child in self._child_widgets:
        #    content += child.render() + "\n"
        # content += "</ul>"
        content += self._render_post_content('div')
        content += self._attach_script()
        return content
