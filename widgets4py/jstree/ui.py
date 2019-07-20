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
    _li_attr = None
    _a_attr = None
    _type = None

    def __init__(self, name, text, icon=None, is_opened=None, is_selected=None, is_disabled=None,
                 child_nodes=None, li_attr=None, a_attr=None, n_type=None):
        """This class represents an item or node in the JSTree. A node can be a parent to other
        nodes or it can be an leaf which means it doesn't have any child nodes. A node represents
        an data in the tree and shows the parent-child replationship visually. Each node should
        have an id (or name) and text (i.e., label) associated with it. A node is rendered using
        the HTML "li" tag, hence all the HTML attributes for an "li" tag can be applied to the
        node. The node's text (or lable) is wrapped in the "a" HTML tag and attributes related to
        "a" tag can also be applied on the node.

            Args:
                name (string, required): a unique identifier or name of the node
                text (string, required): Label to be shown for the current node in the JSTree
                icon (string): A CSS class name containing the icon information
                is_opened (boolean): Initial state of the node to show it as open or closed
                is_selected (boolean): If set True, node will be rendered selected in the tree
                is_disabled (boolean): If True, node will be rendered as disabled in the tree
                child_nodes (list): List of direct child nodes of type `JSTreeNode` for the current node
                li_attr (string): A list of HTML attributes which will be applied to underlying <li> tag
                a_attr (string): A list of HTML attributes to be applied on the uderlying <a> tag
                n_type (`JSTreeNodeType`): An instance of the class `JSTreeNodeType`
        """
        Widget.__init__(self, name)
        self._icon = icon
        self._text = text
        self._li_attr = li_attr
        self._a_attr = a_attr
        self._type = n_type
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

    @property
    def icon(self):
        """The name of the CSS class containing the icon to be shown for this node
        """
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val

    @property
    def text(self):
        """The label to be shown for the current node"""
        return self._text

    @text.setter
    def text(self, val):
        self._text = val

    @property
    def li_attr(self):
        """The HTML "li" attributes to be applied to current node"""
        return self._li_attr

    @li_attr.setter
    def li_attr(self, val):
        self._li_attr = val

    @property
    def a_attr(self):
        """The HTML "a" attributes to be applied to the current node's label"""
        return self._a_attr

    @a_attr.setter
    def a_attr(self, val):
        self._a_attr = val

    @property
    def is_open(self):
        """Returns whether current node is opened or closed"""
        return self._is_opened

    @is_open.setter
    def is_open(self, val):
        self._is_opened = val

    @property
    def is_selected(self):
        """Returns whether current node is selected or not"""
        return self._is_selected

    @is_selected.setter
    def is_selected(self, val):
        self._is_selected = val

    @property
    def is_disabled(self):
        """Returns whether the current node is disabled or not"""
        self._is_disabled

    @is_disabled.setter
    def is_disabled(self, val):
        self._is_disabled = val

    @property
    def is_parent(self):
        """Returns whether the current node is parent to other child nodes or not"""
        if self._child_widgets.__len__() > 0:
            return True
        return False

    @property
    def is_leaf(self):
        """Returns `True` if current node is an leaf else returns `False`"""
        if self._child_widgets.__len__() > 0:
            return False
        return True

    @property
    def is_closed(self):
        """Returns `True` if current node is closed else returns `False`"""
        if self._is_opened:
            return False
        return True

    def get_children_dom(self):
        """Returns the list of all the child nodes available under the current `JSTreeNode`"""
        return self._child_widgets

    def get_next_dom(self, strict):
        """Returns the next visible node that is below the current node. If strict is set to `True`
        only sibling nodes are returned """
        if not strict:
            if self._child_widgets is not None and\
                    self._child_widgets.__len__() > 0:
                for child in self._child_widgets:
                    if not child.is_disabled:
                        return child
        elif self._parent_widget is not None:
            if self._parent_widget._child_widgets is not None and\
                    self._parent_widget._child_widgets.__len__() > 0:
                siblings = self._parent_widget._child_widgets
                return siblings
        return None

    def get_prev_dom(self, strict):
        """Returns the previous visible node that is above the current node. If strict is set to
        `True` only sibling nodes are returned"""
        if not strict:
            if self._parent_widget is not None:
                return self._parent_widget
        elif self._parent_widget is not None:
            siblings = self._parent_widget._child_widgets
            return siblings
        return None

    def get_path(self):
        """Returns the path from root node to current node separated by front slash (/)"""
        path = "/" + self._name
        node = self
        while node is not None:
            parent_node = node.get_parent()
            if parent_node is not None:
                path = "/" + parent_node._name + path
            node = parent_node
        return path

    def render(self):
        """Renders the content of the `JSTreeNode` within the parent widget (i.e., `JSTree`) of this node"""
        content = "{\n"
        content += "id: '" + self._name + "',\n"
        content += "text: '" + self._text + "',\n"
        if self._type is not None:
            content += "type: '" + self._type + "',\n"
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


class JSTreeNodeType:
    """Type of the JSTree Node. Be default there are two types provided by the framework
    which are '#' (aka, root) and 'default'. Types have some properties associated with it and
    it applies to all those nodes which are of that type. For example, if type `ABCType` has a
    specific icon property defined as 'myIcon', all nodes having its 'type': 'ABCType' will get the
    icon value as 'myIcon'
    """

    _name = None
    _max_children = None
    _max_depth = None
    _valid_children = None
    _icon = None
    _li_attr = None
    _a_attr = None

    def __init__(self, name, max_children=None, max_depth=None, valid_children=None, icon=None,
                 li_attr=None, a_attr=None):
        """Following are the parameters to the constructor of this class:

            Args:
                name (string, required): A unique identifier for the given type
                max_children (int): Maximum number of child nodes, a parent node can have
                max_depth (int): Maximum level of child nodes, a parent node can have
                valid_children (boolean): Set to `True` if all the child nodes are valid
                icon (string): The CSS class name which contains the icon information
                li_attr (string): A list of HTML "li" attributes that can be applied to the node
                a_attr (string): A list of HTML "a" attributes that the current node can have
        """
        self._name = name
        self._max_children = max_children
        self._max_depth = max_depth
        self._valid_children = valid_children
        self._icon = icon
        self._li_attr = li_attr
        self._a_attr = a_attr

    def render(self):
        """Renders the JavaScript code for the `JSTreeNodeType` which is further used by the
        framework to work with types in `JSTreeNode`
        """
        content = "'" + self._name + "': {\n"
        if self._max_children is not None:
            content += "max_children: " + str(self._max_children) + ",\n"
        if self._max_depth is not None:
            content += "max_depth: " + str(self._max_depth) + ",\n"
        if self._valid_children is not None:
            content += "valid_children: '" + self._valid_children + "',\n"
        if self._icon is not None:
            content += "icon: '" + self._icon + "',\n"
        if self._li_attr is not None:
            content += "li_attr: '" + self._li_attr + "',\n"
        if self._a_attr is not None:
            content += "a_attr: '" + self._a_attr + "',\n"
        content += "\n}"
        return content


