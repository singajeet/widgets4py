"""Python module to provide graphical or web bases widgets
using W2UI framework. This module wraps the required JavaScript
to make python objects and allows client-server to interact
using same instance of the widget i.e., a single widget instance
will render the widget at client side and same instance can be
used to execute server side code.

    Author: Ajeet Singh
    Date: 7/10/2019
"""
from widgets4py.base import Widget  # noqa
from flask import json, request  # noqa


class GridColumn:
    """Class representing an column of Grid widget. This class will be used
    by grid widget to maintain meta info for a given column
    """

    _field_name = None
    _caption = None
    _size = None

    def __init__(self, field_name, caption, size):
        """Below are the parameters of this class

            Args:
                field_name (string): A technical name of the column
                caption (string): Caption to be displayed in Grid's header
                size (int): Size of the column in percentage %% of total grid width
        """
        self._field_name = field_name
        self._caption = caption
        self._size = size

    @property
    def field_name(self):
        """A technical name of the column
        """
        return self._field_name

    @field_name.setter
    def field_name(self, val):
        self._field_name = val

    @property
    def caption(self):
        """A column title to be shown in Grid's header"""
        return self._caption

    @caption.setter
    def caption(self, val):
        self._caption = val

    @property
    def size(self):
        """Size of the column in %% of total grid's width"""
        return self._size

    @size.setter
    def size(self, val):
        self._size = val

    def render(self):
        content = """{ field: '%s', caption: '%s', size: '%d%%'}"""
        content = content % (self._field_name, self._caption, self._size)
        return json.dumps(content)


class GridColumnCollection:
    """A collection of Grid's all columns. All columns should be added to
    this class in order to be rendered in the Grid"""

    _columns = None

    def __init__(self, columns=[]):
        """A list of columns to be rendered in grid"""
        self._columns = columns

    def add(self, column):
        """Adds a column to this collection

            Args:
                column (GridColumn): An instance of GridColumn class
        """
        self._columns.append(column)

    def remove(self, column):
        """Removes the column from this collection

            Args:
                column (GridColumn): An instance of GridColumn class
        """
        self._columns.remove(column)

    @property
    def columns(self):
        """A list of columns to be shown in a grid"""
        return self._columns

    @columns.setter
    def columns(self, val):
        self._columns = val

    def render(self):
        """Renders the columns collection as JavaScript list"""
        content = "["
        for col in self._columns:
            content += col.render() + ",\n"
        content += "]"
        return content


class Record:
    """A row or record in the dataset of a Grid widget. This class
    takes an `dict` object containing all columns and its values
    and renders it in JavaScript format"""

    _record = None

    def __init__(self, record={}):
        """Below are the parameters of this class """
        self._record = record

    def add_cell(self, column_name, value):
        """Helps in adding cells one by one in the current record"""
        self._record[column_name] = value

    def remove_cell(self, column_name):
        """Removes a cell from the record """
        self._record.pop(column_name)

    @property
    def record(self):
        """A record or row in the Grid Widget"""
        return self._record

    @record.setter
    def record(self, val):
        self._record = val
