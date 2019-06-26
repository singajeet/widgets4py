"""HTML Widgets based on the JQuery UI framework
Author: Ajeet Singh
Date: 06/25/2019
"""
from widgets4py.base import Widget


class JQButton(Widget):
    """JQuery Button class"""

    _title = None
    _app = None
    _onclick_callback = None

    def __init__(self, name, title, app=None, onclick_callback=None):
        """default constructor"""
        Widget.__init__(self, name)
        self._title = title
        self._app = app
        self._onclick_callback = onclick_callback

    def render(self):
        """Renders the JQuery button on the page"""
        url = ''
        content = ''
        if self._app is not None and self._onclick_callback is not None:
            url = str(__name__ + "_" + self._name).replace('_', '.')
            content = """<button id='%s' name='%s'>%s</button>
                        <script>
                            $(function(){
                                $('#%s').button();
                                $('#%s').click(function(event){
                                    $.ajax({
                                        url: '/%s',
                                        success: function(status){alert('success');},
                                        error: function(status){alert('error');}
                                    });
                                });
                            });
                        </script>
                    """ % (self._name, self._name, self._title, self._name, self._name, url)
            self._app.add_url_rule('/' + url, url, self._onclick_callback)
        else:
            content = """<button id='%s' name='%s' value='%s'></button>
                        <script>
                            $(function(){
                                $('%s').button();
                            });
                        </script>
                    """ % (self._name, self._name, self._title, self._name)
        self._widget_content = content
        return self._widget_content
