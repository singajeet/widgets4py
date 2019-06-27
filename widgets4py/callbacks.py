"""Callback objects to be used by widgets for event handling
Author: Ajeet Singh
Date: 06/27/2019
"""


class Callback:
    """Callback class to be used for handling events"""

    _root_widget = None
    _callback_handler = None

    def __init__(self, callback):
        self._callback_handler = callback

    def set_root_widget(self, widget):
        """Sets the widget passed as root widget for the system"""
        self._root_widget = widget

    def call_it(self):
        """This method will be called by the system, not to be used as API"""
        self._callback_handler()
        #return self._root_widget.render()
