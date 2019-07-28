"""This module provides HTML5 Widgets combined with websocket
to be used in a standlone app or any other web app. The websocket
is available through Flask and Socket IO implementation for python
and the is rendered using Javascript Socket-IO client API's

Author: Ajeet Singh
Date: 07/25/2019
"""
import os
from flask_socketio import emit, Namespace
from widgets4py.base import Widget


class Button(Namespace, Widget):
    """A simple button widget having the capabilites to fire click event
    at server whenever this button is clicked in the client window
    """

    _socket_io = None
    _title = None
    _click_callback = None
    _namespace_url = None
    _disabled = None

    def __init__(self, name, title, socket_io, click_callback=None, disabled=None, desc=None, prop=None,
                 style=None, attr=None, css_cls=None):
        """Default constructor of the Button widget class

            Args:
                name (string): name of the widget for internal use
                title (string): title of the button widget
                socket_io (SocketIO, required): An instance of the `SocketIO` class
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                onclick_callback (callable): A function to be called back on onclick event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onclick_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
                css_cls (list): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_click').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_click").replace('.', '_')
        self.add_property('type', 'button')
        self.add_property('value', title)
        self._name = name
        self._title = title
        self._socket_io = socket_io
        self._click_callback = click_callback
        socket_io.on_namespace(self)
        if disabled is not None:
            self.disabled = disabled
        else:
            self._disabled = False

    @property
    def namespace(self):
        """Namespace is the communication port used by the Flask-SocketIO framework"""
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        """Enables or disables the widget in client's window"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def title(self):
        """Title of the button widget"""
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties(self._namespace_url)

    # def set_disabled(self, obj):
    #     self._sync_properties(obj.namespace)

    def _sync_properties(self, ns):
        emit('sync_properties_' + self._name, {'disabled': self._disabled, 'title': self._title}, namespace=ns)

    def on_click(self, click_callback):
        """Registers an callback passed as argument with the onclick event

            Args:
                click_callback (callable): Function or method that should be executed when event fires
        """
        self._click_callback = click_callback

    def on_fire_click_event(self, props):
        """For internal use only: This function is called by the websocket when the event is raised.
        """
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        title = props['title']
        if title is not None:
            self._title = title
        try:
            if self._click_callback is not None:
                self._click_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            msg = 'Method failed during callback execution: ' + str(e)
            emit('failed', {'status': False, 'message': msg})

    def on_connect(self):
        """Called by websocket when connection is established"""
        pass

    def on_disconnect(self):
        """Called by websocket when connection is terminated"""
        pass

    def _attach_script(self):
        script = """
                    <script>
                    $(document).ready(function(){
                        var socket = io('%s');
                        var selector = $('#%s');

                        $('#%s').click(function(){
                            var disabled = selector.prop('disabled')
                            var title = selector.val();
                            socket.emit('fire_click_event', {'disabled': disabled, 'title': title});
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
                            selector.prop('disabled', props['disabled']);
                            selector.val(props['title']);
                        });
                    });
                    </script>
                """ % (self._namespace_url, self._name, self._name, self._name)
        return script

    def render(self):
        """Renders the content of the widget on the page"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content


class TextBox(Namespace, Widget):
    """TextBox widget is used to take string or alphanumeric inputs from the user"""

    _socket_io = None
    _text = None
    _change_callback = None
    _namespace_url = None
    _disabled = None
    _readonly = None

    def __init__(self, name, socket_io, change_callback=None, disabled=None, readonly=None, text=None,
                 desc=None, prop=None, style=None, attr=None, css_cls=None):
        """Default constructor of the TextBox widget class

            Args:
                name (string): name of the widget for internal use
                text (string): Initial text to be displayed in the widget
                socket_io (SocketIO, required): An instance of the `SocketIO` class
                readonly (boolean): Puts the widget in the readonly mode
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                onchange_callback (callable): A function to be called back on onchange event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
                css_cls (list): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_change').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_change").replace('.', '_')
        self.add_property('type', 'text')
        self._name = name
        if text is not None:
            self.add_property('value', text)
            self._text = text
        else:
            self._text = ""
        self._socket_io = socket_io
        self._change_callback = change_callback
        socket_io.on_namespace(self)
        if disabled is not None:
            self.disabled = disabled
        else:
            self._disabled = False
        if readonly is not None:
            self._readonly = readonly
        else:
            self._readonly = False

    @property
    def namespace(self):
        """Namespace is the communication port used by the Flask-SocketIO"""
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        """Enabled or disabled state of the widget"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def text(self):
        """Current text value stored in the widget"""
        return self._text

    @text.setter
    def text(self, val):
        self._text = val
        self._sync_properties(self._namespace_url)

    @property
    def readonly(self):
        """Change the state of widget to readonly or vice-versa"""
        return self._readonly

    @readonly.setter
    def readonly(self, val):
        self._readonly = val
        self._sync_properties(self._namespace_url)

    def _sync_properties(self, ns):
        emit('sync_properties_' + self._name, {'disabled': self._disabled,
                                               'text': self._text,
                                               'readonly': self._readonly},
             namespace=ns)

    def on_change(self, change_callback):
        """Registers an callable event handler with the textbox and called when text value is changed"""
        self._change_callback = change_callback

    def on_fire_change_event(self, props):
        """For internal use only. This method is called by websocket on text changed event of the widget
        """
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        rdonly = props['readonly']
        if rdonly is not None:
            self._readonly = rdonly
        txt = props['text']
        if txt is not None:
            self._text = txt
        try:
            if self._change_callback is not None:
                self._change_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            emit('failed', {'status': False, 'message': 'Method failed during callback execution: ' + str(e)})

    def on_connect(self):
        """This method is called when websocket connection is established"""
        pass

    def on_disconnect(self):
        """This method is called when websocket connection is terminated"""
        pass

    def _attach_script(self):
        script = """
                    <script>
                    $(document).ready(function(){
                        var socket = io('%s');
                        var selector = $('#%s');

                        $('#%s').change(function(){
                            var disabled = selector.prop('disabled')
                            var text = selector.val();
                            var readonly = selector.prop('readOnly')
                            socket.emit('fire_change_event', {'disabled': disabled, 'text': text, 'readonly': readonly});  //  # noqa
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
                            selector.prop('disabled', props['disabled']);
                            selector.val(props['text']);
                            selector.prop('readOnly', props['readonly']);
                        });
                    });
                    </script>
                """ % (self._namespace_url, self._name, self._name, self._name)
        return script

    def render(self):
        """Renders the content of widget on page"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content


