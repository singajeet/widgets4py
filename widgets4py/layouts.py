"""This module contains classes related to various layouts
supported by the system

Author: Ajeet Singh
Date: 06/24/2019
"""
from widgets4py.base import Widget


class SimpleGridLayout(Widget):
    """A simple grid layouts the components in the defined grid
    on first come first appear basis. This logic will go from
    left to right and top to bottom
    """

    _number_of_rows = None
    _number_of_columns = None
    _rows_ratio = None
    _columns_ratio = None

    def __init__(self, name, rows, columns, row_ratio=None, col_ratio=None,
                 desc=None, prop=None, style=None):
        """Default constructor with rows and columns parameters"""
        Widget.__init__(self, name, desc, 'table', prop, style)
        self._number_of_columns = columns
        self._number_of_rows = rows
        if row_ratio is not None:
            self._rows_ratio = row_ratio
        else:
            self._rows_ratio = []
        if col_ratio is not None:
            self._columns_ratio = col_ratio
        else:
            self._columns_ratio = []

    def render(self):
        """Renders the grid layout with its child components"""
        main_content = self._render_pre_content('table')
        widget_counter = 0
        widget_limit = self._child_widgets.__len__()

        # loop through the rows
        for row_index in range(self._number_of_rows):
            # check whether the height ratio is given for row and apply same
            if self._rows_ratio.__len__() > 0\
                    and row_index < self._rows_ratio.__len__():
                main_content += "\n<tr height=" + self._rows_ratio[row_index] + ">"
            else:
                main_content += "\n<tr>"
            # loop through the columns
            for col_index in range(self._number_of_columns):
                # Check whether the column ratio is given and apply same
                if self._columns_ratio.__len__() > 0\
                        and col_index < self._columns_ratio.__len__():
                    main_content += "\n<td width=" + self._columns_ratio[col_index] + ">"
                else:
                    main_content += "\n<td>"
                # check if widget is available then render it
                if widget_counter < widget_limit:
                    main_content += self._child_widgets[widget_counter].render()
                    widget_counter += 1
                else:
                    main_content += ""
                main_content += "\n</td>"
            main_content += "\n</tr>"
        self._widget_content = main_content + self._render_post_content('table')
        return self._widget_content


class GridLayout(Widget):
    """A grid layouts the components in the defined coordinates of each
    child components. While adding the components to Grid, the X & Y
    coordinates needs to be given too tell the location of child component
    """

    _number_of_rows = None
    _number_of_columns = None
    _child_widgets = None
    _rows_ratio = None
    _columns_ratio = None

    def __init__(self, name, rows, columns, row_ratio=None, col_ratio=None,
                 desc=None, prop=None, style=None):
        """Default constructor with rows and columns parameters"""
        Widget.__init__(self, name, desc, 'table', prop, style)
        self._number_of_columns = columns
        self._number_of_rows = rows
        self._child_widgets = {}
        if row_ratio is not None:
            self._rows_ratio = row_ratio
        else:
            self._rows_ratio = []
        if col_ratio is not None:
            self._columns_ratio = col_ratio
        else:
            self._columns_ratio = []

    def add(self, x, y, child):
        """Adds a child component to the Grid at specified coordinates

            Args:
                x (int): The horizontal position of the componenet in grid
                y (int): The vertical position of the component in grid
                child (Widget): The child widget component
        """
        key = str(x) + "|" + str(y)
        self._child_widgets[key] = child

    def remove(self, x, y):
        """Removes an widget which exists at the x,y location in grid

            Args:
                x (int): The horizontal position of the widget
                y (int): The vertical position of the widget
        """
        key = str(x) + "|" + str(y)
        self._child_widgets.pop(key)

    def render(self):
        """Renders the grid layout with its child components"""
        main_content = self._render_pre_content('table')

        for row_index in range(self._number_of_rows):
            if self._rows_ratio.__len__() > 0\
                    and row_index < self._rows_ratio.__len__():
                main_content += "\n<tr height=" + self._rows_ratio[row_index] + ">"
            else:
                main_content += "\n<tr>"
            for col_index in range(self._number_of_columns):
                if self._columns_ratio.__len__() > 0\
                        and col_index < self._columns_ratio.__len__():
                    main_content += "\n<td width=" + self._columns_ratio[col_index] + ">"
                else:
                    main_content += "\n<td>"
                key = str(col_index) + "|" + str(row_index)
                widget = self._child_widgets.get(key)
                if widget is not None:
                    main_content += widget.render()
                else:
                    main_content += "\n"
                main_content += "\n</td>"
            main_content += "\n</tr>"
        self._widget_content = main_content + self._render_post_content('table')
        return self._widget_content


class FlowLayout(Widget):
    """The simplest layout to put the widgets one after another in the flow
    """

    def __init__(self, name, rows, columns, row_ratio=None, col_ratio=None,
                 desc=None, prop=None, style=None):
        """Default constructor with rows and columns parameters"""
        Widget.__init__(self, name, desc, 'div', prop, style)

    def render(self):
        """renders the widgets in flow from left to right"""
        main_content = self._render_pre_content('div')
        for widget in self._child_widgets:
            main_content += widget.render()
        self._widget_content = main_content + self._render_post_content('div')
        return self._widget_content


class VerticalLayout(Widget):
    """The vertical layout of the widgets
    """

    def __init__(self, name, rows, columns, row_ratio=None, col_ratio=None,
                 desc=None, prop=None, style=None):
        """Default constructor with rows and columns parameters"""
        Widget.__init__(self, name, desc, 'div', prop, style)

    def render(self):
        """renders the widgets in flow from left to right"""
        main_content = self._render_pre_content('div')
        for widget in self._child_widgets:
            main_content += "\n<div>" + widget.render() + "\n</div>"
        self._widget_content = main_content + self._render_post_content('div')
        return self._widget_content


class HorizontalLayout(Widget):
    """The vertical layout of the widgets
    """

    def __init__(self, name, rows, columns, row_ratio=None, col_ratio=None,
                 desc=None, prop=None, style=None):
        """Default constructor with rows and columns parameters"""
        Widget.__init__(self, name, desc, 'div', prop, style)

    def render(self):
        """renders the widgets in flow from left to right"""
        main_content = self._render_pre_content('div')
        # display div as table and table-cell
        main_content += "\n<div style='display:table;'>"
        for widget in self._child_widgets:
            main_content += "\n<div style='display: table-cell;'>" + widget.render() + "\n</div>"
        main_content += "\n</div>"
        # table ended here
        self._widget_content = main_content + self._render_post_content('div')
        return self._widget_content
