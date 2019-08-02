"""
This module contains the API's to create app for mobile using
JQuery Mobile framework

Author: Ajeet Singh
Date: 07/30/2019
"""
from flask_socketio import Namespace, emit
from widgets4py.base import Widget
from enum import Enum


class MPage(Widget):
    """The mobile will will act as parent widget to hold all
    other widgets for mobile
    """

    _title = None
    _header_widgets = None
    _footer_widgets = None
    _socketio = None
    _footer_title = None
    _before_render_callback = None
    _after_render_callback = None

    def __init__(self, name, title, socketio, header_widgets=None, footer_widgets=None,
                 child_widgets=None, footer_title=None, before_render_callback=None,
                 after_render_callback=None):
        Widget.__init__(self, name)
        self._title = title
        self._socketio = socketio
        if header_widgets is not None:
            self._header_widgets = header_widgets
        else:
            self._header_widgets = []
        if child_widgets is not None:
            self._child_widgets = child_widgets
        else:
            self._child_widgets = []
        if footer_widgets is not None:
            self._footer_widgets = footer_widgets
        else:
            self._footer_widgets = []
        self._footer_title = footer_title
        self._before_render_callback = before_render_callback
        self._after_render_callback = after_render_callback

    def render(self):
        """Render the contents of mobile page in browser"""
        if self._before_render_callback is not None:
            self._before_render_callback(self._name, {'title': self._title,
                                                      'footer_title': self._footer_title})
        header_content = ""
        if self._header_widgets is not None:
            for hwidget in self._header_widgets:
                header_content += hwidget.render()
        footer_content = ""
        if self._footer_widgets is not None:
            for fwidget in self._footer_widgets:
                footer_content += fwidget.render()
        child_content = ""
        if self._child_widgets is not None:
            for cwidget in self._child_widgets:
                child_content += cwidget.render()
        content = """
                    <div data-role="page" id='%s'>
                        <div data-role="header">
                            <h1>%s</h1>
                            %s
                         </div><!-- /header -->

                         <div role="main" class="ui-content">
                            %s
                         </div><!-- /content -->

                         <div data-role="footer">
                            <h4>%s</h4>
                            %s
                         </div><!-- /footer -->
                    </div><!-- /page -->
                """ % (self._name, self._title, header_content, child_content,
                       self._footer_title, footer_content)
        if self._after_render_callback is not None:
            self._after_render_callback(self._name, {'title': self._title,
                                                     'footer_title': self._footer_title})
        return content


class ButtonStyle(str, Enum):
    """Types of button supported by the framework"""
    ROUND_CORNERS = 'ui-corner-all'
    SHADOW = 'ui-shadow'
    INLINE = 'ui-btn-inline'
    THEME_A = 'ui-btn-a'
    THEME_B = 'ui-btn-b'
    MINI = 'ui-mini'
    ICON_LEFT = 'ui-btn-icon-left'
    ICON_RIGHT = 'ui-btn-icon-right'
    ICON_TOP = 'ui-btn-icon-top'
    ICON_BOTTOM = 'ui-btn-icon-bottom'
    ICON_NOTEXT = 'ui-btn-icon-notext'
    ICON_SHADOW = 'ui-shadow-icon'
    DISABLED = 'ui-state-disabled'