class CheckBox(Namespace, Widget):
    """The chexkbox widget allows to enter input in only two states: True and False or Checked and Unchecked.
    At a time the input can be only in one state i.e., True (checked) or False (unchecked)
    """

    _socket_io = None
    _namespace_url = None
    _title = None
    _value = None
    _checked = None
    _disabled = None
    _click_callback = None

    def __init__(self, name, socket_io, title=None, click_callback=None, disabled=None, value=None, checked=None,
                 desc=None, prop=None, style=None, attr=None, css_cls=None):
        """Default constructor of the CheckBox widget class

            Args:
                name (string): name of the widget for internal use
                socket_io (SocketIO, required): An instance of the `SocketIO` class
                title (string): The label that will be rendered next to checkbox
                value (string): An value associated with checkbox
                checked (boolean): Initial state of the checkbox i.e., checked or unchecked
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                onchange_callback (callable): A function to be called back on onchange event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
                css_cls (list): An list of CSS class names to be added to current widget
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_click').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_click").replace('.', '_')
        self._name = name
        self._title = title
        self._socket_io = socket_io
        self.add_property('type', 'checkbox')
        if value is not None:
            self.add_property('value', value)
            self._value = value
        self._click_callback = click_callback
        socket_io.on_namespace(self)
        if disabled is not None:
            self.disabled = disabled
        else:
            self._disabled = False
        if checked is not None and checked:
            self.add_attribute('checked')
            self._checked = checked
        else:
            self._checked = False

    @property
    def namespace(self):
        """Namespace is the communication port used by the websocket"""
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        """Enabled or disabled state of the widget"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def title(self):
        """Title or label of the widget shown next to checkbox"""
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties(self._namespace_url)

    @property
    def checked(self):
        """True or False state of the checkbox"""
        return self._checked

    @checked.setter
    def checked(self, val):
        self._checked = val
        self._sync_properties(self._namespace_url)

    @property
    def value(self):
        """The alphanumeric value associated with the checkbox"""
        return self._value

    @value.setter
    def value(self, val):
        self.value = val
        self._sync_properties(self._namespace_url)

    # def set_disabled(self, obj):
    #     self._sync_properties(obj.namespace)

    def _sync_properties(self, ns):
        emit('sync_properties_' + self._name, {'disabled': self._disabled,
                                               'title': self._title,
                                               'checked': self._checked,
                                               'value': self._value},
             namespace=ns)

    def on_click(self, click_callback):
        """Attaches an event handler that will be executed when checked state changes"""
        self._click_callback = click_callback

    def on_fire_click_event(self, props):
        """For internal use only. This method is called when mouse click is detected over the widget
        """
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        title = props['title']
        if title is not None:
            self._title = title
        chk = props['checked']
        if chk is not None:
            self._checked = chk
        val = props['value']
        if val is not None:
            self._value = val
        try:
            if self._click_callback is not None:
                self._click_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            emit('failed', {'status': False, 'message': 'Method failed during callback execution: ' + str(e)})

    def on_connect(self):
        """This method is called when websocket establish an connection"""
        pass

    def on_disconnect(self):
        """This method is called when websocket's connection is terminated"""
        pass

    def _attach_script(self):
        script = """
                    <script>
                    $(document).ready(function(){
                        var socket = io('%s');
                        var selector = $('#%s');
                        var lbl_selector = $('#%s_lbl');

                        $('#%s').click(function(){
                            var disabled = selector.prop('disabled');
                            var title = lbl_selector.text();
                            var checked = selector.is(":checked");
                            var val = selector.val();
                            socket.emit('fire_click_event', {'disabled': disabled,
                                                             'title': title,
                                                             'checked': checked,
                                                             'value': val});
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
                            selector.prop('disabled', props['disabled']);
                            selector.prop('checked', props['checked']);
                            selector.val(props['value']);
                            lbl_selector.text(props['text']);
                        });
                    });
                    </script>
                """ % (self._namespace_url, self._name, self._name, self._name, self._name)
        return script

    def render(self):
        """Render the content of the widget on the page"""
        if self._title is None:
            content = self._render_pre_content('input')
            content += self._render_post_content('input')
            self._widget_content = content + "\n" + self._attach_script()
            return self._widget_content
        else:
            content = "<div class='ui-widget-content'>\n"
            content += self._render_pre_content('input')
            content += self._render_post_content('input')
            content += "\n<label for='" + self._name + "' id='" +\
                       self._name + "_lbl'>" + self._title + "</label>"
            content += "\n</div>" + "\n" + self._attach_script()
            self._widget_content = content
            return self._widget_content


