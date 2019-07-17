"""
This module provides the functionality to add an JavaScript Tree widget to the app. It is a
wrapper on top of the famous javascript tree component `JSTree` (https://www.jstree.com).
To get more information about this componenet please visit JSTree's web site included above.
This module will handle the functionality to render the tree at frontend and setup the
communication between the client and server side code.
"""
from widgets4py.base import Widget
from flask import json  # , request


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


class ContextMenuItem:
    """A JSTree's context menu item that will appear in the context menu of a node.
    Each item must have the following two attributes as mandatory: label and action,
    other attributes are optional. An `dict` of objects should be passed to JSTree
    having each element an key and object of this class
    """

    _sep_before = None
    _sep_after = None
    _disabled = None
    _label = None
    _title = None
    _action = None
    _icon = None
    _shortcut = None
    _shortcut_label = None
    _submenu = None

    def __init__(self, label, action, title=None, icon=None, sep_before=None, sep_after=None,
                 disabled=None, shortcut=None, shortcut_label=None, submenu=None):
        self._label = label
        self._action = action
        self._title = title
        self._icon = icon
        self._sep_before = sep_before
        self._sep_after = sep_after
        self._disabled = disabled
        self._shortcut = shortcut
        self._shortcut_label = shortcut_label
        self._submenu = submenu

    def render(self):
        """Renders the context menu """
        content = "'" + self._label + "': {\n"
        if self._sep_before is not None:
            content += "seperator_before: %s,\n" % json.dumps(self._sep_before)
        if self._sep_after is not None:
            content += "separator_after: %s,\n" % json.dumps(self._sep_after)
        if self._disabled is not None:
            content += "_disabled: %s,\n" % json.dumps(self._disabled)
        content += "label: '%s',\n" % (self._label)
        content += "action: %s,\n" % (self._action)
        if self._title is not None:
            content += "title: '%s',\n"
        if self._icon is not None:
            content += "icon: '%s',\n"
        if self._shortcut is not None:
            content += "shortcut: '%s',\n"
        if self._shortcut_label is not None:
            content += "shortcut_label: '%s',\n"
        if self._submenu is not None and self._submenu.__len__() > 0:
            content += "submenu: {\n"
            for menu in self._submenu:
                content += self._submenu.get(menu).render() + ",\n"
            content += "\n}"
        content += "\n}"
        return content