class Button(Widget, Namespace):
    """Button class to create buttons using <a> tag or <button> tag.
    """

    UI_BTN_CLASS = 'ui-btn'
    ROUND_CORNER_NOTEXT_STYLE = """<style>
                                    #%s-border-radius .ui-btn-icon-notext.ui-corner-all{
                                        -webkit-border-radius: .3125em;
                                        border-radius: .3125em;
                                    }
                                    </style>
                                    """
    _title = None
    _icon = None
    _full_round = None
    _tag_type = None
    _btn_styles = None
    _socket_io = None
    _namespace = None
    _click_callback = None

    def __init__(self, name, socket_io, title=None, icon=None, full_round=None, tag_type=None,
                 btn_styles=None, click_callback=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_mbtn").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_mbtn").replace('.', '_')
        self._socket_io = socket_io
        self._title = title
        self._icon = icon
        if full_round is not None:
            self._full_round = full_round
        else:
            self._full_round = False
        if tag_type is not None:
            self._tag_type = tag_type
        else:
            self._tag_type = 'A'
        if btn_styles is not None:
            self._btn_styles = btn_styles
        else:
            self._btn_styles = []
        if title is None and icon is not None:
            found = False
            for st in self._btn_styles:
                if st == ButtonStyle.ICON_NOTEXT:
                    found = True
            if not found:
                self._btn_styles.append(ButtonStyle.ICON_NOTEXT)
        self._socket_io.on_namespace(self)
        self._click_callback = click_callback

    @property
    def namespace(self):
        """Namespace to be used by websockets"""
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def title(self):
        """Title to be shown on the button"""
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties()

    @property
    def icon(self):
        """CSS icon class to show icon on button"""
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val
        self._sync_properties()

    @property
    def is_full_round(self):
        """Returns whether the button should be fully round or not"""
        return self._full_round

    @is_full_round.setter
    def is_full_round(self, val):
        self._full_round = val

    @property
    def tag_type(self):
        """The HTML tag type (a or button) to render the button"""
        return self._tag_type

    @tag_type.setter
    def tag_type(self, val):
        self._tag_type = val

    @property
    def btn_styles(self):
        """A list of the styles applied to button"""
        return self._btn_styles

    @btn_styles.setter
    def btn_styles(self, val):
        self._btn_styles = val
        self._sync_properties()

    def _sync_properties(self):
        emit('sync_properties_' + self._name, {'title': self._title,
                                               'icon': self._icon,
                                               'styles': self._btn_styles},
             namespace=self._namespace)

    def add_style(self, style):
        """Add a new style from ButtonStyle class to the buttons style

            Args:
                style (ButtonStyle): An member of `ButtonStyle` class
        """
        self._btn_styles.append(style)
        self._sync_properties()

    def remove_style(self, style):
        """Removes an style from the button's style list

            Args:
                style (ButtonStyle): The style that needs to be removed
        """
        self._btn_styles.remove(style)
        self._sync_properties()

    def on_fire_click_event(self, props):
        """For internal use only"""
        title = props['title']
        if title is not None:
            self._title = title
        if props.__len__() >= 2:
            icon = props['icon']
            if icon is not None:
                self._icon = icon
        try:
            if self._click_callback is not None:
                self._click_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            msg = 'Method failed during callback execution: ' + str(e)
            emit('error', {'status': False, 'message': msg})

    def _attach_script(self):
        script = """
                    <script>
                    $(document).ready(function(){
                        var socket = io('%s');
                        var selector = $('#%s');
                        var icon = '';
                        selector.click(function(){
                            var title = selector.text();
                            var classes = selector.attr('class').split(' ');
                            for(let cs of classes){
                                var index = cs.indexOf('ui-icon');
                                if(index >= 0){
                                    icon = cs;
                                }
                            }
                            if(icon != ''){
                                socket.emit('fire_click_event', {'title': title,
                                                             'icon': icon});
                            } else {
                                socket.emit('fire_click_event', {'title': title});
                            }
                        });

                        socket.on('failed', function(data){
                            alertify.error('Failure: ' + data['message']);
                        });

                        socket.on('warning', function(data){
                            alertify.warning('Incomplete execution: ' + data['message']);
                        });

                        socket.on('success', function(data){
                            alertify.success('Call success acknowledged!');
                        });

                        socket.on('connect', function(){
                        });

                        socket.on('sync_properties_%s', function(props){
                            selector.text(props['title']);
                            var icon = props['icon'];
                            var styles = props['styles'];
                            //remove existing first
                            if(icon != undefined && icon != ''){
                                var classes = selector.attr('class').split(' ');
                                for(let cs of classes){
                                    var index = cs.indexOf('ui-icon');
                                    if(index >= 0){
                                        selector.removeClass(cs);
                                    }
                                }
                                if(!selector.hasClass(icon)){
                                    selector.addClass(icon);
                                }
                            }
                            if(styles != undefined){
                                selector.attr('class', '');
                                selector.addClass('ui-btn');
                                selector.addClass(icon);
                                for(let st of styles){
                                    if(!selector.hasClass(st)){
                                        selector.addClass(st);
                                    }
                                }
                            }
                        });
                    });
                    </script>
                    """ % (self._namespace, self._name, self._name)
        return script

    def render(self):
        content = ""
        if self._tag_type == "A":
            content = "<a href='#' "
        else:
            content = "<button "
        content += "id='" + self._name + "' "
        content += "class='" + self.UI_BTN_CLASS + " "
        if self._icon is not None:
            content += self._icon + " "
        if self._btn_styles is not None:
            for st in self._btn_styles:
                content += st.value + " "
        content = content.strip() + "' >"
        if self._title is not None:
            content += self._title
        if self._tag_type == "A":
            content += "</a>"
        else:
            content += "</button>"
        if self._full_round is not None and not self._full_round and self._title is None:
            content = ("<div id='%s-border-radius'>" % (self._name)) + content + "</div>"
            content += (self.ROUND_CORNER_NOTEXT_STYLE % (self._name))
        content += "\n" + self._attach_script()
        return content


class FormButton(Button):
    """An input form button based on the 'input' HTML tag. For button built using 'a' or 'button'
    HTML tag, please see this class's parent class `Button`.
    """

    def __init__(self, name, socket_io, title=None, icon=None, full_round=None, btn_styles=None,
                 click_callback=None):
        Button.__init__(self, name, socket_io, title=title, icon=icon, full_round=full_round,
                        btn_styles=btn_styles, click_callback=click_callback)

    def render(self):
        content = "<div id='" + self._name + "' "
        content += "class='ui-input-btn " + self.UI_BTN_CLASS + " "
        if self._icon is not None:
            content += self._icon + " "
        if self._btn_styles is not None:
            for st in self._btn_styles:
                content += st.value + " "
        content = content.strip() + "' >"
        if self._title is not None:
            content += self._title
        content += "<input type='button' data-enhanced='true' value='"\
                   + (self._title if self._title is not None else '') + "'>"
        content += "</div>"
        if self._full_round is not None and not self._full_round and self._title is None:
            content = ("<div id='%s-border-radius'>" % (self._name)) + content + "</div>"
            content += (self.ROUND_CORNER_NOTEXT_STYLE % (self._name))
        content += "\n" + self._attach_script()
        return content