class Color(Namespace, Widget):
    """A Color widget having the capabilites to fire change event
    at server whenever this color is selected from palette
    in the client window
    """

    _socket_io = None
    _click_callback = None
    _namespace_url = None
    _disabled = None
    _value = None

    def __init__(self, name, socket_io, change_callback=None, disabled=None, desc=None, prop=None,
                 style=None, attr=None, css_cls=None, value=None):
        """Default constructor of the Color widget class

            Args:
                name (string): name of the widget for internal use
                socket_io (SocketIO, required): An instance of the `SocketIO` class
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                onchange_callback (callable): A function to be called back on onchange event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
                css_cls (list): An list of CSS class names to be added to current widget
                value (string): The pre-selected value of the color
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_change').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_change").replace('.', '_')
        self.add_property('type', 'color')
        if value is not None:
            self.add_property('value', value)
            self._value = value
        else:
            self._value = ""
        self._name = name
        self._socket_io = socket_io
        self._change_callback = change_callback
        socket_io.on_namespace(self)
        if disabled is not None:
            self.disabled = disabled
        else:
            self._disabled = False

    @property
    def namespace(self):
        """Namespace is the communication port used by the Flask-SocketIO framework"""
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        """Enables or disables the widget in client's window"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def value(self):
        """Selected value of the color"""
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._sync_properties(self._namespace_url)

    def _sync_properties(self, ns):
        emit('sync_properties_' + self._name, {'disabled': self._disabled, 'value': self._value}, namespace=ns)

    def on_change(self, change_callback):
        """Registers an change passed as argument with the onchange event

            Args:
                change_callback (callable): Function or method that should be executed when event fires
        """
        self._change_callback = change_callback

    def on_fire_change_event(self, props):
        """For internal use only: This function is called by the websocket when the event is raised.
        """
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        val = props['value']
        if val is not None:
            self._value = val
        try:
            if self._change_callback is not None:
                self._change_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            msg = 'Method failed during callback execution: ' + str(e)
            emit('failed', {'status': False, 'message': msg})

    def on_connect(self):
        """Called by websocket when connection is established"""
        pass

    def on_disconnect(self):
        """Called by websocket when connection is terminated"""
        pass

    def _attach_script(self):
        script = """
                    <script>
                    $(document).ready(function(){
                        var socket = io('%s');
                        var selector = $('#%s');

                        $('#%s').change(function(){
                            var disabled = selector.prop('disabled')
                            var value = selector.val();
                            socket.emit('fire_change_event', {'disabled': disabled, 'value': value});
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
                            selector.prop('disabled', props['disabled']);
                            selector.val(props['value']);
                        });
                    });
                    </script>
                """ % (self._namespace_url, self._name, self._name, self._name)
        return script

    def render(self):
        """Renders the content of the widget on the page"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content


class Date(Namespace, Widget):
    """Date widget displays an calendar to get the inputs from the user
        NOTE: Not supported on all browsers
   """

    _socket_io = None
    _change_callback = None
    _namespace_url = None
    _disabled = None
    _readonly = None
    _value = None
    _max = None
    _min = None

    def __init__(self, name, socket_io, change_callback=None, disabled=None,
                 readonly=None, desc=None, prop=None, style=None,
                 attr=None, css_cls=None, value=None, max=None, min=None):
        """Default constructor of the Date widget class

            Args:
                name (string): name of the widget for internal use
                socket_io (SocketIO, required): An instance of the `SocketIO` class
                readonly (boolean): Puts the widget in the readonly mode
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                onchange_callback (callable): A function to be called back on onchange event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
                css_cls (list): An list of CSS class names to be added to current widget
                value (string): The current selected date in YYYY-MM-DD format
                max (string): The max limit the calendar can be navigated to
                min (string): The min limit the calendar can be navigated to
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_change').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_change").replace('.', '_')
        self.add_property('type', 'date')
        self._name = name
        if value is not None:
            self.add_property('value', value)
            self._value = value
        else:
            self._value = ""
        self._socket_io = socket_io
        self._change_callback = change_callback
        socket_io.on_namespace(self)
        if disabled is not None:
            self.disabled = disabled
        else:
            self._disabled = False
        if max is not None:
            self._max = max
        if min is not None:
            self._min = min
        if readonly is not None:
            self._readonly = readonly
        else:
            self._readonly = False

    @property
    def namespace(self):
        """Namespace is the communication port used by the Flask-SocketIO"""
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        """Enabled or disabled state of the widget"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def value(self):
        """Current text value stored in the widget"""
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._sync_properties(self._namespace_url)

    @property
    def max(self):
        """The max limit the calendar can be navigated to
        """
        return self._max

    @max.setter
    def max(self, val):
        self._max = val
        self._sync_properties(self._namespace_url)

    @property
    def min(self):
        """The min limit the calendar can be navigated to
        """
        return self._min

    @min.setter
    def min(self, val):
        self._min = val
        self._sync_properties(self._namespace_url)

    @property
    def readonly(self):
        """The edit mode of the date widget"""
        return self._readonly

    @readonly.setter
    def readonly(self, val):
        self._readonly = val
        self._sync_properties(self._namespace_url)

    def _sync_properties(self, ns):
        emit('sync_properties_' + self._name, {'disabled': self._disabled,
                                               'value': self._value,
                                               'max': self._max,
                                               'min': self._min,
                                               'readonly': self._readonly},
             namespace=ns)

    def on_change(self, change_callback):
        """Registers an callable event handler with the textbox and called when text value is changed"""
        self._change_callback = change_callback

    def on_fire_change_event(self, props):
        """For internal use only. This method is called by websocket on text changed event of the widget
        """
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        val = props['value']
        if val is not None:
            self._value = val
        max = props['max']
        if max is not None:
            self._max = max
        min = props['min']
        if min is not None:
            self._min = min
        rdonly = props['readonly']
        if rdonly is not None:
            self._readonly = rdonly
        try:
            if self._change_callback is not None:
                self._change_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            emit('failed', {'status': False, 'message': 'Method failed during callback execution: ' + str(e)})

    def on_connect(self):
        """This method is called when websocket connection is established"""
        pass

    def on_disconnect(self):
        """This method is called when websocket connection is terminated"""
        pass

    def _attach_script(self):
        script = """
                    <script>
                    $(document).ready(function(){
                        var socket = io('%s');
                        var selector = $('#%s');

                        $('#%s').change(function(){
                            var disabled = selector.prop('disabled');
                            var value = selector.val();
                            var max = selector.prop('max');
                            var min = selector.prop('min');
                            var rdonly = selector.prop('readOnly');
                            socket.emit('fire_change_event', {'disabled': disabled, 'value': value, 'max': max, 'min': min, 'readonly': rdonly});  //  # noqa
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
                            selector.prop('disabled', props['disabled']);
                            selector.val(props['value']);
                            selector.prop('max', props['max']);
                            selector.prop('min', props['min']);
                            selector.prop('readOnly', props['readonly']);
                        });
                    });
                    </script>
                """ % (self._namespace_url, self._name, self._name, self._name)
        return script

    def render(self):
        """Renders the content of widget on page"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content


