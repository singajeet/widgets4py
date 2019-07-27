"""This module provides HTML5 Widgets combined with websocket
to be used in a standlone app or any other web app. The websocket
is available through Flask and Socket IO implementation for python
and the is rendered using Javascript Socket-IO client API's

Author: Ajeet Singh
Date: 07/25/2019
"""
from flask_socketio import emit, Namespace
from widgets4py.base import Widget


class Button(Namespace, Widget):

    _app = None
    _socket_io = None
    _title = None
    _click_callback = None
    _namespace_url = None
    _disabled = None

    def __init__(self, name, title, app, socket_io, click_callback=None, disabled=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_click').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_click").replace('.', '_')
        self.add_property('type', 'button')
        self.add_property('value', title)
        self._name = name
        self._title = title
        self._app = app
        self._socket_io = socket_io
        self._click_callback = click_callback
        socket_io.on_namespace(self)
        if disabled is not None:
            self.disabled = disabled
        else:
            self._disabled = False

    @property
    def namespace(self):
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties(self._namespace_url)

    # def set_disabled(self, obj):
    #     self._sync_properties(obj.namespace)

    def _sync_properties(self, ns):
        emit('sync_properties_' + self._name, {'disabled': self._disabled, 'title': self._title}, namespace=ns)

    def on_click(self, click_callback, app=None):
        if app is not None:
            self._app = app
        self._click_callback = click_callback

    def on_fire_click_event(self, props):
        """For internal use only
        """
        try:
            if self._click_callback is not None:
                self._click_callback(self._name, props)
                emit('success', {'status': True, 'message': 'success'})
            else:
                emit('warning', {'status': False, 'message': 'No callback registered'})
        except Exception as e:
            print("Error: " + str(e))
            msg = 'Method failed during callback execution: '  + str(e)
            emit('failed', {'status': False, 'message': msg})

    def on_connect(self):
        pass

    def on_disconnect(self):
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
        # content = "<input type='button' value='" + self._title
        # content += "' id='" + self._name + "' />"
        # content += "\n" + self._attach_script()
        # return content
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content


class TextBox(Namespace, Widget):

    _app = None
    _socket_io = None
    _text = None
    _change_callback = None
    _namespace_url = None
    _disabled = None
    _readonly = None

    def __init__(self, name, app, socket_io, change_callback=None, disabled=None, readonly=None, text=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_change').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_change").replace('.', '_')
        self.add_property('type', 'text')
        self._name = name
        if text is not None:
            self.add_property('value', text)
            self._text = text
        else:
            self._text = ""
        self._app = app
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
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val
        self._sync_properties(self._namespace_url)

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, val):
        self._readonly = val
        self._sync_properties(self._namespace_url)

    # def set_disabled(self, obj):
    #     self._sync_properties(obj.namespace)

    def _sync_properties(self, ns):
        emit('sync_properties_' + self._name, {'disabled': self._disabled,
                                               'text': self._text,
                                               'readonly': self._readonly},
             namespace=ns)

    def on_change(self, change_callback, app=None):
        if app is not None:
            self._app = app
        self._change_callback = change_callback

    def on_fire_change_event(self, props):
        """For internal use only
        """
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
        pass

    def on_disconnect(self):
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
        # content = "<input type='text' value='" + self._text
        # content += "' id='" + self._name + "' />"
        # content += "\n" + self._attach_script()
        content = self._render_pre_content('input')
        content += self._render_post_content('input')
        self._widget_content = content + "\n" + self._attach_script()
        return self._widget_content


class CheckBox(Namespace, Widget):

    _app = None
    _socket_io = None
    _namespace_url = None
    _title = None
    _value = None
    _checked = None
    _disabled = None
    _click_callback = None

    def __init__(self, name, app, socket_io, title=None, click_callback=None, disabled=None, value=None, checked=None):
        Widget.__init__(self, name)
        Namespace.__init__(self, ('/' + str(__name__ + '_' + name + '_click').replace('.', '_')))
        self._namespace_url = '/' + str(__name__ + "_" + name + "_click").replace('.', '_')
        self._name = name
        self._title = title
        self._app = app
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
        return self._namespace_url

    @namespace.setter
    def namespace(self, val):
        self._namespace_url = val

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, val):
        self._disabled = val
        self._sync_properties(self._namespace_url)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._sync_properties(self._namespace_url)

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, val):
        self._checked = val
        self._sync_properties(self._namespace_url)

    @property
    def value(self):
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

    def on_click(self, click_callback, app=None):
        if app is not None:
            self._app = app
        self._click_callback = click_callback

    def on_fire_click_event(self, props):
        """For internal use only
        """
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
        pass

    def on_disconnect(self):
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
                            socket.emit('fire_click_event', {'disabled': disabled, 'title': title, 'checked': checked, 'value': val});
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
        # content = "<input type='text' value='" + self._text
        # content += "' id='" + self._name + "' />"
        # content += "\n" + self._attach_script()
        # return content
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
            content += "\n<div>" + "\n" + self._attach_script()
            self._widget_content = content
            return self._widget_content
