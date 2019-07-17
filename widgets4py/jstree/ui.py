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
        if submenu is not None:
            self._submenu = submenu
        else:
            self._submenu = {}

    def add(self, key, item):
        """Adds submenu item to the current menu item"""
        self._submenu[key] = item

    def remove(self, key):
        """Removes the submenu item from the current menu item"""
        self._submenu.pop(key)

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
    _plugin_contextmenu = None
    _plugin_dnd = None
    _plugin_massload = None
    _plugin_search = None
    _plugin_sort = None
    _plugin_state = None
    _plugin_types = None
    _plugin_unique = None
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
    _dnd_copy = None
    _dnd_always_copy = None
    _dnd_drag_selection = None
    _dnd_drag_selected_touch = None
    _dnd_large_drop_target = None
    _dnd_large_drag_target = None
    _dnd_use_html5 = None
    _search_ajax_url = None

    def __init__(self, name, child_nodes=None, plugin_whole_row=None, plugin_checkbox=None,
                 plugin_contextmenu=None, plugin_dnd=None, plugin_massload=None, plugin_search=None,
                 plugin_sort=None, plugin_state=None, plugin_types=None, plugin_unique=None,
                 core_themes_variant=None, core_themes_show_dots=None, core_themes_show_icons=None,
                 core_themes_show_stripes=None, core_multiple=None, core_animation=None,
                 core_expand_selected_onload=None, core_dblclick_toggle=None,
                 core_chk_callbk_create_node=None, core_chk_callbk_rename_node=None,
                 core_chk_callbk_delete_node=None, core_chk_callbk_move_node=None,
                 core_chk_callbk_copy_node=None, core_chk_callbk_edit=None,
                 checkbox_keep_selected_style=None, checkbox_visible=None, checkbox_three_state=None,
                 checkbox_whole_node=None, ctx_menu_select_node=None, ctx_menu_show_at_node=None,
                 ctx_submenu_items=None, dnd_copy=None, dnd_always_copy=None, dnd_drag_selection=None,
                 dnd_drag_selected_touch=None, dnd_large_drop_target=None, dnd_large_drag_target=None,
                 dnd_use_html5=None, search_ajax_url=None):
        Widget.__init__(self, name)
        if child_nodes is not None:
            self._child_widgets = child_nodes
        else:
            self._child_widgets = []
        self._plugin_whole_row = plugin_whole_row
        self._plugin_checkbox = plugin_checkbox
        self._plugin_contextmenu = plugin_contextmenu
        self._plugin_dnd = plugin_dnd
        self._plugin_massload = plugin_massload
        self._plugin_search = plugin_search
        self._plugin_sort = plugin_sort
        self._plugin_state = plugin_state
        self._plugin_types = plugin_types
        self._plugin_unique = plugin_unique
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
        if ctx_submenu_items is not None:
            self._ctx_submenu_items = ctx_submenu_items
        else:
            self._ctx_submenu_items = {}
        self._dnd_copy = dnd_copy
        self._dnd_always_copy = dnd_always_copy
        self._dnd_drag_selection = dnd_drag_selection
        self._dnd_drag_selected_touch = dnd_drag_selected_touch
        self._dnd_large_drop_target = dnd_large_drop_target
        self._dnd_large_drag_target = dnd_large_drag_target
        self._dnd_use_html5 = dnd_use_html5
        if search_ajax_url is not None:
            self._search_ajax_url = search_ajax_url
        else:
            self._search_ajax_url = str(__name__ + "_" + self._name + "_search")

    def add_ctx_menu_item(self, key, item):
        """Adds an context menu item to the `dict` of items where each element
        contains the key to be displayed in the menu and an object of class
        `ContextMenuItem`

            Args:
                key (string): Name or label of the menu item
                item (ContextMenuItem): An instance of `ContextMenuItem` class
        """
        self._ctx_submenu_items[key] = item

    def remove_ctx_menu_item(self, key):
        """Removes the menu item from the `dict` of submenus based on the key
        passed to this method
        """
        self._ctx_submenu_items.pop(key)

    def _get_plugins(self):
        plugins = ""
        if self._plugin_whole_row is not None and self._plugin_whole_row:
            plugins += "'wholerow', "
        if self._plugin_checkbox is not None and self._plugin_checkbox:
            plugins += "'checkbox', "
        if self._plugin_contextmenu is not None and self._plugin_contextmenu:
            plugins += "'contextmenu', "
        if self._plugin_dnd is not None and self._plugin_dnd:
            plugins += "'dnd', "
        if self._plugin_massload is not None and self._plugin_massload:
            plugins += "'massload', "
        if self._plugin_search is not None and self._plugin_search:
            plugins += "'search', "
        if self._plugin_sort is not None and self._plugin_sort:
            plugins += "'sort', "
        if self._plugin_state is not None and self._plugin_state:
            plugins += "'state', "
        if self._plugin_types is not None and self._plugin_types:
            plugins += "'types', "
        if self._plugin_unique is not None and self._plugin_unique:
            plugins += "'unique', "
        return plugins

    def _attach_script(self):
        data = ""
        plugins = ""
        # ================= Render Submenu Items ===================== #
        submenu = ""
        if self._ctx_submenu_items is not None and self._ctx_submenu_items.__len__() > 0:
            submenu = "items: {\n"
            for menu in self._ctx_submenu_items:
                submenu += self._ctx_submenu_items.get(menu).render() + ",\n"
            submenu += "\n}"
        # ==================== Render Plugins ========================== #
        plugins = self._get_plugins()
        # ==================== Render Child Nodes ====================== #
        for child in self._child_widgets:
            data += child.render() + ",\n"
        # =============== Build the final string for JSTree ============ #
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
                                    %s
                                },
                                dnd: {
                                    copy: %s,
                                    is_draggable: function(nodes, event){return true;},
                                    always_copy: %s,
                                    drag_selection: %s,
                                    touch: %s,
                                    large_drop_target: %s,
                                    large_drag_target: %s,
                                    use_html5: %s
                                },
                                search: {
                                    ajax: {
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json'
                                    }
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
                       submenu,
                       json.dumps(self._dnd_copy if self._dnd_copy is not None else True),
                       json.dumps(self._dnd_always_copy
                                  if self._dnd_always_copy is not None else False),
                       json.dumps(self._dnd_drag_selection
                                  if self._dnd_drag_selection is not None else True),
                       ("'selected'"
                        if self._dnd_drag_selected_touch is not None and self._dnd_drag_selected_touch
                        else json.dumps(False)),
                       json.dumps(self._dnd_large_drop_target
                                  if self._dnd_large_drop_target is not None else False),
                       json.dumps(self._dnd_large_drag_target
                                  if self._dnd_large_drag_target is not None else False),
                       json.dumps(self._dnd_use_html5 if self._dnd_use_html5 is not None else False),
                       self._search_ajax_url
                       )
        return script

    def render(self):
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += self._attach_script()
        return content