class DateTimeLocal(Date):
    """DateTimeLocal shows an calendar with date and time to get inputs from the user
    NOTE: Not supported on all browsers
    """

    def __init__(self, name, socket_io, change_callback=None, disabled=None,
                 readonly=None, desc=None, prop=None, style=None,
                 attr=None, css_cls=None, value=None, max=None, min=None):
        """Default constructor of the DateTimeLocal widget class

            Args:
                name (string): name of the widget for internal use
                socket_io (SocketIO, required): An instance of the `SocketIO` class
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                onchange_callback (callable): A function to be called back on onchange event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
                css_cls (list): An list of CSS class names to be added to current widget
                value (string): The current selected date in YYYY-MM-DD format
                max (string): The max limit the calendar can be navigated to
                min (string): The min limit the calendar can be navigated to
        """
        Date.__init__(self, name, socket_io, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls, min=min,
                      max=max, value=value, change_callback=change_callback)
        self.add_property('type', 'datetime-local')


class Email(TextBox):
    """Email widget is used to take email address as input from the user
    NOTE: Not supported on all browsers
    """

    def __init__(self, name, socket_io, change_callback=None, disabled=None, readonly=None, email=None,
                 desc=None, prop=None, style=None, attr=None, css_cls=None):
        """Default constructor of the Email widget class

            Args:
                name (string): name of the widget for internal use
                email (string): Initial email address to be displayed in the widget
                socket_io (SocketIO, required): An instance of the `SocketIO` class
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                readonly (Boolean): Puts the widget in the readonly mode
                onchange_callback (callable): A function to be called back on onchange event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onchange_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
                css_cls (list): An list of CSS class names to be added to current widget
        """
        TextBox.__init__(self, name, socket_io, text=email, desc=desc, prop=prop, style=style, attr=attr,
                         css_cls=css_cls, change_callback=change_callback, disabled=disabled, readonly=readonly)
        self.add_property('type', 'email')