class CheckBox(Widget, Namespace):
    """Checkbox inputs are used to provide a list of
    options where more than one can be selected.
    Checkbox buttons are enhanced by the checkboxradio widget.
    """

    _items = None
    _orientation = None
    _is_mini = None
    _is_group = None
    _icon_position = None
    _socket_io = None
    _namespace = None
    _click_callback = None
    _legend = None

    def __init__(self, name, socket_io, items=None, is_mini=None, is_group=None,
                 orientation=None, icon_position=None, click_callback=None, legend=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_check").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_check").replace('.', '_')
        self._socketio = socket_io
        self._socketio.on_namespace(self)
        if items is not None:
            self._items = items
        else:
            self._items = []
        if is_mini is not None:
            self._is_mini = is_mini
        else:
            self._is_mini = False
        if is_group is not None:
            self._is_group = is_group
        else:
            self._is_group = False
        if orientation is not None:
            self._orientation = orientation
        else:
            self._orientation = "vertical"
        if icon_position is not None:
            self._icon_position = icon_position
        else:
            self._icon_position = "left"
        self._click_callback = click_callback
        self._legend = legend

    @property
    def namespace(self):
        """Namespace to be used by websockets"""
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def items(self):
        """List of checkbox items as dict objects"""
        return self._items

    @items.setter
    def items(self, val):
        self._items = val

    @property
    def orientation(self):
        """The orientation of the checkbox group i.e., Horizontal or Vertical"""
        return self._orientation

    @orientation.setter
    def orientation(self, val):
        self._orientation = val
        self._sync_properties()

    @property
    def is_mini(self):
        """Set to True for the compact version of the checkboxes"""
        return self._is_mini

    @is_mini.setter
    def is_mini(self, val):
        self._is_mini = val
        self._sync_properties()

    @property
    def is_group(self):
        """Render the checkboxes as Horizontal or Vertical group"""
        return self._is_group

    @is_group.setter
    def is_group(self, val):
        self._is_group = val
        self._sync_properties()

    @property
    def icon_position(self):
        """Position of the icon in reference to checkbox. Can be Left or Right"""
        return self._icon_position

    @icon_position.setter
    def icon_position(self, val):
        self._icon_position = val
        self._sync_properties()

    @property
    def legend(self):
        """The title of the vertical or horizontal group"""
        return self._legend

    @legend.setter
    def legend(self, val):
        self._legend = val
        self._sync_properties()

    def _sync_properties(self):
        emit('sync_properties_' + self._name, {'orientation': self._orientation,
                                               'legend': self._legend},
             namespace=self._namespace)

    def add_item(self, name, title, theme=None, disabled=None):
        """Adds a new item to the collection of checkboxes

            Args:
                name (string): A unique identifier of the checkbox
                title (string): Label to be shown next to the checkbox
                theme (string): Theme swatch to be used for the checkbox
                disabled (boolean): checkbox should be disabled or enabled
        """
        checkbox = {}
        checkbox['name'] = name
        checkbox['title'] = title
        checkbox['state'] = False
        if theme is not None:
            checkbox['theme'] = theme
        else:
            checkbox['theme'] = None
        if disabled is not None:
            checkbox['disabled'] = disabled
        else:
            checkbox['disabled'] = False
        if self._is_mini:
            checkbox['mini'] = True
        else:
            checkbox['mini'] = False
        self._items.append(checkbox)

    def remove_item(self, name):
        """Removes an item from the list of items

            Args:
                name (string): Name of the item that needs to be removed
        """
        for itm in self._items:
            if itm['name'] == name:
                self._items.remove(itm)

    def set_item_title(self, item_name, value):
        emit('sync_item_props_' + self._name, {'item_name': item_name,
                                               'prop_name': 'title',
                                               'value': value},
             namespace=self._namespace)

    def set_item_disabled(self, item_name, value):
        emit('sync_item_props_' + self._name, {'item_name': item_name,
                                               'prop_name': 'disabled',
                                               'value': value},
             namespace=self._namespace)

    def on_fire_click_event(self, data):
        try:
            if self._items is not None:
                for item in self._items:
                    if item['name'] == data['source']:
                        item['state'] = data['state']
            if self._click_callback is not None:
                self._click_callback(data['source'], data['state'], self._items)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            msg = 'Method failed during callback execution: ' + str(e)
            emit('error', {'status': False, 'message': msg})

    def _attach_script(self):
        script = """
                    <script>
                    $(document).ready(function(){
                        var socket = io('%s');

                        socket.on('failed', function(data){
                            alertify.error('Failure: ' + data['message']);
                        });

                        socket.on('warning', function(data){
                            alertify.warning('Incomplete execution: ' + data['message']);
                        });

                        socket.on('success', function(data){
                            alertify.success('Call success acknowledged!');
                        });

                        socket.on('connect', function(){
                        });

                        socket.on('sync_item_props_%s', function(props){
                            var selector = $('#' + props['item_name']);
                            var selector_lbl = $('#' + props['item_name'] + '_lbl');
                            if(props['prop_name'] == 'disabled'){
                                selector.prop('disabled', props['value']);
                            }
                            if(props['prop_name'] == 'title'){
                                selector_lbl.text(props['value']);
                            }
                        });

                        socket.on('sync_properties_%s', function(props){
                            var fldst_selector = $('#%s_fldset');
                            var lgnd_selector = $('#%s_lgnd');
                            var orientation = props['orientation'];
                            var legend = props['legend'];

                            //Change legend
                            if(lgnd_selector != undefined){
                                if(legend != undefined){
                                    lgnd_selector.text(legend);
                                }
                            }
                            //Change orientation
                            if(orientation == "horizontal"){
                                if(fldst_selector.hasClass('ui-controlgroup-vertical')){
                                    fldst_selector.removeClass('ui-controlgroup-vertical');
                                }
                                fldst_selector.addClass('ui-controlgroup-horizontal');
                            } else {
                                if(fldst_selector.hasClass('ui-controlgroup-horizontal')){
                                    fldst_selector.removeClass('ui-controlgroup-horizontal');
                                }
                                fldst_selector.addClass('ui-controlgroup-vertical');
                            }
                        });
                    });
                    </script>
                    """ % (self._namespace, self._name, self._name, self._name, self._name)
        return script

    def render(self):
        content = ""
        if self._is_group:
            content = "<fieldset data-role='controlgroup' "
            if self._orientation == "horizontal":
                content += "data-type='horizontal' "
            if self._icon_position == "right":
                content += "data-iconpos='right' "
            content += "id='" + self._name + "_fldset' >\n"
            if self._legend is not None:
                content += "<legend id='" + self._name + "_lgnd'>" + self._legend + "</legend>\n"
        if self._items is not None:
            for item in self._items:
                content += "<input type='checkbox' name='" + item['name'] + "' "
                content += "id='" + item['name'] + "' onclick='"
                content += """  var socket = io("%s");
                                socket.emit("fire_click_event", {"source": this.name, "state": this.checked});
                            """ % (self._namespace)
                content += "' "
                if item['mini']:
                    content += "data-mini='true' "
                if item['theme'] is not None:
                    content += "data-theme='" + item['theme'] + "' "
                if item['disabled']:
                    content += "disabled='' "
                content += ">\n"
                content += "<label for='" + item['name'] + "' id='" + item['name'] + "_lbl' >"\
                    + item['title'] + "</label>\n"
        if self._is_group:
            content += "</fieldset>\n" + self._attach_script()
        return content


