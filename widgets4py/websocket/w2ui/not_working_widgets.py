

class Popup(Widget, Namespace):
    """The `Popup` class allows you to create different types of dialogs and
    it can fuether configured to your needs using many attributes which belongs
    to this class
    """

    _title = None
    _body = None
    _buttons = None
    _modal = None
    _width = None
    _height = None
    _color = None
    _opacity = None
    _speed = None
    _transition = None
    _show_close = None
    _show_max = None
    _keyboard = None

    _on_open_callback = None
    _on_close_callback = None
    _on_max_callback = None
    _on_min_callback = None
    _on_toggle_callback = None
    _on_keydown_callback = None
    _namespace = None
    _socket_io = None

    def __init__(self, name, socket_io, title=None, body=None, buttons=None,
                 modal=None, width=None, height=None,
                 color=None, opacity=None, speed=None, transition=None,
                 show_close=None, show_max=None, keyboard=None,
                 on_open_callback=None, on_close_callback=None,
                 on_max_callback=None, on_min_callback=None,
                 on_toggle_callback=None, on_keydown_callback=None,
                 desc=None):
        """
            Args:
                name (string, required): A unique identifier for the current object
                socket_io (SocketIO): An instance of the SocketIO class
                title (string): Title of the popup box
                body (string): The text to be displayed in the body of Popup. It can
                                be an HTML script also to display formatted text
                buttons (string): An HTML string consisting of HTML input tag of type
                                Button. In line, javascript can also be provided in the
                                string
                modal (boolean): Whether the popup should be opened as modal or not
                width (int): Width of the popup box
                height (int): Height of the popup box
                color (string): An string having color name or hex value of color
                opacity (float): The background opacity in decimal format
                speed (int): The speed by which animation should run if specified
                transistion (string): An transistion to use while opening or closing popup
                show_close (boolean): Whether to show close button on top right corner
                show_max (boolean): Whether to show max button on top right corner of popup
                keyboard (boolean): Whether to enable keyboard interaction
                on_open_callback (callable): Will be executed on popup open event
                on_close_callback (callable): Executes on close event of popup
                on_max_callback (callable): Executes on maximize event of popup
                on_min_callback (callable): Executes on minimize event of popup
                on_toggle_callback (callable): Executes when popup's state is toggled
                on_keydown_callback (callable): Executes on key pressed event on popup
                desc (string, optional): description of the button widget
        """
        Widget.__init__(self, name, desc=desc)
        Namespace.__init__(self, '/' + str(__name__ + str(name) + "_popup").replace('.', '_'))
        self._namespace = '/' + str(__name__ + str(name) + "_popup").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._title = title
        self._body = body
        self._buttons = buttons
        self._modal = modal
        self._width = width
        self._height = height
        self._color = color
        self._opacity = opacity
        self._speed = speed
        self._transition = transition
        self._show_close = show_close
        self._show_max = show_max
        self._keyboard = keyboard
        self._on_open_callback = on_open_callback
        self._on_close_callback = on_close_callback
        self._on_max_callback = on_max_callback
        self._on_min_callback = on_min_callback
        self._on_toggle_callback = on_toggle_callback
        self._on_keydown_callback = on_keydown_callback

    def on_fire_open_event(self):
        if self._on_open_callback is not None:
            self._on_open_callback()

    def on_fire_close_event(self):
        if self._on_close_callback is not None:
            self._on_close_callback()

    def on_fire_max_event(self):
        if self._on_max_callback is not None:
            self._on_max_callback()

    def on_fire_min_event(self):
        if self._on_min_callback is not None:
            self._on_min_callback()

    def on_fire_toggle_event(self):
        if self._on_toggle_callback is not None:
            self._on_toggle_callback()

    def on_fire_keydown_event(self):
        if self._on_keydown_callback is not None:
            return self._on_keydown_callback()

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def title(self):
        """Title of the popup box"""
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def body(self):
        """Body section of the popup"""
        return self._body

    @body.setter
    def body(self, val):
        self._body = val

    def open(self):
        """Opens the dialogbox or popup on screen"""
        self._sync_properties('OPEN')

    def load(self, url):
        """Opens the popup and displays the content loaded from url"""
        self._sync_properties('LOAD', url)

    def close(self):
        """Closes the already opened popup"""
        self._sync_properties('CLOSE')

    def lock(self, message, showSpinner=False):
        """Locks the dialogbox using an overlay and shows the spinner if set to True
        """
        self._sync_properties('LOCK', message, json.dumps(showSpinner))

    def lock_screen(self, options=None):
        """Locks the whole screen using the overlay"""
        self._sync_properties('LOCK-SCREEN', options)

    def max(self):
        """Maximize the popup window"""
        self._sync_properties('MAX')

    def min(self):
        """Minimizes the popup window"""
        self._sync_properties('MIN')

    def message(self, options=None):
        """Shows an message in the popup box

            Example:
                message({'height':200, 'width': 200, 'html': '<span>Some message</span>}')
        """
        self._sync_properties('MSG', json.dumps(options))

    def resize(self, height, width, callback=None):
        """Resize the popup to desired size and calls the callback"""
        if callback is not None:
            self._sync_properties('RESIZE', width, height, json.dumps(callback))
        else:
            self._sync_properties('RESIZE', width, height)

    def unlock(self):
        """Unlocks the locked popup"""
        self._sync_properties('UNLOCK')

    def unlock_screen(self):
        """Unlocks the whole screen"""
        self._sync_properties('UNLOCK-SCREEN')

    def _sync_properties(self, cmd, value=None, value1=None, value2=None):
        emit('sync_properties_' + self._name,
             {'cmd': cmd, 'value': value, 'value1': value1, 'value2': value2},
             namespace=self._namespace)

    def _attach_script(self):
        script = """<script>
                    $2(document).ready(function(){
                        var socket = io('%s');
                        function %s_popup(){
                                w2popup.open({
                                    title: '%s',
                                    body: '%s',
                                    buttons: '%s',
                                    width: %d,
                                    height: %d,
                                    color: '%s',
                                    speed: '%s',
                                    opacity: '%s',
                                    modal: %s,
                                    showClose: %s,
                                    showMax: %s,
                                    onOpen: function(event){
                                        socket.emit('fire_open_event');
                                    },
                                    onClose: function(event){
                                        socket.emit('fire_close_event');
                                    },
                                    onMax: function(event){
                                        socket.emit('fire_max_event');
                                    },
                                    onMin: function(event){
                                        socket.emit('fire_min_event');
                                    },
                                    onKeydown: function(event){
                                        socket.emit('fire_keydown_event');
                                    }
                                });
                            }
                        socket.on('sync_properties_%s', function(props){
                            if(props.cmd != undefined){
                                if(props.cmd == "OPEN"){
                                    %s_popup();
                                }
                                if(props.cmd == "CLOSE"){
                                    w2popup.close();
                                }
                                if(props.cmd == "LOAD"){
                                    w2popup.load({url: props.value});
                                }
                                if(props.cmd == "LOCK"){
                                    w2popup.lock(props.value, props.value1);
                                }
                                if(props.cmd == "LOCK-SCREEN"){
                                    w2popup.lockScreen(props.value);
                                }
                                if(props.cmd == "MAX"){
                                    w2popup.max();
                                }
                                if(props.cmd == "MIN"){
                                    w2popup.min();
                                }
                                if(props.cmd == "MSG"){
                                    w2popup.message(JSON.parse(props.value));
                                }
                                if(props.cmd == "RESIZE"){
                                    if(props.value2 == null){
                                        w2popup.resize(props.value, props.value1);
                                        }
                                    else{
                                        w2popup.resize(props.value, props.value1, props.value2);
                                    }
                                }
                                if(props.cmd == "UNLOCK"){
                                    w2popup.unlock();
                                }
                                if(props.cmd == "UNLOCK-SCREEN"){
                                    w2popup.unlockScreen();
                                }
                            } else {
                                alertify.warning("No command to process");
                            }
                        });
                    });
                    </script>
                """ % (self._namespace, self._name,
                       self._title if self._title is not None else '',
                       self._body if self._body is not None else '',
                       self._buttons if self._buttons is not None else '',
                       self._width if self._width is not None else 400,
                       self._height if self._height is not None else 300,
                       self._color if self._color is not None else '#333',
                       self._speed if self._speed is not None else '0.3',
                       self._opacity if self._opacity is not None else '0.8',
                       json.dumps(self._modal) if self._modal is not None else json.dumps(False),
                       json.dumps(self._show_close) if self._show_close is not None else json.dumps(False),
                       json.dumps(self._show_max) if self._show_max is not None else json.dumps(False),
                       self._name, self._name)
        return script

    def render(self):
        """Renders the popup as HTML"""
        content = ""
        content += self._attach_script()
        self._widget_content = content
        return content