class JSTree(Widget):
    """The JSTree class collects all the child nodes and renders the HTML content. Also,
    it handles some of the events fired on JSTree and further calls the callbacks
    associated with the Tree
    """

    _plugin_whole_row = None
    _plugin_checkbox = None
    _core_themes_variant = None
    _core_themes_show_dots = None
    _core_themes_show_icons = None
    _core_themes_show_stripes = None
    _core_expand_selected_onload = None
    _core_multiple = None
    _core_animation = None
    _core_dblclick_toggle = None
    _core_chk_callbk_create_node = None
    _core_chk_callbk_rename_node = None
    _core_chk_callbk_delete_node = None
    _core_chk_callbk_move_node = None
    _core_chk_callbk_copy_node = None
    _core_chk_callbk_edit = None
    _checkbox_keep_selected_style = None
    _checkbox_visible = None
    _checkbox_three_state = None
    _checkbox_whole_node = None
    _ctx_menu_select_node = None
    _ctx_menu_show_at_node = None
    _ctx_submenu_items = None

    def __init__(self, name, child_nodes=None, plugin_whole_row=None, plugin_checkbox=None,
                 core_themes_variant=None, core_themes_show_dots=None, core_themes_show_icons=None,
                 core_themes_show_stripes=None, core_multiple=None, core_animation=None,
                 core_expand_selected_onload=None, core_dblclick_toggle=None,
                 core_chk_callbk_create_node=None, core_chk_callbk_rename_node=None,
                 core_chk_callbk_delete_node=None, core_chk_callbk_move_node=None,
                 core_chk_callbk_copy_node=None, core_chk_callbk_edit=None,
                 checkbox_keep_selected_style=None, checkbox_visible=None,
                 checkbox_three_state=None, checkbox_whole_node=None,
                 ctx_menu_select_node=None, ctx_menu_show_at_node=None,
                 ctx_submenu_items=None):
        Widget.__init__(self, name)
        if child_nodes is not None:
            self._child_widgets = child_nodes
        else:
            self._child_widgets = []
        self._plugin_whole_row = plugin_whole_row
        self._plugin_checkbox = plugin_checkbox
        self._core_themes_variant = core_themes_variant
        self._core_themes_show_dots = core_themes_show_dots
        self._core_themes_show_icons = core_themes_show_icons
        self._core_themes_show_icons = core_themes_show_stripes
        self._core_expand_selected_onload = core_expand_selected_onload
        self._core_multiple = core_multiple
        self._core_animation = core_animation
        self._core_dblclick_toggle = core_dblclick_toggle
        self._core_chk_callbk_create_node = core_chk_callbk_create_node
        self._core_chk_callbk_rename_node = core_chk_callbk_rename_node
        self._core_chk_callbk_delete_node = core_chk_callbk_delete_node
        self._core_chk_callbk_move_node = core_chk_callbk_move_node
        self._core_chk_callbk_copy_node = core_chk_callbk_copy_node
        self._core_chk_callbk_edit = core_chk_callbk_edit
        self._checkbox_keep_selected_style = checkbox_keep_selected_style
        self._checkbox_visible = checkbox_visible
        self._checkbox_three_state = checkbox_three_state
        self._checkbox_whole_node = checkbox_whole_node
        self._ctx_menu_select_node = ctx_menu_select_node
        self._ctx_menu_show_at_node = ctx_menu_show_at_node
        self._ctx_submenu_items = ctx_submenu_items

    def _attach_script(self):
        data = ""
        plugins = ""
        submenu = "{\n"
        if self._ctx_submenu_items is not None:
            for menu in self._ctx_submenu_items:
                submenu += self._ctx_submenu_items.get(menu).render() + ",\n"
        submenu += "\n}"
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
                                        variant: '%s',
                                        dots: %s,
                                        icons: %s,
                                        stripes: %s
                                    },
                                    expand_selected_onload: %s,
                                    multiple: %s,
                                    animation: %d,
                                    dblclick_toggle: %s,
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
                                    },
                                    error: function(err_status){
                                        alertify('Error while working with JSTree: ' + str(err_status))
                                    }
                                },
                                plugins: [%s],
                                checkbox: {
                                    keep_selected_style: %s,
                                    visible: %s,
                                    three_state: %s,
                                    whole_node: %s,
                                },
                                contextmenu: {
                                    select_node: %s,
                                    show_at_node: %s,
                                    submenu: %s
                                }
                            });
                        })();
                    </script>
                """ % (self._name, data,
                       self._core_themes_variant if self._core_themes_variant is not None else 'large',
                       json.dumps(self._core_themes_show_dots
                                  if self._core_themes_show_dots is not None else True),
                       json.dumps(self._core_themes_show_icons
                                  if self._core_themes_show_icons is not None else True),
                       json.dumps(self._core_themes_show_stripes
                                  if self._core_themes_show_stripes is not None else False),
                       json.dumps(self._core_expand_selected_onload
                                  if self._core_expand_selected_onload is not None else False),
                       json.dumps(self._core_multiple if self._core_multiple is not None else False),
                       self._core_animation if self._core_animation is not None else 0,
                       json.dumps(self._core_dblclick_toggle
                                  if self._core_dblclick_toggle is not None else True),
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
                       json.dumps(self._checkbox_visible if self._checkbox_visible is not None else True),
                       json.dumps(self._checkbox_three_state if self._checkbox_three_state is not None else True),
                       json.dumps(self._checkbox_whole_node if self._checkbox_whole_node is not None else False),
                       json.dumps(self._ctx_menu_select_node if self._ctx_menu_select_node is not None else True),
                       json.dumps(self._ctx_menu_show_at_node if self._ctx_menu_show_at_node is not None else True),
                       submenu
                       )
        return script

    def render(self):
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += self._attach_script()
        return content