class ContextMenuItem:
    """A JSTree's context menu item that will appear in the context menu of a node.
    A item can be a submenu or can be a leaf menu with an action associated with it.
    Each item must have the following two attributes as mandatory: `label` and `action`,
    other attributes in this class are optional.

    To build the context menu for `JSTree`, an `dict` should be passed to JSTree, having each
    of its element as a key and object pair. The `key` represents the label of the menu item
    and the object is the instace of this class with desired properties filled
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
        """Adds submenu item or the leaf menu item to the current menu

            Args:
                key (string): Key and the label of menu item
                item (ContextMenuItem): An instance of this class having its desired properties filled
        """
        self._submenu[key] = item

    def remove(self, key):
        """Removes the submenu item from the current menu item

            Args:
                key (string): A key associated with the context menu item
        """
        self._submenu.pop(key)

    def render(self):
        """Renders the JavaScript to build the context menu for the `JSTree`"""
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
    associated with the Tree. JSTree have a lot of configurations which can be configured
    through the constructor of this class. Also, this class have a lot of events associated
    which can be used to register handlers with it.
    """

    _app = None
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
    _checkbox_tie_selection = None
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
    _search_callback = None
    _search_case_sensitive = None
    _search_show_only_matches = None
    _search_close_opened_onclear = None
    _sort_callback = None
    _sort_url = None
    _types = None
    _unique_case_sensitive = None
    _unique_trim_whitespace = None
    _unique_duplicate_url = None
    _unique_duplicate_callback = None
    _cmd_queue = None
    # ========= Events ============= #
    _loaded_callback = None
    _ready_callback = None
    _load_node_callback = None
    _model_callback = None
    _redraw_callback = None
    _before_open_callback = None
    _open_node_callback = None
    _after_open_callback = None
    _close_node_callback = None
    _after_close_callback = None
    _activate_node_callback = None
    _hover_node_callback = None
    _dehover_node_callback = None
    _select_node_callback = None
    _changed_callback = None
    _set_text_callback = None
    _create_node_callback = None
    _rename_node_callback = None
    _delete_node_callback = None
    _move_node_callback = None
    _copy_node_callback = None
    _copy_callback = None
    _cut_callback = None
    _paste_callback = None
    _check_node_callback = None
    _uncheck_node_callback = None
    _show_contextmenu_callback = None
    _search_ajax_callback = None
    _clear_search_callback = None
    # ============================== #
    _loaded_url = None
    _ready_url = None
    _load_node_url = None
    _model_url = None
    _redraw_url = None
    _before_open_url = None
    _open_node_url = None
    _after_open_url = None
    _close_node_url = None
    _after_close_url = None
    _activate_node_url = None
    _hover_node_url = None
    _dehover_node_url = None
    _select_node_url = None
    _changed_url = None
    _set_text_url = None
    _create_node_url = None
    _rename_node_url = None
    _delete_node_url = None
    _move_node_url = None
    _copy_node_url = None
    _copy_url = None
    _cut_url = None
    _paste_url = None
    _check_node_url = None
    _uncheck_node_url = None
    _show_contextmenu_url = None
    _search_url = None
    _clear_search_url = None

    def __init__(self, name, app=None, child_nodes=None, plugin_whole_row=None, plugin_checkbox=None,  # noqa
                 plugin_contextmenu=None, plugin_dnd=None, plugin_massload=None, plugin_search=None,
                 plugin_sort=None, plugin_state=None, plugin_types=None, plugin_unique=None,
                 core_themes_variant=None, core_themes_show_dots=None, core_themes_show_icons=None,
                 core_themes_show_stripes=None, core_multiple=None, core_animation=None,
                 core_expand_selected_onload=None, core_dblclick_toggle=None,
                 core_chk_callbk_create_node=None, core_chk_callbk_rename_node=None,
                 core_chk_callbk_delete_node=None, core_chk_callbk_move_node=None,
                 core_chk_callbk_copy_node=None, core_chk_callbk_edit=None,
                 checkbox_keep_selected_style=None, checkbox_tie_selection=None, checkbox_visible=None,
                 checkbox_three_state=None, checkbox_whole_node=None,
                 ctx_menu_select_node=None, ctx_menu_show_at_node=None,
                 ctx_submenu_items=None, dnd_copy=None, dnd_always_copy=None, dnd_drag_selection=None,
                 dnd_drag_selected_touch=None, dnd_large_drop_target=None, dnd_large_drag_target=None,
                 dnd_use_html5=None, search_ajax_url=None, search_ajax_callback=None, search_case_sensitive=None,
                 search_show_only_matches=None, search_close_opened_onclear=None, sort_callback=None,
                 sort_url=None, types=None, unique_case_sensitive=None, unique_trim_whitespace=None,
                 unique_duplicate_url=None, unique_duplicate_callback=None):
        """Constructor parameters defined below...

            Args:
                name (string, required): An id or name of the widget to be used internally
                app (Flask): An instance of `Flask` class as application object
                child_nodes (JSTreeNode): A list of direct child nodes of this class
                plugin_whole_row (boolean): Whether to enable 'whole_row' plugin or not. The
                                            whole_row plugins to select whole row of the tree
                                            instead of just selecting the tree node
                plugin_checkbox (boolean): Whether to enable or disable checkbox plugin which
                                            helps in rendering a checkbox in front of each node
                plugin_contextmenu (boolean): Enables or disables an context menu to be associated
                                                with the `JSTree`. Depending upon the configuration
                                                a context menu can have system populated items such
                                                as "Create", "Rename", "Delete", etc or it can have
                                                custom menu items as configured for the JSTree
                plugin_dnd (boolean): Enables or disable the drag & drop plugin. The plugin
                                        helps in dragging and dropping tree nodes, which also
                                        helps visiualization of cut, copy & paste commands
                plugin_massload (boolean): This plugin helps in the getting the mass load of the nodes
                                            through AJAX calls
                plugin_search (boolean): This plugin helps in making the JSTree as searchable. A user
                                            can submit the search query which could be processed at
                                            either client side or server side depending upon the
                                            configuration. Search helps in finding the `JSTreeNode`
                                            and filtering out the nodes which are of no interset
        """
        Widget.__init__(self, name)
        self._app = app
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
        self._checkbox_tie_selection = checkbox_tie_selection
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
            self._search_ajax_url = str(__name__ + "_" + self._name + "_search").replace('.', '_')
            if self._app is not None:
                found = False
                for rule in self._app.url_map.iter_rules():
                    if rule.endpoint == self._search_ajax_url:
                        found = True
                if not found:
                    self._app.add_url_rule('/' + self._search_ajax_url,
                                           self._search_ajax_url, self._process_search_ajax_callback)
        self._search_ajax_callback = search_ajax_callback
        self._search_case_sensitive = search_case_sensitive
        self._search_show_only_matches = search_show_only_matches
        self._search_close_opened_onclear = search_close_opened_onclear
        self._sort_callback = sort_callback
        if sort_url is not None:
            self._sort_url = sort_url
        else:
            self._sort_url = str(__name__ + "_" + self._name + "_sort").replace('.', '_')
            if self._app is not None:
                found = False
                for rule in self._app.url_map.iter_rules():
                    if rule.endpoint == self._sort_url:
                        found = True
                if not found:
                    self._app.add_url_rule('/' + self._sort_url, self._sort_url, self._process_sort_callback)
        if types is not None:
            self._types = types
        else:
            self._types = {}
        self._unique_case_sensitive = unique_case_sensitive
        self._unique_trim_whitespace = unique_trim_whitespace
        self._unique_duplicate_callback = unique_duplicate_callback
        if unique_duplicate_url is not None:
            self._unique_duplicate_url = unique_duplicate_url
        else:
            self._unique_duplicate_url = str(__name__ + "_" + self._name + "_unique_duplicate").replace('.', '_')
            if self._app is not None:
                found = False
                for rule in self._app.url_map.iter_rules():
                    if rule.endpoint == self._unique_duplicate_url:
                        found = True
                if not found:
                    self._app.add_url_rule('/' + self._unique_duplicate_url,
                                           self._unique_duplicate_url, self._process_unique_duplicate_callback)
        self._cmd_queue = []

    def _process_unique_duplicate_callback(self):
        name = ""
        counter = 0
        if request.args.__len__() > 0:
            name = request.args['name']
            counter = int(request.args['counter'])
        if self._unique_duplicate_callback is not None:
            return json.dumps({'result': self._unique_duplicate_callback(name, counter)})
        return json.dumps({'result': name + '(' + str(counter) + ')'})

    def duplicate_node_config(self, callback):
        """This event is fired when a new node is created with the same name which already
        exist in tree. This callback should return a new name which shouldn't conflict
        with the existing node's name. By default, this callback will return the name in
        the following form: "NodeName(Counter)" for example, "NewNode(2)".

        The callback function will receive the following two parameters: name and counter
        and should return string as a new name for the node

        **NOTE**: This callback is the part of configuration and shouldn't be confused with
                    any event

            Args:
                callback (callable): A callable which accepts two params 'name' & 'counter'
        """
        self._unique_duplicate_callback = callback

    def _process_sort_callback(self):
        node1 = ""
        node2 = ""
        if request.args.__len__() > 0:
            node1 = request.args['node1']
            node2 = request.args['node2']
        if self._sort_callback is not None:
            return json.dumps({'result': self._sort_callback(node1, node2)})
        return json.dumps({'result': -1})  # The sort option should receive 1 or -1

    def sort_config(self, callback):
        """The sort event is fired when tree tries to sort its nodes in a particular direction.
        Callback will receive two parameters: "node1" & "node2" and should return -1 or 1 based
        on the comparision between these 2 nodes. By default, it will return -1

        **NOTE**: This callback is the part of configuration and shouldn't be confused with
                    any event

            Args:
                callback (callable): A callable which accepts two params 'node1' & 'node2'
        """
        self._sort_callback = callback

    def _process_search_ajax_callback(self):
        search_str = ""
        inside = ""
        if request.args.__len__() > 0:
            search_str = request.args['str']
            inside = request.args['inside']
        if self._search_ajax_callback is not None:
            return json.dumps(self._search_ajax_callback(search_str, inside))
        else:
            return json.dumps([])  # an empty JSON array

    def search_ajax_config(self, callback):
        """This callback will be used by JSTree to execute the search query at the server side.
        The callback will receive `str` parameter which is a search string or query and an optional
        parameter `inside` (i.e., node id) if search is limited to a node. The callback should
        return an JSON array of node id after executing the search logic on server. All these
        nodes in the array will be opened and revealed to user

            Args:
                callback (callable): A callable which accepts two params 'str' and 'inside'
        """
        self._search_ajax_callback = callback

    def add_node_type(self, key, n_type):
        """Adds a node type to JSTree's type collection

            Args:
                key (string): A key associated with new type to be added
                n_type (JSTreeNodeType): An inatance of the `JSTreeNodeType` class
        """
        self._types[key] = n_type

    def remove_node_type(self, key):
        """Removes an NodeType from the JSTree's type collection

            Args:
                key (string): A key related to type for deletion
        """
        self._types.pop(key)

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
        types = ""
        # ================= Render Node Types ======================== #
        if self._types is not None and self._types.__len__() > 0:
            types = "types: {\n"
            for n_type in self._types:
                types += self._types.get(n_type).render() + ",\n"
            types += "\n},"
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
                                    tie_selection: %s,
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
                                    },
                                    case_sensitive: %s,
                                    show_only_matches: %s,
                                    close_opened_onclear: %s,
                                },
                                sort: function(node1, node2){
                                    var sort_order = -1;
                                    $.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        async: false,
                                        timeout: 30000,
                                        dataType: 'json',
                                        data: {'node1': node1, 'node2': node2},
                                        success: function(data){
                                            sort_order = data.result;
                                        },
                                        error: function(status){
                                            sort_order = -1;
                                        }
                                    });
                                    return sort_order;
                                },
                                //Types will be rendered below with trailing comma
                                %s
                                unique: {
                                    case_sensitive: %s,
                                    trim_whitespace: %s,
                                    duplicate: function(name, counter){
                                        var name_str = "";
                                        $.ajax({
                                            url: '/%s',
                                            type: 'get',
                                            async: false,
                                            timeout: 30000,
                                            dataType: 'json',
                                            data: {'name': name, 'counter': counter},
                                            success: function(status){
                                                name_str = status.result;
                                            },
                                            error: function(err_status){
                                                name_str = name + '(' + counter + ')';
                                            }
                                        });
                                        if(name_str == ""){
                                            return name + '(' + counter + ')';
                                        } else {
                                            return name_str;
                                        }
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
                       json.dumps(self._checkbox_tie_selection
                                  if self._checkbox_tie_selection is not None else True),
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
                       self._search_ajax_url,
                       json.dumps(self._search_case_sensitive if self._search_case_sensitive is not None else False),
                       json.dumps(self._search_show_only_matches
                                  if self._search_show_only_matches is not None else False),
                       json.dumps(self._search_close_opened_onclear
                                  if self._search_close_opened_onclear is not None else False),
                       self._sort_url,
                       types,
                       json.dumps(self._unique_case_sensitive if self._unique_case_sensitive is not None else False),
                       json.dumps(self._unique_trim_whitespace if self._unique_trim_whitespace is not None else False),
                       self._unique_duplicate_url
                       )
        return script

    def _register_url(self, url, callback):
        if self._app is not None:
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + url, url, callback)

    def _prepare_callback_urls(self):
        self._loaded_url = str(__name__ + "_" + self._name + "_loaded").replace('.', '_')
        self._register_url(self._loaded_url, self._process_loaded_callback)
        #
        self._ready_url = str(__name__ + "_" + self._name + "_loaded").replace('.', '_')
        self._register_url(self._ready_url, self._process_loaded_callback)
        #
        self._load_node_url = str(__name__ + "_" + self._name + "_load_node").replace('.', '_')
        self._register_url(self._load_node_url, self._process_load_node_callback)
        #
        self._model_url = str(__name__ + "_" + self._name + "_model").replace('.', '_')
        self._register_url(self._model_url, self._process_model_callback)
        #
        self._redraw_url = str(__name__ + "_" + self._name + "_redraw").replace('.', '_')
        self._register_url(self._redraw_url, self._process_redraw_callback)
        #
        self._before_open_url = str(__name__ + "_" + self._name + "_before_open").replace('.', '_')
        self._register_url(self._before_open_url, self._process_before_open_callback)
        #
        self._open_node_url = str(__name__ + "_" + self._name + "_open_node").replace('.', '_')
        self._register_url(self._open_node_url, self._process_open_node_callback)
        #
        self._after_open_url = str(__name__ + "_" + self._name + "_after_open").replace('.', '_')
        self._register_url(self._after_open_url, self._process_after_open_callback)
        #
        self._close_node_url = str(__name__ + "_" + self._name + "_close_node").replace('.', '_')
        self._register_url(self._close_node_url, self._process_close_node_callback)
        #
        self._after_close_url = str(__name__ + "_" + self._name + "_after_close").replace('.', '_')
        self._register_url(self._after_close_url, self._process_after_close_callback)
        #
        self._activate_node_url = str(__name__ + "_" + self._name + "_activate_node").replace('.', '_')
        self._register_url(self._activate_node_url, self._process_activate_node_callback)
        #
        self._hover_node_url = str(__name__ + "_" + self._name + "_hover_node").replace('.', '_')
        self._register_url(self._hover_node_url, self._process_hover_node_callback)
        #
        self._dehover_node_url = str(__name__ + "_" + self._name + "_dehover_node").replace('.', '_')
        self._register_url(self._dehover_node_url, self._process_dehover_node_callback)
        #
        self._select_node_url = str(__name__ + "_" + self._name + "_select_node").replace('.', '_')
        self._register_url(self._select_node_url, self._process_select_node_callback)
        #
        self._changed_url = str(__name__ + "_" + self._name + "_changed").replace('.', '_')
        self._register_url(self._changed_url, self._process_changed_callback)
        #
        self._set_text_url = str(__name__ + "_" + self._name + "_set_text").replace('.', '_')
        self._register_url(self._set_text_url, self._process_set_text_callback)
        #
        self._create_node_url = str(__name__ + "_" + self._name + "_create_node").replace('.', '_')
        self._register_url(self._create_node_url, self._process_create_node_callback)
        #
        self._rename_node_url = str(__name__ + "_" + self._name + "_rename_node").replace('.', '_')
        self._register_url(self._rename_node_url, self._process_rename_node_callback)
        #
        self._delete_node_url = str(__name__ + "_" + self._name + "_delete_node").replace('.', '_')
        self._register_url(self._delete_node_url, self._process_delete_node_callback)
        #
        self._move_node_url = str(__name__ + "_" + self._name + "_move_node").replace('.', '_')
        self._register_url(self._move_node_url, self._process_move_node_callback)
        #
        self._copy_node_url = str(__name__ + "_" + self._name + "_copy_node").replace('.', '_')
        self._register_url(self._copy_node_url, self._process_copy_node_callback)
        #
        self._copy_url = str(__name__ + "_" + self._name + "_copy").replace('.', '_')
        self._register_url(self._copy_url, self._process_copy_callback)
        #
        self._cut_url = str(__name__ + "_" + self._name + "_cut").replace('.', '_')
        self._register_url(self._cut_url, self._process_cut_callback)
        #
        self._paste_url = str(__name__ + "_" + self._name + "_paste").replace('.', '_')
        self._register_url(self._paste_url, self._process_paste_callback)
        #
        self._check_node_url = str(__name__ + "_" + self._name + "_check_node").replace('.', '_')
        self._register_url(self._check_node_url, self._process_check_node_callback)
        #
        self._uncheck_node_url = str(__name__ + "_" + self._name + "_uncheck_node").replace('.', '_')
        self._register_url(self._uncheck_node_url, self._process_uncheck_node_callback)
        #
        self._show_contextmenu_url = str(__name__ + "_" + self._name + "_show_contextmenu").replace('.', '_')
        self._register_url(self._show_contextmenu_url, self._process_show_contextmenu_callback)
        #
        self._search_url = str(__name__ + "_" + self._name + "_search_url").replace('.', '_')
        self._register_url(self._search_url, self._process_search_callback)
        #
        self._clear_search_url = str(__name__ + "_" + self._name + "_clear_search").replace('.', '_')
        self._register_url(self._clear_search_url, self._process_clear_search_callback)

    def on_loaded_event(self, callback):
        self._loaded_callback = callback

    def _process_loaded_callback(self):
        if self._loaded_callback is not None:
            return json.dumps({'result': self._loaded_callback()})
        return json.dumps({'result': ''})

    def on_ready_event(self, callback):
        self._ready_callback = callback

    def _process_ready_callback(self):
        if self._ready_callback is not None:
            return json.dumps({'result': self._ready_callback()})
        return json.dumps({'result': ''})

    def on_load_node_event(self, callback):
        self._load_node_callback = callback

    def _process_load_node_callback(self):
        if self._load_node_callback is not None:
            return json.dumps({'result': self._load_node_callback()})
        return json.dumps({'result': ''})

    def on_model_event(self, callback):
        self._model_callback = callback

    def _process_model_callback(self):
        if self._model_callback is not None:
            return json.dumps({'result': self._model_callback()})
        return json.dumps({'result': ''})

    def on_redraw_event(self, callback):
        self._redraw_callback = callback

    def _process_redraw_callback(self):
        if self._redraw_callback is not None:
            return json.dumps({'result': self._redraw_callback()})
        return json.dumps({'result': ''})

    def on_before_open_event(self, callback):
        self._before_open_callback = callback

    def _process_before_open_callback(self):
        if self._before_open_callback is not None:
            return json.dumps({'result': self._before_open_callback()})
        return json.dumps({'result': ''})

    def on_open_node_event(self, callback):
        self._open_node_callback = callback

    def _process_open_node_callback(self):
        if self._open_node_callback is not None:
            return json.dumps({'result': self._open_node_callback()})
        return json.dumps({'result': ''})

    def on_after_open_event(self, callback):
        self._after_open_callback = callback

    def _process_after_open_callback(self):
        if self._after_open_callback is not None:
            return json.dumps({'result': self._after_open_callback()})
        return json.dumps({'result': ''})

    def on_close_node_event(self, callback):
        self._close_node_callback = callback

    def _process_close_node_callback(self):
        if self._close_node_callback is not None:
            return json.dumps({'result': self._close_node_callback()})
        return json.dumps({'result': ''})

    def on_after_close_event(self, callback):
        self._after_close_callback = callback

    def _process_after_close_callback(self):
        if self._after_close_callback is not None:
            return json.dumps({'result': self._after_close_callback()})
        return json.dumps({'result': ''})

    def on_activate_node_event(self, callback):
        self._activate_node_callback = callback

    def _process_activate_node_callback(self):
        if self._activate_node_callback is not None:
            return json.dumps({'result': self._activate_node_callback()})
        return json.dumps({'result': ''})

    def on_hover_node_event(self, callback):
        self._hover_node_callback = callback

    def _process_hover_node_callback(self):
        if self._hover_node_callback is not None:
            return json.dumps({'result': self._hover_node_callback()})
        return json.dumps({'result': ''})

    def on_dehover_node_event(self, callback):
        self._dehover_node_callback = callback

    def _process_dehover_node_callback(self):
        if self._dehover_node_callback is not None:
            return json.dumps({'result': self._dehover_node_callback()})
        return json.dumps({'result': ''})

    def on_select_node_event(self, callback):
        self._select_node_callback = callback

    def _process_select_node_callback(self):
        if self._select_node_callback is not None:
            return json.dumps({'result': self._select_node_callback()})
        return json.dumps({'result': ''})

    def on_changed_event(self, callback):
        self._changed_callback = callback

    def _process_changed_callback(self):
        if self._changed_callback is not None:
            return json.dumps({'result': self._changed_callback()})
        return json.dumps({'result': ''})

    def on_set_text_callback(self, callback):
        self._set_text_callback = callback

    def _process_set_text_callback(self):
        if self._set_text_callback is not None:
            return json.dumps({'result': self._set_text_callback()})
        return json.dumps({'result': ''})

    def on_create_node_callback(self, callback):
        self._create_node_callback = callback

    def _process_create_node_callback(self):
        if self._create_node_callback is not None:
            return json.dumps({'result': self._create_node_callback()})
        return json.dumps({'result': ''})

    def on_rename_node_callback(self, callback):
        self._rename_node_callback = callback

    def _process_rename_node_callback(self):
        if self._rename_node_callback is not None:
            return json.dumps({'result': self._rename_node_callback()})
        return json.dumps({'result': ''})

    def on_delete_node_callback(self, callback):
        self._delete_node_callback = callback

    def _process_delete_node_callback(self):
        if self._delete_node_callback is not None:
            return json.dumps({'result': self._delete_node_callback()})
        return json.dumps({'result': ''})

    def on_move_node_callback(self, callback):
        self._move_node_callback = callback

    def _process_move_node_callback(self):
        if self._move_node_callback is not None:
            return json.dumps({'result': self._move_node_callback()})
        return json.dumps({'result': ''})

    def on_copy_node_callback(self, callback):
        self._copy_node_callback = callback

    def _process_copy_node_callback(self):
        if self._copy_node_callback is not None:
            return json.dumps({'result': self._copy_node_callback()})
        return json.dumps({'result': ''})

    def on_copy_callback(self, callback):
        self._copy_callback = callback

    def _process_copy_callback(self):
        if self._copy_callback is not None:
            return json.dumps({'result': self._copy_callback()})
        return json.dumps({'result': ''})

    def on_cut_callback(self, callback):
        self._cut_callback = callback

    def _process_cut_callback(self):
        if self._cut_callback is not None:
            return json.dumps({'result': self._cut_callback()})
        return json.dumps({'result': ''})

    def on_paste_callback(self, callback):
        self._paste_callback = callback

    def _process_paste_callback(self):
        if self._paste_callback is not None:
            return json.dumps({'result': self._paste_callback()})
        return json.dumps({'result': ''})

    def on_check_node_callback(self, callback):
        self._check_node_callback = callback

    def _process_check_node_callback(self):
        if self._check_node_callback is not None:
            return json.dumps({'result': self._check_node_callback()})
        return json.dumps({'result': ''})

    def on_uncheck_node_callback(self, callback):
        self._uncheck_node_callback = callback

    def _process_uncheck_node_callback(self):
        if self._uncheck_node_callback is not None:
            return json.dumps({'result': self._uncheck_node_callback()})
        return json.dumps({'result': ''})

    def on_show_contextmenu_callback(self, callback):
        self._show_contextmenu_callback = callback

    def _process_show_contextmenu_callback(self):
        if self._show_contextmenu_callback is not None:
            return json.dumps({'result': self._show_contextmenu_callback()})
        return json.dumps({'result': ''})

    def on_search_callback(self, callback):
        self._search_callback = callback

    def _process_search_callback(self):
        if self._search_callback is not None:
            return json.dumps({'result': self._search_callback()})
        return json.dumps({'result': ''})

    def on_clear_search_callback(self, callback):
        self._clear_search_callback = callback

    def _process_clear_search_callback(self):
        if self._clear_search_callback is not None:
            return json.dumps({'result': self._clear_search_callback()})
        return json.dumps({'result': ''})

    def _attach_event_handlers(self):       # noqa
        handlers = ""
        handlers += """<script>
                        $(function(){
                            var selector = $('#%s');\n
                    """ % (self._name)
        if self._loaded_callback is not None:
            handlers += """
                            selector.on('loaded.jstree', function(e, data){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._loaded_url)
        if self._ready_callback is not None:
            handlers += """
                            selector.on('ready.jstree', function(e, data){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._ready_url)
        if self._load_node_callback is not None:
            handlers += """
                            selector.on('load_node.jstree', function(node, status){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._load_node_url)
        if self._model_callback is not None:
            handlers += """
                            selector.on('model.jstree', function(nodes, parent){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._model_url)
        if self._redraw_callback is not None:
            handlers += """
                            selector.on('redraw.jstree', function(nodes){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._redraw_url)
        if self._before_open_callback is not None:
            handlers += """
                            selector.on('before_open.jstree', function(node){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._before_open_url)
        if self._open_node_callback is not None:
            handlers += """
                            selector.on('open_node.jstree', function(node){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._open_node_url)
        if self._after_open_callback is not None:
            handlers += """
                            selector.on('after_open.jstree', function(node){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._after_open_url)
        if self._close_node_callback is not None:
            handlers += """
                            selector.on('close_node.jstree', function(node){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._close_node_url)
        if self._after_close_callback is not None:
            handlers += """
                            selector.on('after_close.jstree', function(node){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._after_close_url)
        if self._activate_node_callback is not None:
            handlers += """
                            selector.on('activate_node.jstree', function(node, event){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._activate_node_url)
        if self._hover_node_callback is not None:
            handlers += """
                            selector.on('hover_node.jstree', function(node){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._hover_node_callback)
        if self._dehover_node_callback is not None:
            handlers += """
                            selector.on('dehover_node.jstree', function(node){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._dehover_node_url)
        if self._select_node_callback is not None:
            handlers += """
                            selector.on('select_node.jstree', function(node, selected, event){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._select_node_url)
        if self._changed_callback is not None:
            handlers += """
                            selector.on('changed.jstree', function(node, action, selected. event){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._changed_url)
        if self._set_text_callback is not None:
            handlers += """
                            selector.on('set_text.jstree', function(e, data){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._set_text_url)
        if self._create_node_callback is not None:
            handlers += """
                            selector.on('create_node.jstree', function(node, parent, position){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._create_node_url)
        if self._rename_node_callback is not None:
            handlers += """
                            selector.on('rename_node.jstree', function(node, text, old){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._rename_node_url)
        if self._delete_node_callback is not None:
            handlers += """
                            selector.on('delete_node.jstree', function(node, parent){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._delete_node_url)
        if self._move_node_callback is not None:
            handlers += """
                            selector.on('move_node.jstree', function(node, parent, position, old_parent, old_position, is_multi, old_instance, new_instance){           //# noqa
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._move_node_url)
        if self._copy_node_callback is not None:
            handlers += """
                            selector.on('copy_node.jstree', function(node, parent, position, old_parent, old_position, is_multi, old_instance, new_instance){           //# noqa
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._copy_node_url)
        if self._copy_callback is not None:
            handlers += """
                            selector.on('copy.jstree', function(nodes){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._copy_url)
        if self._cut_callback is not None:
            handlers += """
                            selector.on('cut.jstree', function(nodes){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._cut_url)
        if self._paste_callback is not None:
            handlers += """
                            selector.on('paste.jstree', function(parent, node, mode){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._paste_url)
        if self._check_node_callback is not None:
            handlers += """
                            selector.on('check_node.jstree', function(node, selected, event){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._check_node_url)
        if self._uncheck_node_callback is not None:
            handlers += """
                            selector.on('uncheck_node.jstree', function(node, selected, event){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._uncheck_node_url)
        if self._show_contextmenu_callback is not None:
            handlers += """
                            selector.on('show_contextmenu.jstree', function(node, x, y){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._show_contextmenu_url)
        if self._search_callback is not None:
            handlers += """
                            selector.on('search.jstree', function(nodes, str, res){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._search_url)
        if self._clear_search_callback is not None:
            handlers += """
                            selector.on('clear_search.jstree', function(nodes, str, res){
                                $.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            });\n
                        """ % (self._clear_search_url)
        handlers += """
                    })();
                    </script>
                    """
        return handlers

    def _command_processor(self):
        if self._cmd_queue is not None and self._cmd_queue.__len__() > 0:
            cmd = self._cmd_queue.pop()
            if cmd is not None:
                return json.dumps(cmd)
        return json.dumps({'cmd': 'NONE'})

    def destroy(self):
        """Destroy all the resources used by JSTree at client side"""
        self._cmd_queue.append({'cmd': 'DESTROY'})

    def redraw(self):
        self._cmd_queue.append({'cmd': 'REDRAW'})

    def open_node(self, node):
        self._cmd_queue.append({'cmd': 'OPEN-NODE', 'arg0': node})

    def close_node(self, node):
        self._cmd_queue.append({'cmd': 'CLOSE-NODE', 'arg0': node})

    def toggle_node(self, node):
        self._cmd_queue.append({'cmd': 'TOGGLE-NODE', 'arg0': node})

    def open_all(self):
        self._cmd_queue.append({'cmd': 'OPEN-ALL'})

    def close_all(self):
        self._cmd_queue.append({'cmd': 'CLOSE-ALL'})

    def enable_node(self, node):
        self._cmd_queue.append({'cmd': 'ENABLE-NODE', 'arg0': node})

    def disable_node(self, node):
        self._cmd_queue.append({'cmd': 'DISABLE-NODE', 'arg0': node})

    def hide_node(self, node):
        self._cmd_queue.append({'cmd': 'HIDE-NODE', 'arg0': node})

    def show_node(self, node):
        self._cmd_queue.append({'cmd': 'SHOW-NODE', 'arg0': node})

    def hide_all(self):
        self._cmd_queue.append({'cmd': 'HIDE-ALL'})

    def show_all(self):
        self._cmd_queue.append({'cmd': 'SHOW-ALL'})

    def select_node(self, node, supress_event=False):
        self._cmd_queue.append({'cmd': 'SELECT-NODE', 'arg0': node, 'arg1': supress_event})

    def deselect_node(self, node, supress_event=False):
        self._cmd_queue.append({'cmd': 'DESELECT-NODE', 'arg0': node, 'arg1': supress_event})

    def select_all(self, supress_event=False):
        self._cmd_queue.append({'cmd': 'SELECT-ALL', 'arg0': supress_event})

    def deselect_all(self, supress_event=False):
        self._cmd_queue.append({'cmd': 'DESELECT-ALL', 'arg0': supress_event})

    def refresh(self):
        self._cmd_queue.append({'cmd': 'REFRESH'})

    def refresh_node(self, node):
        self._cmd_queue.append({'cmd': 'REFRESH-NODE', 'arg0': node})

    def set_id(self, node, id):
        self._cmd_queue.append({'cmd': 'SET-ID', 'arg0': node, 'arg1': id})

    def create_node(self, parent=None, data=None, index=None):
        if parent is not None and index is not None and data is not None:
            self._cmd_queue.append({'cmd': 'CREATE-NODE', 'arg0': parent, 'arg1': data, 'arg2': index})
        elif parent is not None and data is not None and index is None:
            self._cmd_queue.append({'cmd': 'CREATE-NODE', 'arg0': parent, 'arg1': data})
        elif parent is not None and index is None and data is None:
            self._cmd_queue.append({'cmd': 'CREATE-NODE', 'arg0': parent})
        else:
            self._cmd_queue.append({'cmd': 'CREATE-NODE'})

    def rename_node(self, node, name):
        self._cmd_queue.append({'cmd': 'RENAME-NODE', 'arg0': node, 'arg1': name})

    def delete_node(self, node):
        self._cmd_queue.append({'cmd': 'DELETE-NODE', 'arg0': node})

    def move_node(self, node, parent):
        self._cmd_queue.append({'cmd': 'MOVE-NODE', 'arg0': node, 'arg1': parent})

    def copy_node(self, node, parent):
        self._cmd_queue.append({'cmd': 'COPY-NODE', 'arg0': node, 'arg1': parent})

    def cut(self, nodes):
        self._cmd_queue.append({'cmd': 'CUT', 'arg0': nodes})

    def copy(self, nodes):
        self._cmd_queue.append({'cmd': 'COPY', 'arg0': nodes})

    def paste(self, parent):
        self._cmd_queue.append({'cmd': 'PASTE', 'arg0': parent})

    def clear_buffer(self):
        self._cmd_queue.append({'cmd': 'CLEAR-BUFFER'})

    def edit(self, node):
        self._cmd_queue.append({'cmd': 'EDIT', 'arg0': node})

    def show_stripes(self):
        self._cmd_queue.append({'cmd': 'SHOW-STRIPES'})

    def hide_stripes(self):
        self._cmd_queue.append({'cmd': 'HIDE-STRIPES'})

    def toggle_stripes(self):
        self._cmd_queue.append({'cmd': 'TOGGLE-STRIPES'})

    def show_dots(self):
        self._cmd_queue.append({'cmd': 'SHOW-DOTS'})

    def hide_dots(self):
        self._cmd_queue.append({'cmd': 'HIDE-DOTS'})

    def toggle_dots(self):
        self._cmd_queue.append({'cmd': 'TOGGLE-DOTS'})

    def show_icons(self):
        self._cmd_queue.append({'cmd': 'SHOW-ICONS'})

    def hide_icons(self):
        self._cmd_queue.append({'cmd': 'HIDE-ICONS'})

    def toggle_icons(self):
        self._cmd_queue.append({'cmd': 'TOGGLE-ICONS'})

    def show_ellipses(self):
        self._cmd_queue.append({'cmd': 'SHOW-ELLIPSES'})

    def hide_ellipses(self):
        self._cmd_queue.append({'cmd': 'HIDE-ELLIPSES'})

    def toggle_ellipses(self):
        self._cmd_queue.append({'cmd': 'TOGGLE-ELLIPSES'})

    def show_checkboxes(self):
        self._cmd_queue.append({'cmd': 'SHOW-CHECKBOXES'})

    def hide_checkboxes(self):
        self._cmd_queue.append({'cmd': 'HIDE-CHECKBOXES'})

    def toggle_checkboxes(self):
        self._cmd_queue.append({'cmd': 'TOGGLE-CHECKBOXES'})

    def disable_checkbox(self, nodes):
        self._cmd_queue.append({'cmd': 'DISABLE-CHECKBOX', 'arg0': nodes})

    def enable_checkbox(self, nodes):
        self._cmd_queue.append({'cmd': 'ENABLE-CHECKBOX', 'arg0': nodes})

    def check_node(self, nodes):
        self._cmd_queue.append({'cmd': 'CHECK-NODE', 'arg0': nodes})

    def uncheck_node(self, nodes):
        self._cmd_queue.append({'cmd': 'UNCHECK-NODE', 'arg0': nodes})

    def check_all(self):
        self._cmd_queue.append({'cmd': 'CHECK-ALL'})

    def uncheck_all(self):
        self._cmd_queue.append({'cmd': 'UNCHECK-ALL'})

    def show_contextmenu(self):
        self._cmd_queue.append({'cmd': 'SHOW-CONTEXTMENU'})

    def search(self, query, search_on_client):
        self._cmd_queue.append({'cmd': 'SEARCH', 'arg0': query, 'arg1': search_on_client})

    def clear_search(self):
        self._cmd_queue.append({'cmd': 'CLEAR-SEARCH'})

    def save_state(self):
        self._cmd_queue.append({'cmd': 'SAVE-STATE'})

    def restore_state(self):
        self._cmd_queue.append({'cmd': 'RESTORE-STATE'})

    def clear_state(self):
        self._cmd_queue.append({'cmd': 'CLEAR-STATE'})

    def _attach_polling(self):
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        if self._app is not None:
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + url, url, self._command_processor)
        script = """
                <script>
                    (function %s_poll(){
                        setTimeout(function(){
                            $.ajax({
                                url: '/%s',
                                type: 'get',
                                dataType: 'json',
                                success: function(props){
                                    selector = $.jstree.reference('#%s');
                                    if(selector != undefined){
                                        if(props.cmd != undefined){
                                            switch(props.cmd){
                                                case 'DESTROY':
                                                    selector.destroy();
                                                    break;
                                                case 'REDRAW':
                                                    selector.redraw(props.arg0);
                                                    break;
                                                 case 'OPEN-NODE':
                                                    selector.open_node(props.arg0);
                                                    break;
                                                case 'CLOSE-NODE':
                                                    selector.close_node(props.arg0);
                                                    break;
                                                case 'TOGGLE-NODE':
                                                    selector.toggle_node(props.arg0);
                                                    break;
                                                case 'OPEN-ALL':
                                                    selector.open_all();
                                                    break;
                                                case 'CLOSE-ALL':
                                                    selector.close_all();
                                                    break;
                                                case 'ENABLE-NODE':
                                                    selector.enable_node(props.arg0);
                                                    break;
                                                case 'DISABLE-NODE':
                                                    selector.disable_node(props.arg0);
                                                    break;
                                                case 'HIDE-NODE':
                                                    selector.hide_node(props.arg0);
                                                    break;
                                                case 'SHOW-NODE':
                                                    selector.show_node(props.arg0);
                                                    break;
                                                case 'HIDE-ALL':
                                                    selector.hide_all();
                                                    break;
                                                case 'SHOW-ALL':
                                                    selector.show_all();
                                                    break;
                                                case 'SELECT-NODE':
                                                    if(props.arg1 != undefined){
                                                        selector.select_node(props.arg0, props.arg1);
                                                    } else {
                                                        selector.select_node(props.arg0);
                                                    }
                                                    break;
                                                case 'DESELECT-NODE':
                                                    if(props.arg1 != undefined){
                                                        selector.deselect_node(props.arg0, props.arg1);
                                                    } else {
                                                        selector.deselect_node(props.arg0);
                                                    }
                                                    break;
                                                case 'SELECT-ALL':
                                                    selector.select_all(props.arg0);
                                                    break;
                                                case 'DESELECT-ALL':
                                                    selector.deselect_all(props.arg0);
                                                    break;
                                                case 'REFRESH':
                                                    selector.refresh();
                                                    break;
                                                case 'REFRESH-NODE':
                                                    selector.refresh_node(props.arg0);
                                                    break;
                                                case 'SET-ID':
                                                    selector.set_id(props.arg0, props.arg1);
                                                    break;
                                                case 'CREATE-NODE':
                                                    if(props.arg2 != undefined && props.arg1 != undefined && props.arg0 != undefined) //# noqa
                                                    {
                                                        selector.create_node(props.arg0, props.arg1, props.arg2);
                                                    } else if(props.arg1 != undefined && props.arg0 != undefined)
                                                    {
                                                        selector.create_node(props.arg0, props.arg1);
                                                    } else if (props.arg0 != undefined)
                                                    {
                                                        selector.create_node(props.arg0);
                                                    } else {
                                                        selector.create_node();
                                                    }
                                                    break;
                                                case 'RENAME-NODE':
                                                    selector.rename_node(props.arg0, props.arg1);
                                                    break;
                                                case 'DELETE-NODE':
                                                    selector.delete_node(props.arg0);
                                                    break;
                                                case 'MOVE-NODE':
                                                    selector.move_node(props.arg0, props.arg1);
                                                    break;
                                                case 'COPY-NODE':
                                                    selector.copy_node(props.arg0, props.arg1);
                                                    break;
                                                case 'CUT':
                                                    selector.cut(props.arg0);
                                                    break;
                                                case 'COPY':
                                                    selector.copy(props.arg0);
                                                    break;
                                                case 'PASTE':
                                                    selector.paste(props.arg0);
                                                    break;
                                                case 'CLEAR-BUFFER':
                                                    selector.clear_buffer();
                                                    break;
                                                case 'EDIT':
                                                    selector.edit(props.arg0);
                                                    break;
                                                case 'SHOW-STRIPES':
                                                    selector.show_stripes();
                                                    break;
                                                case 'HIDE-STRIPES':
                                                    selector.hide_stripes();
                                                    break;
                                                case 'TOGGLE-STRIPES':
                                                    selector.toggle_stripes();
                                                    break;
                                                case 'SHOW-DOTS':
                                                    selector.show_dots();
                                                    break;
                                                case 'HIDE-DOTS':
                                                    selector.hide_dots();
                                                    break;
                                                case 'TOGGLE-DOTS':
                                                    selector.toggle_dots();
                                                    break;
                                                case 'SHOW-ICONS':
                                                    selector.show_icons();
                                                    break;
                                                case 'HIDE-ICONS':
                                                    selector.hide_icons();
                                                    break;
                                                case 'TOGGLE-ICONS':
                                                    selector.toggle_icons();
                                                    break;
                                                case 'SHOW-ELLIPSIS':
                                                    selector.show_ellipsis();
                                                    break;
                                                case 'HIDE-ELLIPSIS':
                                                    selector.hide_ellipsis();
                                                    break;
                                                case 'TOGGLE-ELLIPSIS':
                                                    selector.toggle_ellipsis();
                                                    break;
                                                case 'SHOW-CHECKBOXES':
                                                    selector.show_checkboxes();
                                                    break;
                                                case 'HIDE-CHECKBOXES':
                                                    selector.hide_checkboxes();
                                                    break;
                                                case 'TOGGLE-CHECKBOXES':
                                                    selector.toggle_checkboxes()
                                                    break;
                                                case 'DISABLE-CHECKBOX':
                                                    selector.disable_checkbox(props.arg0);
                                                    break;
                                                case 'ENABLE-CHECKBOX':
                                                    selector.enable_checkbox(props.arg0);
                                                    break;
                                                case 'CHECK-NODE':
                                                    selector.check_node(props.arg0);
                                                    break;
                                                case 'UNCHECK-NODE':
                                                    selector.uncheck_node(props.arg0);
                                                    break;
                                                case 'CHECK-ALL':
                                                    selector.check_all();
                                                    break;
                                                case 'UNCHECK-ALL':
                                                    selector.uncheck_all();
                                                    break;
                                                case 'SHOW-CONTEXTMENU':
                                                    selector.show_contextmenu();
                                                    break;
                                                case 'SEARCH':
                                                    if(props.arg1 != undfined){
                                                        selector.search(props.arg0, props.arg1);
                                                    } else
                                                    {
                                                        selector.search(props.arg0);
                                                    }
                                                    break;
                                                case 'CLEAR-SEARCH':
                                                    selector.clear_search();
                                                    break;
                                                case 'SAVE-STATE':
                                                    selector.save_state();
                                                    break;
                                                case 'RESTORE-STATE':
                                                    selector.restore_state();
                                                    break;
                                                case 'CLEAR-STATE':
                                                    selector.clear_state();
                                                    break;
                                            }
                                        }
                                    }
                                },
                                error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                }
                            });
                            %s_poll();
                        }, 10000);
                    })();
                </script>
                """ % (url, url, self._name, url)
        return script

    def render(self):
        self._prepare_callback_urls()
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += self._attach_script() + "\n" + self._attach_event_handlers()\
            + "\n" + self._attach_polling()
        return content