# class WidgetContextMenu(Widget):
#     """Displays a context menu for a given widget whenever it is clicked.
#     Please note that it is not like normal context menu which appears on
#     right mouse click on a field, rather it appears when left button of
#     mouse is clicked on an widget
#     """

#     _spinner = None
#     _search = None
#     _match = None
#     _align = None  # values can be: None, left, right, both
#     _open_above = None
#     _alt_rows = None
#     _index = None
#     _msg_no_items = None
#     _onselect_callback = None
#     _app = None
#     _items = None

#     def __init__(self, name, items=None, spinner=None, search=None, match=None,
#                  alt_rows=None, index=None, msg_no_items=None, align=None,
#                  open_above=None, onselect_callback=None, app=None):
#         Widget.__init__(self, name)
#         if items is not None:
#             self.items = items
#         else:
#             self._items = []
#         self._spinner = spinner
#         self._search = search
#         self._match = match
#         self._align = align
#         self._open_above = open_above
#         self._alt_rows = alt_rows
#         self._index = index
#         self._msg_no_items = msg_no_items
#         self._onselect_callback
#         self._app = app

#     def add_item(self, id, text, icon=None):
#         item = "{id: '" + id + "',text: '" + text + "', "
#         if icon is not None:
#             item += "icon: '" + icon + "'"
#         item += "}"
#         self._items.append(item)

