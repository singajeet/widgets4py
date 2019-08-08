"""
This module contains the API's to create app for mobile using
JQuery Mobile framework

Author: Ajeet Singh
Date: 07/30/2019
"""
from flask import json
from flask_socketio import Namespace, emit
from widgets4py.base import Widget
from enum import Enum


class MobilePage(Widget, Namespace):
    """The mobile will will act as parent widget to hold all
    other widgets for mobile
    """

    _title = None
    _header_widgets = None
    _footer_widgets = None
    _panel_widgets = None
    _socketio = None
    _footer_title = None
    _before_render_callback = None
    _after_render_callback = None
    _close_button = None
    _close_button_text = None
    _contentTheme = None
    _corners = None
    _is_dialog = None
    _is_disabled = None
    _dom_cache = None
    _overlay_theme = None
    _theme = None
    _namespace = None
    _click_callback = None

    def __init__(self, name, title, socketio, header_widgets=None, footer_widgets=None,
                 child_widgets=None, footer_title=None, before_render_callback=None,
                 after_render_callback=None, close_button=None, close_button_text=None,
                 content_theme=None, corners=None, is_dialog=None, is_disabled=None,
                 dom_cache=None, overlay_theme=None, theme=None, click_callback=None,
                 panel_widgets=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + name + "_page").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + name + "_page").replace('.', '_')
        self._title = title
        self._socketio = socketio
        self._socketio.on_namespace(self)
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
        self._close_button = close_button
        self._close_button_text = close_button_text
        self._content_theme = content_theme
        self._corners = corners
        self._is_dialog = is_dialog
        self._is_disabled = is_disabled
        self._dom_cache = dom_cache
        self._overlay_theme = overlay_theme
        self._theme = theme
        self._click_callback = click_callback
        if panel_widgets is not None:
            self._panel_widgets = panel_widgets
        else:
            self._panel_widgets = []

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val
        self._sync_properties('theme', val)

    @property
    def overlay_theme(self):
        return self._overlay_theme

    @overlay_theme.setter
    def overlay_theme(self, val):
        self._overlay_theme = val
        self._sync_properties('overlayTheme', val)

    @property
    def dom_cache(self):
        return self._dom_cache

    @dom_cache.setter
    def dom_cache(self, val):
        self._dom_cache = val
        self._sync_properties('domCache', val)

    @property
    def is_disabled(self):
        return self._is_disabled

    @is_disabled.setter
    def is_disabled(self, val):
        self._is_disabled = val
        self._sync_properties('disabled', val)

    @property
    def is_dialog(self):
        return self._is_dialog

    @is_dialog.setter
    def is_dialog(self, val):
        self._is_dialog = val
        self._sync_properties('dialog', val)

    @property
    def corners(self):
        return self._corners

    @corners.setter
    def corners(self, val):
        self._corners = val
        self._sync_properties('corners', val)

    @property
    def content_theme(self):
        return self._content_theme

    @content_theme.setter
    def content_theme(self, val):
        self._content_theme = val
        self._sync_properties('contentTheme', val)

    @property
    def close_button_text(self):
        return self._close_button_text

    @close_button_text.setter
    def close_button_text(self, val):
        self._close_button_text = val
        self._sync_properties('closeBtnText', val)

    @property
    def close_button(self):
        return self._close_button

    @close_button.setter
    def close_button(self, val):
        self._close_button = val
        self._sync_properties('closeBtn', val)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def header_widgets(self):
        return self._header_widgets

    @header_widgets.setter
    def header_widgets(self, val):
        self._header_widgets = val

    @property
    def child_widgets(self):
        return self._child_widgets

    @child_widgets.setter
    def child_widgets(self, val):
        self._child_widgets = val

    @property
    def footer_widgets(self):
        return self._footer_widgets

    @footer_widgets.setter
    def footer_widgets(self, val):
        self._footer_widgets = val

    @property
    def panel_widgets(self):
        return self._panel_widgets

    @panel_widgets.setter
    def panel_widgets(self, val):
        self._panel_widgets = val

    @property
    def footer_title(self):
        return self._footer_title

    @footer_title.setter
    def footer_title(self, val):
        self._footer_title = val

    def add_panel(self, panel):
        self._panel_widgets.append(panel)

    def remove_panel(self, panel):
        self._panel_widgets.remove(panel)

    def add_header_widget(self, widget):
        self._header_widgets.append(widget)

    def remove_header_widget(self, widget):
        self._header_widgets.remove(widget)

    def add_footer_widget(self, widget):
        self._footer_widgets.append(widget)

    def remove_footer_widget(self, widget):
        self._footer_widgets.remove(widget)

    def on_before_render_event(self, callback):
        self._before_render_callback = callback

    def on_after_render_event(self, callback):
        self._after_render_callback = callback

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def on_fire_click_event(self, props):
        if self._click_callback is not None:
            self._click_callback(self._name, props)

    def _attach_script(self):
        script = """
                <script>
                (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');

                            socket.on('sync_properties_%s', function(props){
                                selector.page("option", props['cmd'], props['value']);
                            });

                            selector.bind('vclick', function(){
                                props = {
                                            'closeBtn': selector.page("option", "closeBtn"),
                                            'closeBtnText': selector.page("option", "closeBtnText"),
                                            'contentTheme': selector.page("option", "contentTheme"),
                                            'corners': selector.page("option", "corners"),
                                            'dialog': selector.page("option", "dialog"),
                                            'disabled': selector.page("option", "disabled"),
                                            'domCache': selector.page("option", "domCache"),
                                            'overlayTheme': selector.page("option", "overlayTheme"),
                                            'theme': selector.page("option", "theme")
                                        };
                                socket.emit("fire_click_event", props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name)
        return script

    def render(self):  # noqa
        """Render the contents of mobile page in browser"""
        if self._before_render_callback is not None:
            self._before_render_callback(self._name, {'title': self._title,
                                                      'footer_title': self._footer_title})
        panel_content = ""
        if self._panel_widgets is not None:
            for pwidget in self._panel_widgets:
                panel_content += pwidget.render()
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
        content = "<div data-role='page' id='" + self._name + "' "
        if self._close_button is not None:
            content += "data-close-btn='" + self._close_button + "' "
        if self._close_button_text is not None:
            content += "data-close-btn-text='" + self._close_button_text + "' "
        if self._content_theme is not None:
            content += "data-content-theme='" + self._content_theme + "' "
        if self._corners is not None:
            content += "data-corners='" + self._corners + "' "
        if self._is_dialog is not None:
            content += "data-dialog='" + json.dumps(self._is_dialog) + "' "
        if self._is_disabled is not None:
            content += "data-disabled='" + json.dumps(self._is_disabled) + "' "
        if self._dom_cache is not None:
            content += "data-dom_cache='" + self._dom_cache + "' "
        if self._overlay_theme is not None:
            content += "data-overlay-theme='" + self._overlay_theme + "' "
        if self._theme is not None:
            content += "data-theme='" + self._theme + "' "
        content += ">"
        content += """   <!-- panels -->
                            %s
                         <!-- /panels -->
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
                """ % (panel_content, self._title, header_content, child_content,
                       self._footer_title, footer_content)
        if self._after_render_callback is not None:
            self._after_render_callback(self._name, {'title': self._title,
                                                     'footer_title': self._footer_title})
        return content


class MultiPage(Widget):
    """This class is the collection of multiple virtual pages that will be rendered on
    a single page in reality. Please check 'Multi-Page' section in the JQuery Mobile
    for more information
    """

    def __init__(self, name, pages):
        Widget.__init__(self, name)
        if pages is not None:
            self._child_widgets = pages
        else:
            self._child_widgets = []

    def add_page(self, page):
        """Adds a new page of type `MobilePage` to this MultiPage widget

            Args:
                page (MobilePage): Instance of the `MobilePage` widget
        """
        self._child_widgets.append(page)

    def remove_page(self, page):
        """Removes a page of type `MobilePage` from this widget

            Args:
                page (MobilePage): Instance of the `MobilePage` widget
        """
        self._child_widgets.remove(page)

    def render(self):
        """Renders all the child pages"""
        content = ""
        for page in self._child_widgets:
            content += page.render() + "\n"
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
    _href = None
    _data_rel = None

    def __init__(self, name, socket_io, title=None, icon=None, full_round=None, tag_type=None,
                 btn_styles=None, click_callback=None, href=None, data_rel=None):
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
        self._href = href
        self._data_rel = data_rel

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

    @property
    def href(self):
        return self._href

    @href.setter
    def href(self, val):
        self._href = val

    @property
    def data_rel(self):
        return self._data_rel

    @data_rel.setter
    def data_rel(self, val):
        self._data_rel = val

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

    def render(self):  # noqa
        content = ""
        if self._tag_type == "A":
            if self._href is None:
                content = "<a href='#' "
            else:
                content += "<a href='" + self._href + "' "
            if self._data_rel is not None:
                content += "data-rel='" + self._data_rel + "' "
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
    _collapse_callback = None
    _expand_callback = None

    def __init__(self, name, title, socket_io, theme=None, content_theme=None, is_collapsed=None,
                 is_mini=None, collapsed_icon=None, expanded_icon=None, iconpos=None,
                 is_fieldset=None, legend=None, is_inset=None, corners=None, collapse_callback=None,
                 expand_callback=None, disabled=None):
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
        self._collapse_callback = collapse_callback
        self._expand_callback = expand_callback

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

    def on_fire_collapse_event(self, props):  # noqa
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
        if self._collapse_callback is not None:
            self._collapse_callback(self._name, props)

    def on_fire_expand_event(self, props):  # noqa
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
        if self._expand_callback is not None:
            self._expand_callback(self._name, props)

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
                                selector.collapsible("option", props['cmd'], props['value']);
                            });

                            selector.on( "collapsiblecollapse", function( event, ui ) {
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
                                socket.emit("fire_collapse_event", props);
                            } );

                            selector.on( "collapsibleexpand", function( event, ui ) {
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
                                socket.emit("fire_expand_event", props);
                            } );
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name)
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
                 is_fieldset=None, legend=None, is_inset=None, collapse_callback=None, items=None,
                 no_corners=None, use_filter=None):
        Collapsible.__init__(self, name, None, socket_io, theme=theme, content_theme=content_theme,
                             is_collapsed=is_collapsed, is_mini=is_mini, collapsed_icon=collapsed_icon,
                             expanded_icon=expanded_icon, iconpos=iconpos, is_fieldset=None, legend=None,
                             is_inset=is_inset, collapse_callback=collapse_callback)
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
    _change_callback = None
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
                 custom_size=None, change_callback=None, custom_label_css=None, custom_label_size_css=None):
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
        self._change_callback = change_callback
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

    def on_fire_change_event(self, props):  # noqa
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
        if self._change_callback is not None:
            self._change_callback(self._name, props)

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
                                socket.emit("fire_change_event", props);
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


class GridLayout(Widget):
    """A simple CSS based columns"""

    _column_count = None
    _ui_grid_solo = ['ui-block-a']
    _ui_grid_a = ['ui-block-a', 'ui-block-b']
    _ui_grid_b = ['ui-block-a', 'ui-block-b', 'ui-block-c']
    _ui_grid_c = ['ui-block-a', 'ui-block-b', 'ui-block-c', 'ui-block-d']
    _ui_grid_d = ['ui-block-a', 'ui-block-b', 'ui-block-c', 'ui-block-d', 'ui-block-e']
    _ui_grids = [_ui_grid_solo, _ui_grid_a, _ui_grid_b, _ui_grid_c, _ui_grid_d]
    _ui_grid_types = ['ui-grid-solo', 'ui-grid-a', 'ui-grid-b', 'ui-grid-c', 'ui-grid-d']

    def __init__(self, name, col_count, items=None):
        Widget.__init__(self, name)
        if col_count <= 5:
            self._column_count = col_count
        else:
            self._column_count = 5
        if col_count <= 0:
            self._column_count = 1
        if items is not None:
            self._child_widgets = items
        else:
            self._child_widgets = []

    def render(self):
        grid_type = self._ui_grid_types[self._column_count - 1]
        content = "<div class='" + grid_type + "' >\n"
        grid = self._ui_grids[self._column_count - 1]
        counter = 0
        for widget in self._child_widgets:
            if counter < self._column_count:
                block = grid[counter]
                counter += 1
            else:
                counter = 0
                block = grid[counter]
                counter += 1
            content += "<div class='" + block + "' >\n"
            content += widget.render()
            content += "</div>\n"
        content += "</div>\n"
        return content


class SectionLayout(Widget):
    """Sections build using `ui-bar` css class which help in separating the
    content like, creating an header and `ui-body` css class is used to
    render rest of the content
    """

    _header = None
    _separate_header = None
    _header_theme = None
    _body_theme = None
    _header_corners = None
    _body_corners = None

    def __init__(self, name, header, separate_header=None, header_theme=None, body_theme=None,
                 header_corners=None, body_corners=None, items=None):
        Widget.__init__(self, name)
        self._header = header
        if separate_header is not None:
            self._separate_header = separate_header
        else:
            self._separate_header = True
        self._header_theme = header_theme
        self._body_theme = body_theme
        if header_corners is not None:
            self._header_corners = header_corners
        else:
            self._header_corners = False
        if body_corners is not None:
            self._body_corners = body_corners
        else:
            self._body_corners = False
        if items is not None:
            self._child_widgets = items
        else:
            self._child_widgets = []

    def render(self):
        content = ""
        if self._separate_header:
            content = "<h3 class='ui-bar "
            if self._header_theme is not None:
                content += "ui-bar-" + self._header_theme + " "
            else:
                content += "ui-bar-a "
            if self._header_corners:
                content += "ui-corner-all'>"
            else:
                content += "'>"
            content += self._header + "</h3>\n"
        content += "<div class='ui-body "
        if self._body_theme is not None:
            content += "ui-body-" + self._body_theme + " "
        if self._body_corners:
            content += "ui-corner-all' >\n"
        else:
            content += "' >\n"
        if not self._separate_header:
            content += "<h3>" + self._header + "</h3>\n"
        for widget in self._child_widgets:
            content += widget.render() + "\n"
        content += "</div>"
        return content


class ListView(Widget, Namespace):
    """A listview is coded as a simple unordered list (ul)
    or ordered list (ol) with a data-role="listview"
    attribute and has a wide range of features.
    """

    _is_ordered = None
    _is_inset = None
    _is_filterable = None
    _is_filter_reveal = None
    _is_auto_divider_enabled = None
    _is_split_button_enabled = None
    _theme = None
    _items = None
    _disabled = None
    _hide_dividers = None
    _icon = None
    _split_icon = None
    _split_theme = None
    _namespace = None
    _socket_io = None

    def __init__(self, name, socket_io, is_ordered=None, is_inset=None, is_filterable=None,
                 is_filter_reveal=None, is_auto_divider_enabled=None, is_split_button_enabled=None,
                 theme=None, items=None, disabled=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + self._name + "_lv").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + self._name + "_lv").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._is_ordered = is_ordered
        self._is_inset = is_inset
        self._is_filterable = is_filterable
        self._is_filter_reveal = is_filter_reveal
        self._is_auto_divider_enabled = is_auto_divider_enabled
        self._is_split_button_enabled = is_split_button_enabled
        self._disabled = disabled
        if items is not None:
            self._child_widgets = items
        else:
            self._child_widgets = []

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def split_theme(self):
        return self._split_theme

    @split_theme.setter
    def split_theme(self, val):
        self._split_theme = val
        self._sync_properties('splitTheme', val)

    @property
    def split_icon(self):
        return self._split_icon

    @split_icon.setter
    def split_icon(self, val):
        self._split_icon = val
        self._sync_properties('splitIcon', val)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val
        self._sync_properties('icon', val)

    @property
    def hide_dividers(self):
        return self._hide_dividers

    @hide_dividers.setter
    def hide_dividers(self, val):
        self._hide_dividers = val
        self._sync_properties('hideDividers', val)

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def is_inset(self):
        return self._is_inset

    @is_inset.setter
    def is_inset(self, val):
        self._is_inset = val
        self._sync_properties('inset', val)

    @property
    def is_auto_divider_enabled(self):
        return self._is_auto_divider_enabled

    @is_auto_divider_enabled.setter
    def is_auto_divider_enabled(self, val):
        self._is_auto_divider_enabled = val
        self._sync_properties('autodividers', val)

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val
        self._sync_properties('theme', val)

    @property
    def is_ordered(self):
        return self._is_ordered

    @is_ordered.setter
    def is_ordered(self, val):
        self._is_ordered = val

    @property
    def is_filterable(self):
        return self._is_filterable

    @is_filterable.setter
    def is_filterable(self, val):
        self._is_filterable = val

    @property
    def is_filter_reveal(self):
        return self._is_filter_reveal

    @is_filter_reveal.setter
    def is_filter_reveal(self, val):
        self._is_filter_reveal = val

    @property
    def is_split_button_enabled(self):
        return self._is_split_button_enabled

    @is_split_button_enabled.setter
    def is_split_button_enabled(self, val):
        self._is_split_button_enabled = val

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
                                selector.listview("option", props['cmd'], props['value']);
                                selector.listview('refresh');
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name)
        return script

    def render(self):
        content = ""
        if not self._is_ordered:
            content += "<ul data-role='listview' "
        else:
            content += "<ol data-role='listview' "
        content += "id='" + self._name + "' "
        content += "style='margin-bottom: 10px;' "
        if self._is_inset:
            content += "data-inset='true' "
        if self._is_filterable:
            content += "data-filter='true' data-filter-placeholder='Search Items...' "
        if self._is_filter_reveal:
            content += "data-filter='true' data-filter-reveal='true' data-input='#" + self._name + "_auto' "
        if self._is_auto_divider_enabled:
            content += "data-autodividers='true' "
        if self._is_split_button_enabled:
            content += "data-split-icon='gear' data-split-theme='a' "
        content += ">\n"
        for widget in self._child_widgets:
            content += widget.render() + "\n"
        if not self._is_ordered:
            content += "</ul>\n"
        else:
            content += "</ol>\n" + self._attach_script()
        return content


class ListItem(Widget, Namespace):
    """An listview item which can be rendered as readonly, link or complex UI using the options
    provided by this class
    """

    _namespace = None
    _socket_io = None
    _title = None
    _content = None
    _is_read_only = None
    _is_linked = None
    _is_count_bubble_enabled = None
    _is_thumbnail_enabled = None
    _icon = None
    _is_list_divider = None
    _count = None
    _img_src = None
    _click_callback = None
    _is_active = None
    _href = None
    _data_rel = None

    def __init__(self, name, title, socket_io, content=None, is_read_only=None, is_linked=None,
                 is_count_bubble_enabled=None, is_thumbnail_enabled=None, icon=None,
                 is_list_divider=None, count=None, img_src=None, click_callback=None, is_active=None,
                 href=None, data_rel=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + self._name + "_li").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + self._name + "_li").replace('.', '_')
        self._title = title
        self._content = content
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        if is_linked is not None:
            self._is_linked = is_linked
        else:
            self._is_linked = True
        self._is_count_bubble_enabled = is_count_bubble_enabled
        self._is_thumbnail_enabled = is_thumbnail_enabled
        self._is_read_only = is_read_only
        self._icon = icon
        self._is_list_divider = is_list_divider
        self._count = count
        self._img_src = img_src
        self._click_callback = click_callback
        self._is_active = is_active
        if href is not None:
            self._href = href
        else:
            self._href = "#"
        self._data_rel = data_rel

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, val):
        self._content = val

    @property
    def is_linked(self):
        return self._is_linked

    @is_linked.setter
    def is_linked(self, val):
        self._is_linked = val

    @property
    def is_count_bubble_enabled(self):
        return self._is_count_bubble_enabled

    @is_count_bubble_enabled.setter
    def is_count_bubble_enabled(self, val):
        self._is_count_bubble_enabled = val

    @property
    def is_thumbnail_enabled(self):
        return self._is_thumbnail_enabled

    @is_thumbnail_enabled.setter
    def is_thumbnail_enabled(self, val):
        self._is_thumbnail_enabled = val

    @property
    def is_read_only(self):
        return self._is_read_only

    @is_read_only.setter
    def is_read_only(self, val):
        self._is_read_only = val

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val

    @property
    def is_list_divider(self):
        return self._is_list_divider

    @is_list_divider.setter
    def is_list_divider(self, val):
        self._is_list_divider = val

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val

    @property
    def img_src(self):
        return self._img_src

    @img_src.setter
    def img_src(self, val):
        self._img_src = val

    def on_fire_click_event(self, props):  # noqa
        if self._click_callback is not None:
            self._click_callback(self._name, props)

    def _attach_script(self):
        script = """
                <script>
                    (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');

                            selector.bind('click', function(){
                                props = {
                                        };
                                socket.emit("fire_click_event", props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name)
        return script

    def render(self):
        content = ""
        if self._is_list_divider is not None and self._is_list_divider:
            return "<li data-role='list-divider' id='" + self._name + "'>" + self._title + "</li>"
        if self._is_read_only is not None and self._is_read_only:
                return "<li id='" + self._name + "'>" + self._title + "</li>"
        else:
            if self._is_linked is not None and self._is_linked:
                if self._icon is not None:
                    content += "<li data-icon='" + self._icon + "' "
                else:
                    content += "<li "
                content += "id='" + self._name + "'>"
                content += "<a href='" + self._href + "' "
                if self._data_rel is not None:
                    content += "data-rel='" + self._data_rel + "' "
                if self._is_active is not None and self._is_active:
                    content += "class='ui-btn-active' "
                content += ">"
                if self._is_thumbnail_enabled is not None and self._is_thumbnail_enabled:
                    content += "<img src='" + self._img_src + "' />"
                    content += "<h2>" + self._title + "</h2>"
                else:
                    content += self._title
                if self._is_count_bubble_enabled is not None and self._is_count_bubble_enabled:
                    content += "<span class='ui-li-count>" + self._count + "</span>"
                content += "</a></li>\n" + self._attach_script()
                return content
        return self._content


class NavBar(Widget, Namespace):
    """A navbar consist of upto 5 items/buttons in a row, if the
    items are more than 5, the items will be wrapped across multiple
    rows with 2 items in each row
    """

    _socket_io = None
    _theme = None
    _items = None
    _namespace = None
    _is_persist = None
    _icon_pos = None
    _disabled = None
    _click_callback = None

    def __init__(self, name, socket_io, theme=None, items=None,
                 is_persist=None, icon_pos=None, click_callback=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + self._name + "_nb").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + self._name + "_nb").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._theme = theme
        self._items = items
        self._is_persist = is_persist
        self._icon_pos = icon_pos
        self._click_callback = click_callback

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, val):
        self._items = val

    @property
    def is_persist(self):
        return self._is_persist

    @is_persist.setter
    def is_persist(self, val):
        self._is_persist = val

    @property
    def icon_pos(self):
        return self._icon_pos

    @icon_pos.setter
    def icon_pos(self, val):
        self._icon_pos = val
        self._sync_properties('iconpos', val)

    def add_item(self, key, value, is_selected, href=None, icon=None, data_rel=None):
        if self._items is not None:
            self._items[key] = [value, is_selected, href, icon, data_rel]
        else:
            self._items = {}
            self._items[key] = [value, is_selected, href, icon, data_rel]

    def remove_item(self, key):
        self._items.pop(key)

    def on_fire_click_event(self, props):
        dsbld = props['disabled']
        if dsbld is not None:
            self._disabled = dsbld
        iconpos = props['iconpos']
        if iconpos is not None:
            self._icon_pos = iconpos
        clicked_item = props['clicked_item']
        if self._click_callback is not None:
            self._click_callback(clicked_item, props)

    def _sync_properties(self, cmd, value):
        emit("sync_properties_" + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def _attach_script(self):
        script = """
                <script>
                    (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');

                            socket.on('sync_properties_%s', function(props){
                                selector.navbar("option", props['cmd'], props['value']);
                                selector.navbar('refresh');
                            });

                            $('#%s a').bind('click', function(e){
                            props = {
                                        'iconpos': selector.navbar('option', 'iconpos'),
                                        'disabled': selector.navbar('option', 'disabled'),
                                        'clicked_item': e.target.id
                                     };
                                socket.emit('fire_click_event', props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name, self._name)
        return script

    def render(self):
        content = "<div data-role='navbar' id='" + self._name + "' "
        if self._icon_pos is not None:
            content += "data-iconpos='" + self._icon_pos + "' "
        content += ">\n"
        content += "<ul>\n"
        for key in self._items:
            item = self._items.get(key)
            value = item[0]
            selected = item[1]
            href = item[2] if item[2] is not None else "#"
            icon = item[3]
            data_rel = item[4]
            content += "<li><a id='" + key + "' href='" + href + "' class='"
            if selected:
                content += "ui-btn-active "
            if self._is_persist:
                content += "ui-state-persist"
            content += "' "
            if icon is not None:
                content += "data-icon='" + icon + "' "
            if data_rel is not None:
                content += "data-rel='" + data_rel + "' "
            if self._theme is not None:
                content += "data-theme='" + self._theme + "' "
            content += ">" + value + "</a></li>\n"
        content += "</ul>\n"
        content += "</div>\n" + self._attach_script()
        return content


class Panel(Widget, Namespace):
    """A panel can be shown of right or left side of the screen.
    A panel can be displayed using any pf the three transitions:
    Overlay, Reveal and Push. Visit Panel section under JQMobile site
    for more information
    """

    _namespace = None
    _socket_io = None
    _position = None
    _display = None
    _is_swipe_close = None
    _is_dismissible = None
    _show_close_btn = None  # add the data-rel='close' to the btn
    _animate = None
    _is_position_fixed = None
    _theme = None
    _before_close_callback = None
    _before_open_callback = None

    def __init__(self, name, socket_io, position=None, display=None, swipe_close=None, dismissible=None,
                 show_close_btn=None, animate=None, position_fixed=None, theme=None,
                 before_close_callback=None, before_open_callback=None, child_widgets=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + self._name + "_pnl").replace(".", "_"))
        self._namespace = '/' + str(__name__ + "_" + self._name + "_pnl").replace(".", "_")
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._position = position
        self._display = display
        self._is_swipe_close = swipe_close
        self._is_dismissible = dismissible
        self._show_close_btn = show_close_btn
        self._animate = animate
        self._is_position_fixed = position_fixed
        self._theme = theme
        if child_widgets is not None:
            self._child_widgets = child_widgets
        else:
            self._child_widgets = []
        self._before_close_callback = before_close_callback
        self._before_open_callback = before_open_callback

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val
        self._sync_properties('position', val)

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, val):
        self._display = val
        self._sync_properties('display', val)

    @property
    def is_swipe_close(self):
        return self._is_swipe_close

    @is_swipe_close.setter
    def is_swipe_close(self, val):
        self._is_swipe_close = val
        self._sync_properties('swipeClose', val)

    @property
    def is_dismissible(self):
        return self._is_dismissible

    @is_dismissible.setter
    def is_dismissible(self, val):
        self._is_dismissible = val
        self._sync_properties('dismissible', val)

    @property
    def show_close_btn(self):
        return self._show_close_btn

    @show_close_btn.setter
    def show_close_btn(self, val):
        self._show_close_btn = val

    @property
    def animate(self):
        return self._animate

    @animate.setter
    def animate(self, val):
        self._animate = val
        self._sync_properties('animate', val)

    @property
    def is_position_fixed(self):
        return self._is_position_fixed

    @is_position_fixed.setter
    def is_position_fixed(self, val):
        self._is_position_fixed = val
        self._sync_properties('positionFixed', val)

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val
        self._sync_properties('theme', val)

    def on_fire_before_close_event(self, props):
        ani = props['animate']
        if ani is not None:
            self._animate = ani
        dsbld = props['disabled']
        if dsbld is not None:
            self._display = dsbld
        dismiss = props['dismissible']
        if dismiss is not None:
            self._is_dismissible = dismiss
        dsply = props['display']
        if dsply is not None:
            self._display = dsply
        pos = props['position']
        if pos is not None:
            self._position = pos
        posFixed = props['positionFixed']
        if posFixed is not None:
            self._is_position_fixed = posFixed
        swipcls = props['swipeClose']
        if swipcls is not None:
            self._is_swipe_close = swipcls
        theme = props['theme']
        if theme is not None:
            self._theme = theme
        if self._before_close_callback is not None:
            self._before_close_callback(self._name, props)

    def on_fire_before_open_event(self, props):
        if self._before_open_callback is not None:
            self._before_open_callback(self._name, props)

    def _sync_properties(self, cmd, value):
        emit("sync_properties_" + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def _attach_script(self):
        script = """
                <script>
                    (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');

                            socket.on('sync_properties_%s', function(props){
                                selector.panel("option", props['cmd'], props['value']);
                                selector.panel('refresh');
                            });

                            selector.on('panelbeforeopen', function(e, ui){
                                var props = {
                                            };
                                socket.emit('fire_before_open_event', props);
                            });
                            selector.on('panelbeforeclose', function(e, ui){
                            var props = {
                                        'animate': selector.panel('option', 'animate'),
                                        'disabled': selector.panel('option', 'disabled'),
                                        'dismissible': selector.panel('option', 'dismissible'),
                                        'display': selector.panel('option', 'display'),
                                        'position': selector.panel('option', 'position'),
                                        'positionFixed': selector.panel('option', 'positionFixed'),
                                        'swipeClose': selector.panel('option', 'swipeClose'),
                                        'theme': selector.panel('option', 'theme')
                                     }
                                socket.emit('fire_before_close_event', props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name)
        return script

    def render(self):
        content = ""
        content += "<div data-role='panel' id='" + self._name + "' "
        if self._position is not None:
            content += "data-position='" + self._position + "' "
        if self._display is not None:
            content += "data-display='" + self._display + "' "
        if self._is_position_fixed is not None:
            content += "data-position-fixed='" + json.dumps(self._is_position_fixed) + "' "
        if self._is_swipe_close is not None:
            content += "data-swipe-close='" + json.dumps(self._is_swipe_close) + "' "
        if self._is_dismissible is not None:
            content += "data-dismissible='" + json.dumps(self._is_dismissible) + "' "
        if self._animate is not None:
            content += "data-animate='" + self._animate + "' "
        if self._theme is not None:
            content += "data-theme='" + self._theme + "' "
        content += ">\n"
        for widget in self._child_widgets:
            content += widget.render() + "\n"
        if self._show_close_btn is not None and self._show_close_btn:
            content += "<a class='ui-btn' href='#' data-rel='close'>Close</a>\n"
        content += "</div>\n" + self._attach_script()
        return content


class Popup(Widget, Namespace):
    """The popup widget can be used for various types of popups.
    From a small tooltip popup to a large photo lightbox.
    """

    _namespace = None
    _socket_io = None
    _style_class = None
    _theme = None
    _overlay_theme = None
    _corners = None
    _is_dismissible = None
    _height = None
    _width = None
    _is_arrow_visible = None
    _show_close_button = None
    _close_btn_position = None
    _after_close_callback = None
    _after_open_callback = None
    _disabled = None
    _positionTo = None
    _shadow = None
    _tolerance = None
    _transition = None

    def __init__(self, name, socket_io, style_class=None, theme=None, overlay_theme=None,
                 corners=None, is_dismissible=None, height=None, width=None, is_arrow_visible=None,
                 child_widgets=None, show_close_button=None, close_btn_position=None,
                 after_close_callback=None, after_open_callback=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + self._name + "_popup").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + self._name + "_popup").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._style_class = style_class
        self._theme = theme
        self._overlay_theme = overlay_theme
        self._corners = corners
        self._is_dismissible = is_dismissible
        self._height = height
        self._width = width
        self._is_arrow_visible = is_arrow_visible
        if child_widgets is not None:
            self._child_widgets = child_widgets
        else:
            self._child_widgets = []
        if show_close_button is not None:
            self._show_close_button = show_close_button
        else:
            self._show_close_button = False
        if close_btn_position is not None:
            self._close_btn_position = close_btn_position
        else:
            self._close_btn_position = "right"
        self._after_open_callback = after_open_callback
        self._after_close_callback = after_close_callback

    @property
    def style_class(self):
        return self._style_class

    @style_class.setter
    def style_class(self, val):
        self._style_class = val

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val
        self._sync_properties('theme', val)

    @property
    def overlay_theme(self):
        return self._overlay_theme

    @overlay_theme.setter
    def overlay_theme(self, val):
        self._overlay_theme = val
        self._sync_properties('overlayTheme', val)

    @property
    def corners(self):
        return self._corners

    @corners.setter
    def corners(self, val):
        self._corners = val
        self._sync_properties('corners', val)

    @property
    def is_dismissible(self):
        return self._is_dismissible

    @is_dismissible.setter
    def is_dismissible(self, val):
        self._is_dismissible = val
        self._sync_properties('dismissible', val)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def is_arrow_visible(self):
        return self._is_arrow_visible

    @is_arrow_visible.setter
    def is_arrow_visible(self, val):
        self._is_arrow_visible = val
        self._sync_properties('arrow', val)

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def positionTo(self):
        return self._positionTo

    @positionTo.setter
    def positionTo(self, val):
        self._positionTo = val
        self._sync_properties('positionTo', val)

    @property
    def shadow(self):
        return self._shadow

    @shadow.setter
    def shadow(self, val):
        self._shadow = val
        self._sync_properties('shadow', val)

    @property
    def tolerance(self):
        return self._tolerance

    @tolerance.setter
    def tolerance(self, val):
        self._tolerance = val
        self._sync_properties('tolerance', val)

    @property
    def transition(self):
        return self._transition

    @transition.setter
    def transition(self, val):
        self._transition = val
        self._sync_properties('transition', val)

    @property
    def show_close_button(self):
        return self._show_close_button

    @show_close_button.setter
    def show_close_button(self, val):
        self._show_close_button = val

    @property
    def close_btn_position(self):
        return self._close_btn_position

    @close_btn_position.setter
    def close_btn_position(self, val):
        self._close_btn_position = val

    def on_fire_after_close_event(self, props):
        theme = props['theme']
        if theme is not None:
            self._theme = theme
        overlay_theme = props['overlayTheme']
        if overlay_theme is not None:
            self._overlay_theme = overlay_theme
        corners = props['corners']
        if corners is not None:
            self._corners = corners
        is_dismissible = props['dismissible']
        if is_dismissible is not None:
            self._is_dimissible = is_dismissible
        is_arrow_visible = props['arrow']
        if is_arrow_visible is not None:
            self._is_arrow_visibale = is_arrow_visible
        disabled = props['disabled']
        if disabled is not None:
            self._disabled = disabled
        positionTo = props['positionTo']
        if positionTo is not None:
            self._positionTo = positionTo
        shadow = props['shadow']
        if shadow is not None:
            self._shadow = shadow
        tolerance = props['tolerance']
        if tolerance is not None:
            self._tolerance = tolerance
        transition = props['transition']
        if transition is not None:
            self._transition = transition
        if self._after_close_callback is not None:
            self._after_close_callback(self._name, props)

    def on_fire_after_open_event(self, props):
        theme = props['theme']
        if theme is not None:
            self._theme = theme
        overlay_theme = props['overlayTheme']
        if overlay_theme is not None:
            self._overlay_theme = overlay_theme
        corners = props['corners']
        if corners is not None:
            self._corners = corners
        is_dismissible = props['dismissible']
        if is_dismissible is not None:
            self._is_dimissible = is_dismissible
        is_arrow_visible = props['arrow']
        if is_arrow_visible is not None:
            self._is_arrow_visibale = is_arrow_visible
        disabled = props['disabled']
        if disabled is not None:
            self._disabled = disabled
        positionTo = props['positionTo']
        if positionTo is not None:
            self._positionTo = positionTo
        shadow = props['shadow']
        if shadow is not None:
            self._shadow = shadow
        tolerance = props['tolerance']
        if tolerance is not None:
            self._tolerance = tolerance
        transition = props['transition']
        if transition is not None:
            self._transition = transition
        if self._after_open_callback is not None:
            self._after_open_callback(self._name, props)

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
                                selector.popup('option', props['cmd'], props['value']);
                            });

                            selector.on('popupafterclose', function(){
                            var props = {'arrow': selector.popup('option', 'arrow'),
                                         'disabled': selector.popup('option', 'disabled'),
                                         'positionTo': selector.popup('option', 'positionTo'),
                                         'shadow': selector.popup('option', 'shadow'),
                                         'tolerance': selector.popup('option', 'tolerance'),
                                         'transition': selector.popup('option', 'transition'),
                                         'theme': selector.popup('option', 'theme'),
                                         'overlayTheme': selector.popup('option', 'overlayTheme'),
                                         'corners': selector.popup('option', 'corners'),
                                         'dismissible': selector.popup('option', 'dismissible')
                                        };
                                socket.emit('fire_after_close_event', props);
                            });

                            selector.on('popupafteropen', function(){
                            var props = {'arrow': selector.popup('option', 'arrow'),
                                         'disabled': selector.popup('option', 'disabled'),
                                         'positionTo': selector.popup('option', 'positionTo'),
                                         'shadow': selector.popup('option', 'shadow'),
                                         'tolerance': selector.popup('option', 'tolerance'),
                                         'transition': selector.popup('option', 'transition'),
                                         'theme': selector.popup('option', 'theme'),
                                         'overlayTheme': selector.popup('option', 'overlayTheme'),
                                         'corners': selector.popup('option', 'corners'),
                                         'dismissible': selector.popup('option', 'dismissible')
                                        };
                                socket.emit('fire_after_open_event', props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name)
        return script

    def render(self):  # noqa
        content = ""
        content += "<div data-role='popup' "
        content += "id='" + self._name + "' "
        if self._style_class is not None:
            content += "class='ui-content " + self._style_class + "' "
        else:
            content += "class='ui-content' "
        if self._theme is not None:
            content += "data-theme='" + self._theme + "' "
        if self._overlay_theme is not None:
            content += "data-overlay-theme='" + self._overlay_theme + "' "
        if self._corners is not None:
            content += "data-corners='" + json.dumps(self._corners) + "' "
        if self._is_dismissible is not None:
            content += "data-dismissible='" + json.dumps(self._is_dismissible) + "' "
        if self._is_arrow_visible is not None:
            content += "data-arrow='" + self._is_arrow_visible + "' "
        if self._height is not None and self._width is not None:
            content += "style='max-width:" + self._width + ", max-height: " + self._height + "' "
        elif self._height is None and self._width is not None:
            content += "style='max-width:" + self._width + "' "
        elif self._height is not None and self._width is None:
            content += "style='max-height: " + self._height + "' "
        content += ">"
        for widget in self._child_widgets:
            content += widget.render() + "\n"
        if self._show_close_button is not None:
            if self._close_btn_position is not None and self._close_btn_position == "right":
                content += "<a href='#' data-rel='back' class='ui-btn ui-corner-all ui-shadow ui-btn-a\
                 ui-icon-delete ui-btn-icon-notext ui-btn-right'>Close</a>"
            if self._close_btn_position is not None and self._close_btn_position == "left":
                content += "<a href='#' data-rel='back' class='ui-btn ui-corner-all ui-shadow ui-btn-a\
                 ui-icon-delete ui-btn-icon-notext ui-btn-left'>Close</a>"
        content += "</div>" + "\n" + self._attach_script()
        return content


class HTML(Widget):
    """Widget to render html on a mobile page. The HTML can be passed
    as argument to constructor or can be assigned to `html` property.
    Apart from that you can pass CSS script which will be rendered
    before HTML is rendered on page.
    """

    _html = None
    _css = None

    def __init__(self, name, html=None, child_widgets=None, css=None):
        Widget.__init__(self, name)
        self._html = html
        self._css = css
        if child_widgets is not None:
            self._child_widgets = child_widgets
        else:
            self._child_widgets = []

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, val):
        self._html = val

    @property
    def css(self):
        return self._css

    @css.setter
    def css(self, val):
        self._css = val

    def render(self):
        content = ""
        if self._css is not None:
            content += "<style>" + "\n"
            content += self._css + "\n"
            content += "</style>"
        if self._html is not None:
            content += "<div id='" + self._name + "'>"
            content += self._html + "\n"
        if self._child_widgets is not None:
            for widget in self._child_widgets:
                content += widget.render() + "\n"
        if self._html is not None:
            content += "</div>"
        return content


class JavaScript(Widget):
    """Renders the javascript in executionable container. The script
    will be executed on `pagecreate` event, so that it have access to
    DOM object of JQMobile widgets
    """

    _js = None

    def __init__(self, name, js=None):
        Widget.__init__(self, name)
        self._js = js

    @property
    def javascript(self):
        return self._js

    @javascript.setter
    def javascript(self, val):
        self._js = val

    def render(self):
        js = """<script>
                (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            %s
                        });
                    })(jQuery);
                </script>
            """ % (self._js)
        return js


class RangeSlider(Widget, Namespace):
    """Range slider offer two handles to set a min
    and max value along a numeric continuum.
    """

    _title1 = None
    _title2 = None
    _value1 = None
    _value2 = None
    _value1min = None
    _value1max = None
    _value2min = None
    _value2max = None
    _step1 = None
    _step2 = None
    _namespace = None
    _socket_io = None
    _highlight = None
    _theme = None
    _track_theme = None
    _mini = None
    _disabled = None
    _value_changed_callback = None

    def __init__(self, name, socket_io, title1=None, title2=None, value1=None, value2=None,
                 value1min=None, value1max=None, value2min=None, value2max=None, step1=None,
                 step2=None, highlight=None, theme=None, track_theme=None, mini=None,
                 disabled=None, value_changed_callback=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + '_' + self._name + '_rs').replace('.', '_'))
        self._namespace = '/' + str(__name__ + '_' + self._name + '_rs').replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        if title1 is not None:
            self._title1 = title1
        else:
            self._title1 = ""
        if title2 is not None:
            self._title2 = title2
        else:
            self._title2 = ""
        if value1 is not None:
            self._value1 = value1
        else:
            self._value1 = 0
        if value2 is not None:
            self._value2 = value2
        else:
            self._value2 = 100
        if value1min is not None:
            self._value1min = value1min
        else:
            self._value1min = 0
        if value1max is not None:
            self._value1max = value1max
        else:
            self._value1max = 100
        if value2min is not None:
            self._value2min = value2min
        else:
            self._value2min = 0
        if value2max is not None:
            self._value2max = value2max
        else:
            self._value2max = 100
        self._step1 = step1
        self._step2 = step2
        self._highlight = highlight
        self._theme = theme
        self._track_theme = track_theme
        self._mini = mini
        self._disabled = disabled
        self._value_changed_callback = value_changed_callback

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties('disabled', val)

    @property
    def highlight(self):
        return self._highlight

    @highlight.setter
    def highlight(self, val):
        self._highlight = val
        self._sync_properties('highlight', val)

    @property
    def mini(self):
        return self._mini

    @mini.setter
    def mini(self, val):
        self._mini = val
        self._sync_properties('mini', val)

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, val):
        self._theme = val
        self._sync_properties('theme', val)

    @property
    def track_theme(self):
        return self._track_theme

    @track_theme.setter
    def track_theme(self, val):
        self._track_theme = val
        self._sync_properties('trackTheme', val)

    def on_value_changed_event(self, callback):
        self._value_changed_callback = callable

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def on_fire_change_event(self, props):
        dsbld = props['disabled']
        if dsbld is not None:
            self._disabled = dsbld
        highlight = props['highlight']
        if highlight is not None:
            self._highlight = highlight
        mini = props['mini']
        if mini is not None:
            self._mini = mini
        theme = props['theme']
        if theme is not None:
            self._theme = theme
        trackTheme = props['trackTheme']
        if trackTheme is not None:
            self._track_theme = trackTheme
        val1 = props['value1']
        if val1 is not None:
            self._value1 = val1
        val2 = props['value2']
        if val2 is not None:
            self._value2 = val2
        if self._value_changed_callback is not None:
            self._value_changed_callback(self._name, props)

    def _attach_script(self):
        script = """
                <script>
                    (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');
                            var input1 = $('#%s1');
                            var input2 = $('#%s2');

                            socket.on('sync_properties_%s', function(props){
                                selector.rangeslider("option", props['cmd'], props['value']);
                                selector.rangeslider('refresh');
                            });

                            selector.bind('change', function(e){
                                var props = {
                                            'disabled': selector.rangeslider('option', 'disabled'),
                                            'highlight': selector.rangeslider('option', 'highlight'),
                                            'mini': selector.rangeslider('option', 'mini'),
                                            'theme': selector.rangeslider('option', 'theme'),
                                            'trackTheme': selector.rangeslider('option', 'trackTheme'),
                                            'value1': input1.val(),
                                            'value2': input2.val()
                                };
                                socket.emit('fire_change_event', props);
                            });
                        });
                    })(jQuery);
                </script>
                """ % (self._namespace, self._name, self._name, self._name, self._name)
        return script

    def render(self):
        content = ""
        content += "<div data-role='rangeslider' id='" + self._name + "' "
        if self._highlight is not None:
            content += "data-highlight='" + json.dumps(self._highlight) + "' "
        if self._theme is not None:
            content += "data-theme='" + self._theme + "' "
        if self._track_theme is not None:
            content += "data-track-theme='" + self._track_theme + "' "
        if self._mini is not None:
            content += "data-mini='" + json.dumps(self._mini) + "' "
        content += ">\n"
        content += "<label for='" + self._name + "1' >" + self._title1 + "</label>\n"
        content += "<input type='range' id='" + self._name + "1' min='" + str(self._value1min)\
            + "' max='" + str(self._value1max) + "' value='" + str(self._value1) + "' "
        if self._step1 is not None:
            content += "step='" + str(self._step1) + "' "
        if self._disabled is not None and self._disabled:
            content += "disabled='disabled' "
        content += ">\n"
        content += "<label for='" + self._name + "2' >" + self._title2 + "</label>\n"
        content += "<input type='range' id='" + self._name + "2' min='" + str(self._value2min)\
            + "' max='" + str(self._value2max) + "' value='" + str(self._value2) + "' "
        if self._step2 is not None:
            content += "step='" + self._step2 + "' "
        if self._disabled is not None and self._disabled:
            content += "disabled='disabled' "
        content += ">\n"
        content += "</div> \n" + self._attach_script()
        return content


class SelectMenu(Widget, Namespace):
    """The select menu is based on a native select element, which is hidden from view and
    replaced with a custom-styled select button that matches the look and feel of the jQuery
    Mobile framework

    Options is a dict with values as sub dict. Framework takes care of creatin these dict objects
    once the `add_option` is called with required parameters...
    {'option_value': '', 'option_title': '', 'selected': '', 'disabled': '', 'opt_group': ''}

    """

    _namespace = None
    _socket_io = None
    _close_text = None
    _corners = None
    _disabled = None
    _divider_theme = None
    _hide_placeholder_menuitems = None
    _icon = None
    _icon_pos = None
    _icon_shadow = None
    _inline = None
    _mini = None
    _native_menu = None
    _overlay_theme = None
    _shadow = None
    _theme = None
    _options = None
    _multiple = None
    _click_callback = None
    _selected_value = None

    def __init__(self, name, socket_io, close_text=None, corners=None, disabled=None, divider_theme=None,
                 hide_placeholder_menuitems=None, icon=None, icon_pos=None, icon_shadow=None, inline=None,
                 mini=None, native_menu=None, overlay_theme=None, shadow=None, theme=None, options=None,
                 multiple=None, click_callback=None, selected_value=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, '/' + str(__name__ + "_" + self._name + "_sel").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + self._name + "_sel").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._close_text = close_text
        self._corners = corners
        self._disabled = disabled
        self._divider_theme = divider_theme
        self._hide_placeholder_menuitems = hide_placeholder_menuitems
        self._icon = icon
        self._icon_pos = icon_pos
        self._icon_shadow = icon_shadow
        self._inline = inline
        self._mini = mini
        self._native_menu = native_menu
        self._overlay_theme = overlay_theme
        self._shadow = shadow
        self._theme = theme
        self._multiple = multiple
        if options is not None:
            self._options = options
        else:
            self._options = []
        self._click_callback = click_callback
        self._selected_value = selected_value

    @property
    def selected_value(self):
        return self._selected_value

    @selected_value.setter
    def selected_value(self, val):
        self._selected_value = val
        self._sync_properties('selectedValue', val)

    @property
    def close_text(self):
        return self._close_text

    @close_text.setter
    def close_text(self, val):
        self._close_text = val
        self._sync_properties('closeText', val)

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
    def divider_theme(self):
        return self._divider_theme

    @divider_theme.setter
    def divider_theme(self, val):
        self._divider_theme = val
        self._sync_properties('dividerTheme', val)

    @property
    def hide_placeholder_menuitems(self):
        return self._hide_placeholder_menuitems

    @hide_placeholder_menuitems.setter
    def hide_placeholder_menuitems(self, val):
        self._hide_placeholder_menuitems = val
        self._sync_properties('hidePlaceholderMenuItems', val)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val
        self._sync_properties('icon', val)

    @property
    def icon_pos(self):
        return self._icon_pos

    @icon_pos.setter
    def icon_pos(self, val):
        self._icon_pos = val
        self._sync_properties('iconpos', val)

    @property
    def icon_shadow(self):
        return self._icon_shadow

    @icon_shadow.setter
    def icon_shadow(self, val):
        self._icon_shadow = val
        self._sync_properties('iconshadow', val)

    @property
    def inline(self):
        return self._inline

    @inline.setter
    def inline(self, val):
        self._inline = val
        self._sync_properties('inline', val)

    @property
    def mini(self):
        return self._mini

    @mini.setter
    def mini(self, val):
        self._mini = val
        self._sync_properties('mini', val)

    @property
    def native_menu(self):
        return self._native_menu

    @native_menu.setter
    def native_menu(self, val):
        self._native_menu = val
        self._sync_properties('nativeMenu', val)

    @property
    def overlay_theme(self):
        return self._overlay_theme

    @overlay_theme.setter
    def overlay_theme(self, val):
        self._overlay_theme = val
        self._sync_properties('overlayTheme', val)

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
    def multiple(self):
        return self._multiple

    @multiple.setter
    def multiple(self, val):
        self._multiple = val

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def add_option(self, option_value, option_title=None, selected=False, disabled=False, opt_group=None):
        option = {}
        option['option_value'] = option_value
        if option_title is None:
            option['option_title'] = option_value
        else:
            option['option_title'] = option_title
        option['selected'] = selected
        option['disabled'] = disabled
        option['opt_group'] = opt_group
        self._options.append(option)

    def remove(self, option):
        self._options.remove(option)

    def on_fire_click_event(self, props):
        close_text = props['closeText']
        if close_text is not None:
            self._close_text = close_text
        corners = props['corners']
        if corners is not None:
            self._corners = corners
        disabled = props['disabled']
        if disabled is not None:
            self._disabled = disabled
        divider_theme = props['dividerTheme']
        if divider_theme is not None:
            self._divider_theme = divider_theme
        hide_placeholder_menuitems = props['hidePlaceholderMenuItems']
        if hide_placeholder_menuitems is not None:
            self._hide_placeholder_menuitems = hide_placeholder_menuitems
        icon = props['icon']
        if icon is not None:
            self._icon = icon
        icon_pos = props['iconpos']
        if icon_pos is not None:
            self._icon_pos = icon_pos
        icon_shadow = props['iconshadow']
        if icon_shadow is not None:
            self._icon_shadow = icon_shadow
        inline = props['inline']
        if inline is not None:
            self._inline = inline
        mini = props['mini']
        if mini is not None:
            self._mini = mini
        native_menu = props['nativeMenu']
        if native_menu is not None:
            self._native_menu = native_menu
        overlay_theme = props['overlayTheme']
        if overlay_theme is not None:
            self._overlay_theme = overlay_theme
        shadow = props['shadow']
        if shadow is not None:
            self._shadow = shadow
        theme = props['theme']
        if theme is not None:
            self._theme = theme
        selected_val = props['selectedValue']
        if selected_val is not None:
            self._selected_value = selected_val
        if self._click_callback is not None:
            self._click_callback(self._name, props)

    def _attach_script(self):
        script = """
                    <script>
                    (function($, undefined){
                        $(document).bind('pagecreate', function(e){
                            var socket = io('%s');
                            var selector = $('#%s');

                            selector.bind('click', function(e){
                                var props = {
                                                'closeText': selector.selectmenu('option', 'closeText'),
                                                'corners': selector.selectmenu('option', 'corners'),
                                                'disabled': selector.selectmenu('option', 'disabled'),
                                                'dividerTheme': selector.selectmenu('option', 'dividerTheme'),
                                                'hidePlaceholderMenuItems': selector.selectmenu('option', 'hidePlaceholderMenuItems'),
                                                'icon': selector.selectmenu('option', 'icon'),
                                                'iconpos': selector.selectmenu('option', 'iconpos'),
                                                'iconshadow': selector.selectmenu('option', 'iconshadow'),
                                                'inline': selector.selectmenu('option', 'inline'),
                                                'mini': selector.selectmenu('option', 'mini'),
                                                'nativeMenu': selector.selectmenu('option', 'nativeMenu'),
                                                'overlayTheme': selector.selectmenu('option', 'overlayTheme'),
                                                'shadow': selector.selectmenu('option', 'shadow'),
                                                'theme': selector.selectmenu('option', 'theme'),
                                                'selectedValue': selector.val()
                                };
                                socket.emit('fire_click_event', props);
                            });

                            socket.on('sync_properties_%s', function(props){
                                if(props['cmd'] == 'selectedValue'){
                                    selector.val(props['value']);
                                } else {
                                    selector.selectmenu('option', props['cmd'], props['value']);
                                }
                                selector.selectmenu('refresh');
                            });
                        });
                    })(jQuery);
                    </script>
                """ % (self._namespace, self._name, self._name)
        return script

    def render(self):  # noqa
        content = ""
        content += "<select id='" + self._name + "' "
        if self._mini is not None:
            content += "data-mini='" + json.dumps(self._mini) + "' "
        if self._icon_pos is not None:
            content += "data-iconpos='" + self._icon_pos + "' "
        if self._multiple is not None and self._multiple:
            content += "multiple "
        if self._close_text is not None:
            content += "data-close-text='" + self._close_text + "' "
        if self._corners is not None:
            content += "data-corners='" + json.dumps(self._corners) + "' "
        if self._disabled is not None:
            content += "data-disabled='" + json.dumps(self._disabled) + "' "
        if self._divider_theme is not None:
            content += "data-divider-theme='" + self._divider_theme + "' "
        if self._hide_placeholder_menuitems is not None:
            content += "data-hide-placeholder-menu-items='"\
                       + json.dumps(self._hide_placeholder_menuitems) + "' "
        if self._icon is not None:
            content += "data-icon='" + self._icon + "' "
        if self._icon_shadow is not None:
            content += "data-icon-shadow='" + json.dumps(self._icon_shadow) + "' "
        if self._inline is not None:
            content += "data-inline='" + json.dumps(self._inline) + "' "
        if self._native_menu is not None:
            content += "data-native-menu='" + json.dumps(self._native_menu) + "' "
        if self._overlay_theme is not None:
            content += "data-overlay-theme='" + self._overlay_theme + "' "
        if self._shadow is not None:
            content += "data-shadow='" + json.dumps(self._overlay_theme) + "' "
        if self._theme is not None:
            content += "data-theme='" + self._theme + "' "
        content += ">"
        opt_groups = {}
        for option in self._options:
            if option['opt_group'] is None:
                if opt_groups.get('None') is None:
                    opt_groups['None'] = []
                    opt_groups['None'].append(option)
                else:
                    opt_groups['None'].append(option)
            else:
                if opt_groups.get(option['opt_group']) is None:
                    opt_groups[option['opt_group']] = []
                    opt_groups[option['opt_group']].append(option)
                else:
                    opt_groups[option['opt_group']].append(option)
        opt_text = ""
        for option in opt_groups:
            if option == 'None':
                option_list = opt_groups.get('None')
                for opt in option_list:
                    opt_text += "<option value='" + opt['option_value'] + "' "
                    if opt['selected']:
                        opt_text += "selected='selected' "
                    if opt['disabled']:
                        opt_text += "disabled='disabled' "
                    opt_text += ">" + opt['option_title'] + "</option>\n"
            else:
                option_list = opt_groups.get(option)
                opt_text += "<optgroup label='" + option + "'>\n"
                for opt in option_list:
                    opt_text += "<option value='" + opt['option_value'] + "' "
                    if opt['selected']:
                        opt_text += "selected='selected' "
                    if opt['disabled']:
                        opt_text += "disabled='disabled' "
                    opt_text += ">" + opt['option_title'] + "</option>\n"
                opt_text += "</optgroup>\n"
        content += opt_text
        content += "</select>\n" + self._attach_script()
        return content