class File(Namespace, Widget):
    """A simple file widget having the capabilites to fire click event
    at server whenever an file from client is loaded to server. The
    path to store files on server is configurable and it also support
    multiple file upload
    """

    _socket_io = None
    _click_callback = None
    _change_callback = None
    _namespace_url = None
    _disabled = None
    _multiple = None
    _upload_folder = None
    _allowed_extensions = None

    def __init__(self, name, socket_io, click_callback=None, disabled=None, desc=None, prop=None,
                 style=None, attr=None, css_cls=None, multiple=None, upload_folder=None,
                 allowed_extensions=None, change_callback=None):
        """Default constructor of the Button widget class

            Args:
                name (string): name of the widget for internal use
                socket_io (SocketIO, required): An instance of the `SocketIO` class
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                click_callback (callable): A function to be called back on onclick event.
                                            The callback method should accept two args: `source` and `props`
                                            as shown in below example:

                        def onclick_handler(source, props):
                            pass

                        source: Name of the button for which this event is fired
                        props: Dict object having two props: Title & Disabled
                change_callback (callable): Same as onclick but fires on change event of widget
                css_cls (list): An list of CSS class names to be added to current widget
                multiple (boolean): Allows multiple files to be uploaded
                upload_folder (string): The path on the server where files should be stored. This path is
                                        relative the web server path
                allowed_extensions (list): A list of strings containing the ext allowed to be uploaded
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr, css_cls=css_cls)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_click').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_click").replace('.', '_')
        self.add_property('type', 'file')
        if multiple is not None:
            self._multiple = multiple
        else:
            self._multiple = False
        if upload_folder is not None:
            self._upload_folder = upload_folder
        else:
            self._upload_folder = "uploads"
        if allowed_extensions is not None:
            self._allowed_extensions = allowed_extensions
        else:
            self._allowed_extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg',
                                            'gif', 'doc', 'docx', 'xls', 'xlsx'])
        self._click_callback = click_callback
        self._change_callback = change_callback
        socket_io.on_namespace(self)

    def _allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self._allowed_extensions

    @property
    def namespace(self):
        """Namespace is used by websocket as connection port"""
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        """To enable or disable the file widget"""
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def multiple(self):
        """Allows to upload multiple files if set to True"""
        return self._multiple

    @multiple.setter
    def multiple(self, val):
        self._multiple = val
        self._sync_properties(self._namespace_url)

    @property
    def upload_folder(self):
        """The path on the server where uploaded files will be stored. The path is relative to
        root of the application on webserver. The default path is "uploads/"
        """
        return self._upload_folder

    @upload_folder.setter
    def upload_folder(self, val):
        self._upload_folder = val
        self._sync_properties(self._namespace_url)

    @property
    def allowed_extensions(self):
        """List of allowed file extensions to be uploaded"""
        return self._allowed_extensions

    @allowed_extensions.setter
    def allowed_extensions(self, val):
        self._allowed_extensions = val
        self._sync_properties(self._namespace_url)

    def _sync_properties(self, ns):
        emit('sync_properties_' + self._name, {'disabled': self._disabled,
                                               'multiple': self._multiple},
             namespace=ns)

    def on_change(self, change_callback):
        """Registers an callable event handler with the widget and called when text value is changed"""
        self._change_callback = change_callback

    def on_click(self, click_callback):
        """Registers an callable event handler with the widget and called when the widget is clicked"""
        self._click_callback = click_callback

    def on_fire_change_event(self, props):
        """For internal use only. This method is called by websocket on value changed event of the widget
        """
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        mul = props['multiple']
        if mul is not None:
            self._multiple = mul
        files = props['files']
        if files is not None:
            files_path = []
            for fl in files:
                if fl and self._allowed_file(fl.filename):
                    filename = fl.filename
                    if not os.path.exists(self._upload_folder):
                        os.mkdir(self._upload_folder)
                    fl.save(os.path.join(self._upload_folder, filename))
                    files_path.append(os.path.join(self._upload_folder, filename))
        try:
            if self._change_callback is not None:
                self._change_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            emit('failed', {'status': False, 'message': 'Method failed during callback execution: ' + str(e)})

    def on_fire_click_event(self, props):
        """For internal use only. This method is called by websocket on click event of the widget
        """
        dsbl = props['disabled']
        if dsbl is not None:
            self._disabled = dsbl
        mul = props['multiple']
        if mul is not None:
            self._multiple = mul
        try:
            if self._click_callback is not None:
                self._click_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            emit('failed', {'status': False, 'message': 'Method failed during callback execution: ' + str(e)})

    def on_connect(self):
        """This method is called when websocket connection is established"""
        # pass
        print("\nConnected\n")

    def on_disconnect(self):
        """This method is called when websocket connection is terminated"""
        # pass
        print("\nDisconnected\n")

    def _attach_script(self):
        script = """
                    <script>
                    $(document).ready(function(){
                        var socket = io('%s');
                        var selector = $('#%s');

                        $('#%s').change(function(){
                            var disabled = selector.prop('disabled');
                            var mul = selector.prop('multiple');
                            var files = selector.prop('files');
                            socket.emit('fire_change_event', {'disabled': disabled,
                                                              'multiple': multiple,
                                                              'files': files});
                        });

                        $('#%s').click(function(){
                            var disabled = selector.prop('disabled');
                            var mul = selector.prop('multiple');
                            socket.emit('fire_click_event', {'disabled': disabled, 'multiple': multiple});
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
                            alert("Connected");
                        });

                        socket.on('sync_properties_%s', function(props){
                            selector.prop('disabled', props['disabled']);
                            selecttor.prop('multiple', props['multiple']);
                        });
                    });
                    </script>
                """ % (self._namespace_url, self._name, self._name, self._name, self._name)
        return script

    def render(self):
        """Renders the content of widget on page"""
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content