#     def _process_onselect_callback(self):
#         if self._onselect_callback is not None:
#             return json.dumps({'result': self._onselect_callback()})
#         return json.dumps({'result': ''})

#     def _attach_script(self):
#         url = ""
#         if self._app is not None:
#             url = str(__name__ + "_" + self._name + "_ctx_menu").replace('.', '_')
#             found = False
#             for rule in self._app.url_map.iter_rules():
#                 if rule.endpoint == url:
#                     found = True
#             if not found:
#                 self._app.add_url_rule('/' + url, url, self._process_onselect_callback)
#         items = "[\n"
#         for item in self._items:
#             items += item + ",\n"
#         items += "]"
#         script = """
#                     <script>
#                     $('#%s').w2menu({
#                         //type: type,
#                         align: '%s',
#                         openAbove: %s,
#                         search: %s,
#                         match: '%s',
#                         altRows: %s,
#                         index: %d,
#                         msgNoItems: '%s',
#                         items: %s,
#                         onSelect: function(event){
#                             $2.ajax({
#                                 url: '/%s',
#                                 type: 'get',
#                                 dataType: 'json',
#                                 error: function(err_status){
#                                         alertify.error("Status Code: "
#                                         + err_status.status + "<br />" + "Error Message:"
#                                         + err_status.statusText);
#                                 }
#                             });
#                         }
#                     });
#                     </script>
#                 """ % (self._name,
#                        self._align if self._align is not None else "none",
#                        json.dumps(self._open_above) if self._open_above is not None else json.dumps(False),
#                        json.dumps(self._search) if self._search is not None else json.dumps(False),
#                        self._match if self._match is not None else "begins",
#                        json.dumps(self._alt_rows) if self._alt_rows is not None else json.dumps(True),
#                        self._index if self._index is not None else 0,
#                        self._msg_no_items if self._msg_no_items is not None else 'No Items!',
#                        items,
#                        url
#                        )
#         return script

#     def render(self):
#         content = self._attach_script()
#         return content