class Radio(CheckBox):
    """Radio inputs are used to provide a list of options
    where only a single option can be selected.
    Radio buttons are enhanced by the checkboxradio widget.
    """

    def __init__(self, name, socket_io, items=None, is_mini=None, is_group=None,
                 orientation=None, icon_position=None, click_callback=None, legend=None):
        CheckBox.__init__(self, name, socket_io, items=items, is_mini=is_mini, is_group=is_group,
                          orientation=orientation, icon_position=icon_position, click_callback=click_callback,
                          legend=legend)

    def render(self):
        content = ""
        if self._is_group:
            content = "<fieldset data-role='controlgroup' "
            if self._orientation == "horizontal":
                content += "data-type='horizontal' "
            if self._icon_position == "right":
                content += "data-iconpos='right' "
            content += "id='" + self._name + "_fldset' >\n"
            if self._legend is not None:
                content += "<legend id='" + self._name + "_lgnd'>" + self._legend + "</legend>\n"
        if self._items is not None:
            for item in self._items:
                content += "<input type='radio' name='" + self._name + "_grp' "
                content += "id='" + item['name'] + "' onclick='"
                content += """  var socket = io("%s");
                                socket.emit("fire_click_event", {"source": this.id, "state": this.checked});
                            """ % (self._namespace)
                content += "' "
                if item['mini']:
                    content += "data-mini='true' "
                if item['theme'] is not None:
                    content += "data-theme='" + item['theme'] + "' "
                if item['disabled']:
                    content += "disabled='' "
                content += ">\n"
                content += "<label for='" + item['name'] + "' id='" + item['name'] + "_lbl' >"\
                    + item['title'] + "</label>\n"
        if self._is_group:
            content += "</fieldset>\n" + self._attach_script()
        return content


class Collapsible(Namespace, Widget):
    """Collapsibles are simple widgets that allow you
    to expand or collapse content when tapped and are
    useful in mobile to provide a compact presentation
    of content.
    """

    _title = None
    _theme = None
    _content_theme = None
    _is_collapsed = None
    _is_mini = None
    _collapsed_icon = None
    _expanded_icon = None
    _iconpos = None
    _is_fieldset = None
    _legend = None
    _is_inset = None
    _corners = None
    _disabled = None
    _socket_io = None
    _namespace = None
    _click_callback = None

    def __init__(self, name, title, socket_io, theme=None, content_theme=None, is_collapsed=None,
                 is_mini=None, collapsed_icon=None, expanded_icon=None, iconpos=None,
                 is_fieldset=None, legend=None, is_inset=None, corners=None, click_callback=None,
                 disabled=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + self._name + "_colpse").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + self._name + "_colpse").replace('.', '_')
        self._title = title
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._theme = theme
        self._content_theme = content_theme
        self._is_collapsed = is_collapsed
        self._is_mini = is_mini
        self._collapsed_icon = collapsed_icon
        self._expanded_icon = expanded_icon
        self._iconpos = iconpos
        self._is_fieldset = is_fieldset
        self._legend = legend
        self._is_inset = is_inset
        self._corners = corners
        self._disabled = disabled
        self._click_callback = click_callback

    @property
    def namespace(self):
        """Namespace to be used by the websocket framework"""
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def title(self):
        """Header or title of collapsible widget"""
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties('heading', val)

    @property
    def theme(self):
        """Theme to be used by the header of collapsible widget"""
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val
        self._sync_properties('theme', val)

    @property
    def content_theme(self):
        """Theme to be used by content of the widget. Set the
        value of this property to False to have no theme applied
        at all
        """
        return self._content_theme

    @content_theme.setter
    def content_theme(self, val):
        self._content_theme = val
        self._sync_properties('contentTheme', val)

    @property
    def is_collapsed(self):
        """If set to True, widget will be rendered as collapsed"""
        return self._is_collapsed

    @is_collapsed.setter
    def is_collapsed(self, val):
        self._is_collapsed = val
        self._sync_properties('collapsed', val)

    @property
    def is_mini(self):
        """If set to True, widget will be rendered in compact mode"""
        return self._is_mini

    @is_mini.setter
    def is_mini(self, val):
        self._is_mini = val
        self._sync_properties('mini', val)

    @property
    def collapsed_icon(self):
        """The icon to be shown when widget is collapsed. Default is the + sign"""
        return self._collapsed_icon

    @collapsed_icon.setter
    def collapsed_icon(self, val):
        self._collapsed_icon = val
        self._sync_properties('collapsedIcon', val)

    @property
    def expanded_icon(self):
        """The icon to be shown when widget is expanded, default is - sign"""
        return self._expanded_icon

    @expanded_icon.setter
    def expanded_icon(self, val):
        self._expanded_icon = val
        self._sync_properties('expandedIcon', val)

    @property
    def icon_position(self):
        """The position of the icon; It can bse either right or left"""
        return self._iconpos

    @icon_position.setter
    def icon_position(self, val):
        self._iconpos = val
        self._sync_properties('iconpos', val)

    @property
    def is_fieldset(self):
        """Whether to use fieldset to group child items or not """
        return self._is_fieldset

    @is_fieldset.setter
    def is_fieldset(self, val):
        self._is_fieldset = val

    @property
    def legend(self):
        """The legend to be shown if `is_fieldset` is set to True"""
        return self._legend

    @legend.setter
    def legend(self, val):
        self._legend = val
        self._sync_properties('heading', val)

    @property
    def is_inset(self):
        """Whether to show the widget inset or not"""
        return self._is_inset

    @is_inset.setter
    def is_inset(self, val):
        self._is_inset = val
        self._sync_properties('inset', val)

    @property
    def corners(self):
        """Whether to have round corners or not"""
        return self._corners

    @corners.setter
    def corners(self, val):
        self._corners = val
        self._sync_properties('corners', val)

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    def on_fire_click_event(self, props):  # noqa
        clspd = props['collapsed']
        if clspd is not None:
            self._is_collapsed = clspd
        clspdIcn = props['collapsedIcon']
        if clspdIcn is not None:
            self._collapsed_icon = clspdIcn
        conthme = props['contentTheme']
        if conthme is not None:
            self._content_theme = conthme
        crnrs = props['corners']
        if crnrs is not None:
            self._corners = crnrs
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        expndIcon = props['expandedIcon']
        if expndIcon is not None:
            self._expanded_icon = expndIcon
        head = props['heading']
        if head is not None and head != "h1,h2,h3,h4,h5,h6,legend":
            self._title = head
        icnpos = props['iconpos']
        if icnpos is not None:
            self._iconpos = icnpos
        inst = props['inset']
        if inst is not None:
            self._is_inset = inst
        mini = props['mini']
        if mini is not None:
            self._is_mini = mini
        thm = props['theme']
        if thm is not None:
            self._theme = thm
        if self._click_callback is not None:
            self._click_callback(self._name, props)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def _attach_script(self):
        script = """
                <script>
                    (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');
                            var head_selector = $('#%s_head');

                            socket.on('sync_properties_%s', function(props){
                                selector.collapsible("option", props['cmd'], props['value']);
                            });

                            selector.bind('vclick', function(){
                                props = {
                                            'collapsed': selector.collapsible("option", "collapsed"),
                                            'collapsedIcon': selector.collapsible("option", "collapsedIcon"),
                                            'contentTheme': selector.collapsible("option", "contentTheme"),
                                            'corners': selector.collapsible("option", "corners"),
                                            'disabled': selector.collapsible("option", "disabled"),
                                            'expandedIcon': selector.collapsible("option", "expandedIcon"),
                                            'heading': selector.collapsible("option", "heading"),
                                            'iconpos': selector.collapsible("option", "iconpos"),
                                            'inset': selector.collapsible("option", "inset"),
                                            'mini': selector.collapsible("option", "mini"),
                                            'theme': selector.collapsible("option", "theme")
                                        };
                                socket.emit("fire_click_event", props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name, self._name)
        return script

    def render(self):       # noqa
        """Renders the widget contents"""
        content = ""
        if self._is_fieldset is not None and self._is_fieldset:
            content = "<fieldset data-role='collapsible' id='" + self._name + "' "
        else:
            content = "<div data-role='collapsible' id='" + self._name + "' "
        if self._theme is not None:
            content += "data-theme='" + self._theme + "' "
        if self._content_theme is not None:
            content += "data-content-theme='" + self._content_theme + "' "
        if self._is_collapsed is not None and not self._is_collapsed:
            content += "data-collapsed='false' "
        if self._is_mini is not None and self._is_mini:
            content += "data-mini='true' "
        if self._collapsed_icon is not None:
            content += "data-collapsed-icon='" + self._collapsed_icon + "' "
        if self._expanded_icon is not None:
            content += "data-expanded-icon='" + self._expanded_icon + "' "
        if self._iconpos is not None:
            content += "data-iconpos='" + self._iconpos + "' "
        if self._is_inset is not None and not self._is_inset:
            content += "data-inset='false' "
        content += ">\n"
        if self._is_fieldset is not None and self._is_fieldset:
            if self._legend is not None:
                content += "<legend id='" + self._name + "_head'>" + self._legend + "</legend>\n"
        else:
            if self._title is not None:
                content += "<h4 id='" + self._name
                content += "_head'>" + self._title + "</h4>\n"
        if self._child_widgets is not None:
            for widget in self._child_widgets:
                content += widget.render() + "\n"
        if self._is_fieldset is not None and self._is_fieldset:
            content += "</fieldset>"
        else:
            content += "</div>"
        content += "\n" + self._attach_script()
        return content


class CollapsibleSet(Collapsible):
    """Collapsible set work as the collection for collapsible
    widgets"""

    _no_corners = None
    _use_filter = None

    def __init__(self, name, title, socket_io, theme=None, content_theme=None, is_collapsed=None,
                 is_mini=None, collapsed_icon=None, expanded_icon=None, iconpos=None,
                 is_fieldset=None, legend=None, is_inset=None, click_callback=None, items=None, no_corners=None,
                 use_filter=None):
        Collapsible.__init__(self, name, None, socket_io, theme=theme, content_theme=content_theme,
                             is_collapsed=is_collapsed, is_mini=is_mini, collapsed_icon=collapsed_icon,
                             expanded_icon=expanded_icon, iconpos=iconpos, is_fieldset=None, legend=None,
                             is_inset=is_inset, click_callback=click_callback)
        if items is not None:
            self._child_widgets = items
        else:
            self._child_widgets = []
        self._no_corners = no_corners
        self._use_filter = use_filter

    def render(self):       # noqa
        """Renders the widget contents"""
        content = ""
        if self._use_filter is not None and self._use_filter:
            content = "<input data-type='search' id='" + self._name + "_query_value' />\n"
            content += "<div data-role='collapsibleset' data-filter='true' data-input='#" + self._name + "_query_value' "  # noqa
        else:
            content = "<div data-role='collapsibleset' "
        if self._theme is not None:
            content += "data-theme='" + self._theme + "' "
        if self._content_theme is not None:
            content += "data-content-theme='" + self._content_theme + "' "
        if self._is_collapsed is not None and not self._is_collapsed:
            content += "data-collapsed='false' "
        if self._is_mini is not None and self._is_mini:
            content += "data-mini='true' "
        if self._collapsed_icon is not None:
            content += "data-collapsed-icon='" + self._collapsed_icon + "' "
        if self._expanded_icon is not None:
            content += "data-expanded-icon='" + self._expanded_icon + "' "
        if self._iconpos is not None:
            content += "data-iconpos='" + self._iconpos + "' "
        if self._is_inset is not None and not self._is_inset:
            content += "data-inset='false' "
        if self._no_corners is not None and self._no_corners:
            content += "data-corners='false' "
        content += ">\n"
        if self._child_widgets is not None:
            for widget in self._child_widgets:
                content += widget.render() + "\n"
        content += "</div>"
        return content


class ControlGroup(Widget, Namespace):
    """Controlgroups are used to visually group a set of buttons to
    form a single block that looks contained like a navigation component.
    """

    _socket_io = None
    _namespace = None
    _corners = None
    _disabled = None
    _exclude_invisible = None
    _mini = None
    _shadow = None
    _theme = None
    _type = None
    _is_fieldset = None
    _legend = None
    _use_filter = None

    def __init__(self, name, socket_io, corners=None, disabled=None, exclude_invisible=None,
                 mini=None, shadow=None, theme=None, type=None, items=None, is_fieldset=None,
                 legend=None, use_filter=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_cg").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_cg").replace('.', '_')
        self._socket_io = socket_io
        self._corners = corners
        self._disabled = disabled
        self._exclude_invisible = exclude_invisible
        self._mini = mini
        self._shadow = shadow
        self._theme = theme
        self._type = type
        self._child_widgets = items
        self._is_fieldset = is_fieldset
        self._legend = legend
        if items is not None:
            self._child_widgets = items
        else:
            self._child_widgets = []
        self._use_filter = use_filter

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def corners(self):
        return self._corners

    @corners.setter
    def corners(self, val):
        self._corners = val
        self._sync_properties('corners', val)

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def exclude_invisible(self):
        return self._exclude_invisible

    @exclude_invisible.setter
    def exclude_invisible(self, val):
        self._exclude_invisible = val
        self._sync_properties('excludeInvisible', val)

    @property
    def mini(self):
        return self._mini

    @mini.setter
    def mini(self, val):
        self._mini = val
        self._sync_properties('mini', val)

    @property
    def shadow(self):
        return self._shadow

    @shadow.setter
    def shadow(self, val):
        self._shadow = val
        self._sync_properties('shadow', val)

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val
        self._sync_properties('theme', val)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val
        self._sync_properties('type', val)

    @property
    def is_fieldset(self):
        return self._is_fieldset

    @is_fieldset.setter
    def is_fieldset(self, val):
        self._is_fieldset = val

    @property
    def legend(self):
        return self._legend

    @legend.setter
    def legend(self, val):
        self._legend = val

    def on_fire_click_event(self, props):  # noqa
        crnrs = props['corners']
        if crnrs is not None:
            self._corners = crnrs
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        mini = props['mini']
        if mini is not None:
            self._is_mini = mini
        thm = props['theme']
        if thm is not None:
            self._theme = thm
        xludeInvisi = props['excludeInvisible']
        if xludeInvisi is not None:
            self._exclude_invisible = xludeInvisi
        shdw = props['shadow']
        if shdw is not None:
            self._shadow = shdw
        typ = props['type']
        if typ is not None:
            self._type = typ
        if self._click_callback is not None:
            self._click_callback(self._name, props)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def _attach_script(self):
        script = """
                <script>
                    (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');
                            var head_selector = $('#%s_lgnd');

                            socket.on('sync_properties_%s', function(props){
                                selector.controlgroup("option", props['cmd'], props['value']);
                            });

                            selector.bind('vclick', function(){
                                props = {
                                            'corners': selector.controlgroup("option", "corners"),
                                            'disabled': selector.controlgroup("option", "disabled"),
                                            'mini': selector.controlgroup("option", "mini"),
                                            'theme': selector.controlgroup("option", "theme"),
                                            'excludeInvisible': selector.controlgroup("option", "excludeInvisible"),
                                            'shadow': selector.controlgroup("option", "shadow"),
                                            'type': selector.controlgroup("option", "type")
                                        };
                                socket.emit("fire_click_event", props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name, self._name)
        return script

    def render(self):  # noqa
        content = ""
        if self._use_filter is not None and self._use_filter:
            content = "<input data-type='search' id='" + self._name + "_filter_query' />\n"
        if self._is_fieldset is not None and self._is_fieldset:
            content += "<fieldset data-role='controlgroup' id='" + self._name + "' "
        else:
            content += "<div data-role='controlgroup' id='" + self._name + "' "
        if self._use_filter is not None and self._use_filter:
            content += "data-filter='true' data-input='#" + self._name + "_filter_query' "
        if self._mini is not None and self._mini:
            content += "data-mini='true' "
        if self._type is not None and self._type == "horizontal":
            content += "data-type='horizontal' "
        if self._corners is not None and not self._corners:
            content += "data-corners='false' "
        if self._disabled is not None and self._disabled:
            content += "data-disabled='true' "
        if self._exclude_invisible is not None and not self._exclude_invisible:
            content += "data-exclude-invisible='false' "
        if self._shadow is not None and not self._shadow:
            content += "data-shadow='false' "
        if self._theme is not None:
            content += "theme='" + self._theme + "' "
        content += ">\n"
        if self._is_fieldset is not None and self._is_fieldset:
            if self._legend is not None:
                content += "<legend id='" + self._name + "_lgnd' >" + self._legend + "</legend>\n"
        if self._child_widgets is not None:
            for widget in self._child_widgets:
                content += widget.render()
        if self._is_fieldset is not None and self._is_fieldset:
            content += "</fieldset>\n"
        else:
            content += "</div>\n"
        content += self._attach_script()
        return content


class FlipSwitch(Widget, Namespace):
    """Flip switches are used for boolean style inputs like
    true/false or on/off in a compact UI element
    """

    _namespace = None
    _socket_io = None
    _on_text = None
    _off_text = None
    _is_checked = None
    _switch_kind = None
    _select_options = None
    _theme = None
    _is_mini = None
    _no_corners = None
    _is_disabled = None
    _custom_size = None
    _click_callback = None
    _custom_label_css = None
    _custom_label_size_css = None

    _data_wrapper_class_size = "custom-size-flipswitch"
    _data_wrapper_class_label = "custom-label-flipswitch"

    CUSTOM_LABEL_CSS = """
                        <style>
                        .custom-label-flipswitch.ui-flipswitch .ui-btn.ui-flipswitch-on {
                            text-indent: -3.4em;
                        }
                        .custom-label-flipswitch.ui-flipswitch .ui-flipswitch-off {
                            text-indent: 0.5em;
                        }
                        </style>
                        """
    CUSTOM_SIZE_CSS = """
                    <style>
                    /* Custom indentations are needed because the length of custom labels differs from
                    the length of the standard labels */
                    .custom-size-flipswitch.ui-flipswitch .ui-btn.ui-flipswitch-on {
                        text-indent: -5.9em;
                    }
                    .custom-size-flipswitch.ui-flipswitch .ui-flipswitch-off {
                        text-indent: 0.5em;
                    }
                    /* Custom widths are needed because the length of custom labels differs from
                    the length of the standard labels */
                    .custom-size-flipswitch.ui-flipswitch {
                        width: 8.875em;
                    }
                    .custom-size-flipswitch.ui-flipswitch.ui-flipswitch-active {
                        padding-left: 7em;
                        width: 1.875em;
                    }
                    @media (min-width: 28em) {
                        /*Repeated from rule .ui-flipswitch above*/
                        .ui-field-contain > label + .custom-size-flipswitch.ui-flipswitch {
                            width: 1.875em;
                        }
                    }
                    </style>
                    """

    def __init__(self, name, socket_io, on_text=None, off_text=None, is_checked=None, switch_kind=None,
                 select_options=None, theme=None, is_mini=None, no_corners=None, is_disabled=None,
                 custom_size=None, click_callback=None, custom_label_css=None, custom_label_size_css=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + self._name + "_fs").replace(".", "_"))
        self._namespace = '/' + str(__name__ + "_" + self._name + "_fs").replace(".", "_")
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._on_text = on_text
        self._off_text = off_text
        if is_checked is not None:
            self._is_checked = is_checked
        else:
            self._is_checked = False
        if switch_kind is not None:
            self._switch_kind = switch_kind
        else:
            self._switch_kind = "checkbox"
        if select_options is not None:
            self._select_options = select_options
        else:
            self._select_options = []
        self._theme = theme
        if is_mini is not None:
            self._is_mini = is_mini
        else:
            self._is_mini = False
        if is_disabled is not None:
            self._is_disabled = is_disabled
        else:
            self._is_disabled = False
        if no_corners is not None:
            self._no_corners = no_corners
        else:
            self._no_corners = False
        if custom_size is not None:
            self._custom_size = custom_size
        else:
            self._custom_size = False
        self._click_callback = click_callback
        self._custom_label_css = custom_label_css
        self._custom_label_size_css = custom_label_size_css

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def on_text(self):
        return self._on_text

    @on_text.setter
    def on_text(self, val):
        self._on_text = val
        self._sync_properties('onText', val)

    @property
    def off_text(self):
        return self._off_text

    @off_text.setter
    def off_text(self, val):
        self._off_text = val
        self._sync_properties('offText', val)

    @property
    def is_checked(self):
        return self._is_checked

    @is_checked.setter
    def is_checked(self, val):
        self._is_checked = val
        self._sync_properties('checked', val)

    @property
    def switch_kind(self):
        return self._switch_kind

    @switch_kind.setter
    def switch_kind(self, val):
        self._switch_kind = val

    @property
    def select_options(self):
        return self._select_options

    @select_options.setter
    def select_options(self, val):
        self._select_options = val

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val
        self._sync_properties('theme', val)

    @property
    def is_mini(self):
        return self._is_mini

    @is_mini.setter
    def is_mini(self, val):
        self._is_mini = val
        self._sync_properties('mini', val)

    @property
    def is_disabled(self):
        return self._is_disabled

    @is_disabled.setter
    def is_disabled(self, val):
        self._is_disabled = val
        self._sync_properties('disabled', val)

    @property
    def no_corners(self):
        return self._no_corners

    @no_corners.setter
    def no_corners(self, val):
        self._no_corners = val
        self._sync_properties('corners', val)

    def add_option(self, value):
        if self._select_options is None:
            self._select_options = []
        self._select_options.append(value)

    def remove_option(self, value):
        if self._select_options is not None:
            self._select_options.pop(value)

    def on_fire_click_event(self, props):  # noqa
        crnrs = props['corners']
        if crnrs is not None:
            self._corners = crnrs
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        mini = props['mini']
        if mini is not None:
            self._is_mini = mini
        thm = props['theme']
        if thm is not None:
            self._theme = thm
        offtxt = props['offText']
        if offtxt is not None:
            self._off_text = offtxt
        ontxt = props['onText']
        if ontxt is not None:
            self._on_text = ontxt
        chk = props['checked']
        if chk is not None:
            self._is_checked = chk
        if self._click_callback is not None:
            self._click_callback(self._name, props)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def _attach_script(self):
        script = """
                <script>
                    (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');

                            socket.on('sync_properties_%s', function(props){
                                selector.flipswitch("option", props['cmd'], props['value']);
                                selector.flipswitch('refresh');
                            });

                            selector.bind('change', function(){
                                props = {
                                            'corners': selector.flipswitch("option", "corners"),
                                            'disabled': selector.flipswitch("option", "disabled"),
                                            'mini': selector.flipswitch("option", "mini"),
                                            'theme': selector.flipswitch("option", "theme"),
                                            'offText': selector.flipswitch("option", "offText"),
                                            'onText': selector.flipswitch("option", "onText"),
                                            'checked': selector.is(':checked')
                                        };
                                socket.emit("fire_click_event", props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name)
        return script

    def render(self):  # noqa
        content = ""
        if self._custom_label_css is not None:
            content += self._custom_label_css + "\n"
        else:
            content += self.CUSTOM_LABEL_CSS + "\n" 
        if self._custom_label_size_css is not None:
            content += self._custom_label_size_css + "\n"
        else:
            content += self.CUSTOM_SIZE_CSS + "\n"
        if self._switch_kind == "checkbox":
            content += "<input type='checkbox' data-role='flipswitch' "
        else:
            content += "<select data-role='flipswitch' "
        content += "id='" + self._name + "' "
        if self._on_text is not None:
            content += "data-on-text='" + self._on_text + "' "
        if self._off_text is not None:
            content += "data-off-text='" + self._off_text + "' "
        if (self._on_text is not None or self._off_text is not None) and not self._custom_size:
            content += "data-wrapper-class='" + self._data_wrapper_class_label + "' "
        if (self._on_text is not None or self._off_text is not None) and self._custom_size:
            content += "data-wrapper-class='" + self._data_wrapper_class_size + "' "
        if self._switch_kind == "checkbox" and self._is_checked:
            content += "checked='' "
        if self._theme is not None:
            content += "data-theme='" + self._theme + "' "
        if self._is_mini:
            content += "data-mini='true' "
        if self._no_corners:
            content += "data-corners='false' "
        if self._is_disabled:
            content += "disabled='disabled' "
        content += ">\n"
        if self._switch_kind != "checkbox":
            for option in self._select_options:
                content += "<option>" + option + "</option>\n"
            content += "</select>\n"
        else:
            content += "</input>\n" + self._attach_script()
        return content
