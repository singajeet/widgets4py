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
    _render = None
    _attributes = None
    _sortable = None

    def __init__(self, field_name, caption, size, render=None, attributes=None, sortable=None):
        """Below are the parameters of this class

            Args:
                field_name (string): A technical name of the column
                caption (string): Caption to be displayed in Grid's header
                size (int): Size of the column in percentage %% of total grid width
                render (string): A format string to render cell contents like, money, date,etc
                attributes (string): A key value pair to format the row eg, align=center
        """
        self._field_name = field_name
        self._caption = caption
        self._size = size
        self._render = render
        self._attributes = attributes
        self._sortable = sortable

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

    @property
    def attributes(self):
        """Attributes to format whole column of the grid"""
        return self._attributes

    @attributes.setter
    def attributes(self, val):
        self._attributes = val

    @property
    def render(self):
        """Render value to format the whole column"""
        return self._render

    @render.setter
    def render(self, val):
        self._render = val

    @property
    def sortable(self):
        """Whether the current column is sortable or not"""
        return self._sortable

    @sortable.setter
    def sortable(self, val):
        self._sortable = val

    def render(self):
        content = """{ field: '%s', caption: '%s', size: '%d%%'"""
        content = content % (self._field_name, self._caption, self._size)
        if self._attributes is not None:
            content += ", attr: '" + self._attributes + "'"
        if self._render is not None:
            content += ", render: '" + self._render + "'"
        if self._sortable is not None:
            content += ", sortable: " + json.dumps(self._sortable)
        content += "}"
        return content


class GridColumnCollection:
    """A collection of Grid's all columns. All columns should be added to
    this class in order to be rendered in the Grid"""

    _columns = None

    def __init__(self, columns=None):
        """A list of columns to be rendered in grid"""
        if columns is not None:
            self._columns = columns
        else:
            self._columns = []

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


class GridRecord:
    """A row or record in the dataset of a Grid widget. This class
    takes an `dict` object containing all columns and its values
    and renders it in JavaScript format"""

    _cells = None
    _style = None

    def __init__(self, cells=None, style=None):
        """Below are the parameters of this class

            Args:
                record (dict): A 'dict' of cells in an given record
        """
        if cells is not None:
            self._cells = cells
        else:
            self._cells = {}
        self._style = style

    def add_cell(self, column_name, value):
        """Helps in adding cells one by one in the current record"""
        self._cells[column_name] = value

    def remove_cell(self, column_name):
        """Removes a cell from the record """
        self._cells.pop(column_name)

    @property
    def record(self):
        """A record or row in the Grid Widget"""
        return self._cells

    @record.setter
    def record(self, val):
        self._cells = val

    @property
    def style(self):
        """The style for the whole row or record"""
        return self._style

    @style.setter
    def style(self, val):
        self._style = val

    def render(self):
        """Renders the record in JavaScript format and returns to parent widget"""
        content = "{"
        for cell in self._cells:
            if type(self._cells.get(cell)) == int:
                content += cell + ": " + str(self._cells.get(cell)) + ", "
            else:
                content += cell + ": '" + self._cells.get(cell) + "', "
        if self._style is not None:
            content += "w2ui: { style: '" + self._style + "'}"
        content += "}"
        return content


class SummaryGridRecord(GridRecord):
    """Renders an summary row at the end of the grid. The cell names should be same as
    available in `GridRecord' but its content should have the summary details. For example,
    if GridRecord have the following columns {'fname': 'Jane', lname: 'Doe', qty: 1000},
    the summary record can have the following structure {'fname': 'Total', qty: '1000'}

    The cell value can have HTML included to format it e.g., {'fname': '<span>Total</span>'}
    """

    def render(self):
        """Renders the summary record at the last of the Grid widget"""
        content = "{ w2ui: { summary: true },\n"
        for cell in self._cells:
            if type(self._cells.get(cell)) == int:
                content += cell + ": " + str(self._cells.get(cell)) + ", "
            else:
                content += cell + ": '" + self._cells.get(cell) + "', "
        content += "}"
        return content


class GridRecordCollection:
    """A collection of rows or records of an Grid. All records should be added to
    this class in order to be rendered under an Grid Widget
    """

    _records = None
    _counter = None

    def __init__(self, records=None):
        """Default constructor of this class with below parameters

            Args:
                records (list): A list of records to be rendered in Grid widget
        """
        if records is not None:
            self._records = records
        else:
            self._records = []
        self._counter = 1

    @property
    def records(self):
        return self._records

    @records.setter
    def records(self, val):
        self._records = val

    @property
    def count(self):
        """Returns the number of records available in the collection"""
        return self._records.__len__()

    def add(self, record):
        """Adds an row or record in the collection

            Args:
                record (GridRecord): A gird record or row to be added
        """
        record.add_cell('recid', self._counter)
        self._counter += 1
        self._records.append(record)

    def remove(self, record):
        """Removes an row from the rows collection

            Args:
                record: Record to be removed from the collection
        """
        self._counter -= 1
        self._records.pop(record)

    def render(self):
        """Function to render all records in the JavaScript list format"""
        content = "["
        for rec in self._records:
            content += rec.render() + ",\n"
        content += "]"
        return content


class GridSearch:
    """Defines an search option for the Grid widget. It contains the information of
    field name, caption, type, etc to define an search option for the Grid
    """

    _field = None
    _caption = None
    _type = None
    _options = None

    def __init__(self, field, caption, ftype, options=None):
        """Default constructor parameters

            field (string): Name of the existing field in the Grid widget
            caption (string): A title of the field used for search
            type (string): type of the field that will be used to search
            options (dict): shows a predefined options to select in the search toolbar
                            e.g., ['ABC', 'DEF', 'GHI']
        """
        self._field = field
        self._caption = caption
        self._ftype = ftype
        self._options = options

        @property
        def field(self):
            """Field name that will be used in the search"""
            return self._field

        @field.setter
        def field(self, val):
            self._field = val

        @property
        def caption(self):
            """Caption of the field that is used in the search box"""
            return self._caption

        @caption.setter
        def caption(self, val):
            self._caption = val

        @property
        def ftype(self):
            """Type (eg int, text, list, etc) of the field used in search"""
            return self._ftype

        @ftype.setter
        def ftype(self, val):
            self._ftype = val

        @property
        def options(self):
            """Predefined options list to be used with an field for selection"""
            return self._options

        @options.setter
        def options(self, val):
            self._options = val

        def render(self):
            """Renders the search options to be included in the grid"""
            content = "{"
            content += " field: %s, caption: %s, type: %s" % (self._field,
                                                              self._caption, self._type)
            if self._options is not None:
                content += ", options: { items: " + str(self._options) + "}"
            content += "}"
            return content


class GridSearchCollection:
    """A collection of search options of an Grid. All options should be added to
    this class in order to be rendered under an Grid Widget
    """

    _searches = None
    _counter = None

    def __init__(self, searches=None):
        """Default constructor of this class with below parameters

            Args:
                searches (list): A list of searches to be rendered in Grid widget
        """
        if searches is not None:
            self._searches = searches
        else:
            self._searches = []
        self._counter = 1

    @property
    def searches(self):
        return self._searches

    @searches.setter
    def searches(self, val):
        self._searches = val

    @property
    def count(self):
        """Returns the number of searches available in the collection"""
        return self._searches.__len__()

    def add(self, search):
        """Adds an search option in the collection

            Args:
                search (GridSearch): A gird search option to be added
        """
        self._searches.append(search)

    def remove(self, search):
        """Removes an search option from the collection

            Args:
                search: Search to be removed from the collection
        """
        self._searches.pop(search)

    def render(self):
        """Function to render all searches in the JavaScript list format"""
        content = "["
        for search in self._searches:
            content += search.render() + ",\n"
        content += "]"
        return content


class Grid(Widget):
    """A class to render W2UI grid and attach its event to server side events
    .This class works a wrapper of JavaScript and generates JS code to render
    W2UI widget in the browser or app
    """

    _header = None
    _column_collection = None
    _row_collection = None
    _search_collection = None
    _data_url = None
    _tool_bar = None
    _toolbarAdd = None
    _toolbarDelete = None
    _toolbarSave = None
    _toolbarEdit = None
    _toolbar_add_client_script = None
    _toolbar_add_callback = None
    _toolbar_delete_client_script = None
    _toolbar_delete_callback = None
    _toolbar_save_client_script = None
    _toolbar_save_callback = None
    _toolbar_delete_client_callback = None
    _toolbar_delete_callback = None
    _footer = None
    _sort_on = None
    _sort_dir = None
    _data_load_callback = None
    _app = None
    _onclick_callback = None
    _onclick_url = None
    _disabled = None
    _select_column = None
    _multi_select = None
    _line_numbers = None
    _queue = None
    _multi_search = None
    _toolbar_add_url = None
    _toolbar_delete_url = None
    _toolbar_save_url = None
    _toolbar_edit_url = None

    def __init__(self, name, header, column_collection, row_collection=None, desc=None,  # noqa
                 prop=None, style=None, attr=None, disabled=False, onclick_callback=None,
                 app=None, css_cls=None, data_url=None, data_load_callback=None,
                 toolbar=None, footer=None, sort_on=None, sort_dir=None, select_column=None,
                 multi_select=None, line_numbers=None, search_collection=None, multi_search=None,
                 toolbarAdd=None, toolbarDelete=None, toolbarSave=None, toolbarEdit=None,
                 toolbar_add_client_script=None, toolbar_add_callback=None,
                 toolbar_delete_client_script=None, toolbar_delete_callback=None,
                 toolbar_save_client_script=None, toolbar_save_callback=None,
                 toolbar_edit_client_script=None, toolbar_edit_callback=None):
        """Default constructor of the Button widget class

            Args:
                name (string): name of the widget for internal use
                header (string): title of the Grid widget
                column_collection (GridColumnCollection): A list of GridColumns to be rendered
                row_collection (GridRecordCollection): A list of grid records or rows
                desc (string): description of the button widget OPTIONAL!
                prop (dict): dict of objects to be added as properties of widget
                style (dict): dict of objects to be added as style elements to HTML tag
                attr (list): list of objects to be added as attributes of HTML tag
                disabled (Boolean): Enabled or Disabled state of widget
                onclick_callback (function): A function to be called back on onclick event
                app (Flask): An instance of Flask class
                css_cls (list): An list of CSS class names to be added to current widget
                data_url (string): A URL to fetch records to be shown in grid
                data_load_callback (callable): A callback to get the data in GridRecordCollection
                toolbar (Boolean): Whether to show toolbar for the grid or not
                footer (boolean): Whether to show footer in the grid or not
                sort_on (string): The field name on which sorting should be done
                sort_dir (string): Whether to sort in ASC or DSC order
                select_column (boolean): Allows to select a column or not
                multi_select (boolean): Allows to select multiple records or not
                line_numbers (boolean): Shows line number in each row or record
                search_collection (GridSearchCollection): A list of search option
                multi_search (boolean): Wether to all multi field search or not
                toolbarAdd (boolean): Show or hide the Add button in toolbar
                toolbarDelete (boolean): Show or hide the Delete button in toolbar
                toolbarSave (boolean): Show or hide the Save button in toolbar
                toolbarEdit (boolean): Show or hide the Edit button in toolbar
                toolbar_add_client_script (string): JS script to be added for execution at client
                toolbar_add_callback (callable): It will be called at server side when add button is clicked
                toolbar_delete_client_script (string): JS script to be added for execution at client
                toolbar_delete_callback (callable): It will be called at server side when delete button is clicked
                toolbar_save_client_script (string): JS script to be added for execution at client
                toolbar_save_callback (callable): It will be called at server side when save button is clicked
                toolbar_edit_client_script (string): JS script to be added for execution at client
                toolbar_edit_callback (callable): It will be called at server side when edit button is clicked
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        self._header = header
        self._column_collection = column_collection
        self._row_collection = row_collection
        self._search_collection = search_collection
        self.add_style("width", "100%")
        self.add_style("height", "100%")
        self._app = app
        self._disabled = disabled
        self._onclick_callback = onclick_callback
        self._data_url = data_url
        self._data_load_callback = data_load_callback
        if toolbar is not None:
            self._tool_bar = toolbar
        else:
            self._tool_bar = False
        if footer is not None:
            self._footer = footer
        else:
            self._footer = False
        if sort_on is not None:
            self._sort_on = sort_on
        else:
            self._sort_on = 'recid'
        if sort_dir is not None:
            self._sort_dir = sort_dir
        else:
            self._sort_dir = 'ASC'
        if select_column is not None:
            self._select_column = select_column
        else:
            self._select_column = True
        if multi_select is not None:
            self._multi_select = multi_select
        else:
            self._multi_select = False
        if line_numbers is not None:
            self._line_numbers = line_numbers
        else:
            self._line_numbers = False
        if multi_search is not None:
            self._multi_search = multi_search
        else:
            self._multi_search = False
        self._queue = []
        if toolbarAdd is not None:
            self._toolbarAdd = toolbarAdd
        else:
            self._toolbarAdd = False
        if toolbarDelete is not None:
            self._toolbarDelete = toolbarDelete
        else:
            self._toolbarDelete = False
        if toolbarSave is not None:
            self._toolbarSave = toolbarSave
        else:
            self._toolbarSave = False
        if toolbarEdit is not None:
            self._toolbarEdit = toolbarEdit
        else:
            self._toolbarEdit = False
        if toolbar_add_client_script is not None:
            self._toolbar_add_client_script = toolbar_add_client_script
        else:
            self._toolbar_add_client_script = ""
        self._toolbar_add_callback = toolbar_add_callback
        if toolbar_delete_client_script is not None:
            self._toolbar_delete_client_script = toolbar_delete_client_script
        else:
            self._toolbar_delete_client_script = ""
        self._toolbar_delete_callback = toolbar_delete_callback
        if toolbar_save_client_script is not None:
            self._toolbar_save_client_script = toolbar_save_client_script
        else:
            self._toolbar_save_client_script = ""
        self._toolbar_save_callback = toolbar_save_callback
        if toolbar_edit_client_script is not None:
            self._toolbar_edit_client_script = toolbar_edit_client_script
        else:
            self._toolbar_edit_client_script = ""
        self._toolbar_edit_callback = toolbar_edit_callback

    def _attach_script(self):
        self._load_toolbar_urls()
        script = ""
        if self._data_url is None and self._data_load_callback is None:
            script = """
                    <script>
                        $2(function(){
                            $2('#%s').w2grid({
                                name: '%s',
                                header: '%s',
                                columns: %s,
                                records: %s,
                                show: {
                                    toolbar: %s,
                                    footer: %s,
                                    selectColumn: %s,
                                    lineNumbers: %s,
                                    toolbarAdd: %s,
                                    toolbarDelete: %s,
                                    toolbarSave: %s,
                                    toolbarEdit: %s
                                },
                                multiSelect: %s,
                                onClick: function(event){
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onAdd: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onEdit: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onDelete: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onSave: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                sortData: [{field: '%s', direction: '%s'}],
                                multiSearch: %s
                                %s  //searches placeholder
                            });
                        });
                    </script>
                """ % (self._name, self._name, self._header, self._column_collection.render(),
                       self._row_collection.render() if self._row_collection is not None else "",
                       json.dumps(self._tool_bar), json.dumps(self._footer),
                       json.dumps(self._select_column), json.dumps(self._line_numbers),
                       json.dumps(self._toolbarAdd), json.dumps(self._toolbarDelete),
                       json.dumps(self._toolbarSave), json.dumps(self._toolbarEdit),
                       json.dumps(self._multi_select),
                       self._onclick_url,
                       self._toolbar_add_client_script,
                       self._toolbar_add_url,
                       self._toolbar_edit_client_script,
                       self._toolbar_edit_url,
                       self._toolbar_delete_client_callback,
                       self._toolbar_delete_url,
                       self._toolbar_save_client_script,
                       self._toolbar_save_url,
                       self._sort_on, self._sort_dir,
                       json.dumps(self._multi_search),
                       (", searches: " + self._search_collection if self._search_collection is not None else ""))
        elif self._data_url is not None and self._data_load_callback is None:
            script = """
                    <script>
                        $2(function(){
                            $2('#%s').w2grid({
                                name: '%s',
                                header: '%s',
                                columns: %s,
                                method: "GET",
                                url: '%s',
                                show: {
                                    toolbar: %s,
                                    footer: %s,
                                    selectColumn: %s,
                                    lineNumbers: %s,
                                    toolbarAdd: %s,
                                    toolbarDelete: %s,
                                    toolbarSave: %s,
                                    toolbarEdit: %s
                                },
                                multiSelect: %s,
                                onClick: function(event){
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onAdd: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onEdit: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onDelete: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onSave: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                sortData: [{field: '%s', direction: '%s'}],
                                multiSearch: %s
                                %s  //searches placeholder
                            });
                        });
                    </script>
                    """ % (self._name, self._name, self._header, self._column_collection.render(),
                           self._data_url, json.dumps(self._tool_bar), json.dumps(self._footer),
                           json.dumps(self._select_column), json.dumps(self._line_numbers),
                           json.dumps(self._toolbarAdd), json.dumps(self._toolbarDelete),
                           json.dumps(self._toolbarSave), json.dumps(self._toolbarEdit),
                           json.dumps(self._multi_select),
                           self._onclick_url,
                           self._toolbar_add_client_script,
                           self._toolbar_add_url,
                           self._toolbar_edit_client_script,
                           self._toolbar_edit_url,
                           self._toolbar_delete_client_callback,
                           self._toolbar_delete_url,
                           self._toolbar_save_client_script,
                           self._toolbar_save_url,
                           self._sort_on, self._sort_dir,
                           json.dumps(self._multi_search),
                           (", searches: " + self._search_collection if self._search_collection is not None else ""))
        elif self._data_url is None and self._data_load_callback is not None:
            url = str(__name__ + "_" + self._name + "_data_load").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            script = """
                    <script>
                        $2(function(){
                            $2('#%s').w2grid({
                                name: '%s',
                                header: '%s',
                                columns: %s,
                                method: "GET",
                                url: '%s',
                                show: {
                                    toolbar: %s,
                                    footer: %s,
                                    selectColumn: %s,
                                    lineNumbers: %s,
                                    toolbarAdd: %s,
                                    toolbarDelete: %s,
                                    toolbarSave: %s,
                                    toolbarEdit: %s
                                },
                                multiSelect: %s,
                                onClick: function(event){
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onAdd: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onEdit: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onDelete: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                onSave: function (event) {
                                    %s
                                    //AJAX to fire callbacks
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        //data: {'data': event},
                                        success: function(){},
                                        error: function(){
                                                    alertify.error("Status Code: "
                                                    + err_status.status + "<br />" + "Error Message:"
                                                    + err_status.statusText);
                                        }
                                    });
                                },
                                sortData: [{field: '%s', direction: '%s'}],
                                multiSearch: %s
                                %s  //searches placeholder
                            });
                        });
                    </script>
                    """ % (self._name, self._name, self._header, self._column_collection.render(),
                           url, json.dumps(self._tool_bar), json.dumps(self._footer),
                           json.dumps(self._select_column), json.dumps(self._line_numbers),
                           json.dumps(self._toolbarAdd), json.dumps(self._toolbarDelete),
                           json.dumps(self._toolbarSave), json.dumps(self._toolbarEdit),
                           json.dumps(self._multi_select),
                           self._onclick_url,
                           self._toolbar_add_client_script,
                           self._toolbar_add_url,
                           self._toolbar_edit_client_script,
                           self._toolbar_edit_url,
                           self._toolbar_delete_client_callback,
                           self._toolbar_delete_url,
                           self._toolbar_save_client_script,
                           self._toolbar_save_url,
                           self._sort_on, self._sort_dir,
                           json.dumps(self._multi_search),
                           (", searches: " + self._search_collection if self._search_collection is not None else ""))
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_data_load_callback)
        return script

    def _load_toolbar_urls(self):  # noqa
            # Toolbar Add Url
            self._onclick_url = str(__name__ + "_" + self._name + "_grid_onclick").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == self._onclick_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + self._onclick_url, self._onclick_url,
                                       self._process_onclick_callback)
            # Toolbar Add Url
            self._toolbar_add_url = str(__name__ + "_" + self._name + "_toolbar_add").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == self._toolbar_add_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + self._toolbar_add_url, self._toolbar_add_url,
                                       self._process_toolbar_add_callback)
            # Toolbar Delete Url
            self._toolbar_delete_url = str(__name__ + "_" + self._name + "_toolbar_delete").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == self._toolbar_delete_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + self._toolbar_delete_url, self._toolbar_delete_url,
                                       self._process_toolbar_delete_callback)
            # Toolbar Edit Url
            self._toolbar_edit_url = str(__name__ + "_" + self._name + "_toolbar_edit").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == self._toolbar_edit_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + self._toolbar_edit_url, self._toolbar_edit_url,
                                       self._process_toolbar_edit_callback)
            # Toolbar Save Url
            self._toolbar_save_url = str(__name__ + "_" + self._name + "_toolbar_save").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == self._toolbar_save_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + self._toolbar_save_url, self._toolbar_save_url,
                                       self._process_toolbar_save_callback)

    def _process_onclick_callback(self):
        if self._onclick_callback is not None:
            return json.dumps({'result': self._onclick_callback()})
        return json.dumps({'result': ''})

    def _process_data_load_callback(self):
        record_collection = self._data_load_callback()
        self._row_collection = record_collection
        result = "{\n'total': " + record_collection.records.__len__() + ",\n"
        result += "'records': " + record_collection.render()
        return result

    def _process_toolbar_add_callback(self):
        if self._toolbar_add_callback is not None:
            return json.dumps({'result': self._toolbar_add_callback()})
        return json.dumps({'result': ''})

    def _process_toolbar_edit_callback(self):
        if self._toolbar_edit_callback is not None:
            return json.dumps({'result': self._toolbar_edit_callback()})
        return json.dumps({'result': ''})

    def _process_toolbar_delete_callback(self):
        if self._toolbar_delete_callback is not None:
            return json.dumps({'result': self._toolbar_delete_callback()})
        return json.dumps({'result': ''})

    def _process_toolbar_save_callback(self):
        if self._toolbar_save_callback is not None:
            return json.dumps({'result': self._toolbar_save_callback()})
        return json.dumps({'result': ''})

    def toggle_column(self, col_name):
        """Toggles the visibility of an column in the grid

            Args:
                col_name: Name of the column that needs to be toggled
        """
        self._queue.append({'cmd': 'HIDE', 'arg0': col_name})

    def add_record(self, record):
        """Adds an record to the grid

            Args:
                record (GridRecord): An record of GridRecord type
        """
        rec_count = self._row_collection.count
        self._row_collection.add(record)
        record.add_cell('recid', rec_count + 1)
        self._queue.append({'cmd': 'ADD-RECORD', 'arg0': record.render()})

    def select_all_records(self):
        """Selects all the records available in the Grid Widget"""
        self._queue.append({'cmd': 'SELECT-ALL'})

    def unselect_all_records(self):
        """Selects all the records available in the Grid Widget"""
        self._queue.append({'cmd': 'UNSELECT-ALL'})

    def select_records(self, records):
        """Selects all the records available in the Grid Widget

            Args:
                records (string): A comma seperated string containing records to select
                                    e.g., "2,3,5" or "5"
        """
        self._queue.append({'cmd': 'SELECT', 'arg0': records})

    def unselect_records(self, records):
        """Selects all the records available in the Grid Widget

            Args:
                records (string): A comma seperated string containing records to select
                                    e.g., "2,3,5" or "5"
        """
        self._queue.append({'cmd': 'UNSELECT', 'arg0': records})

    def _sync_properties(self):
        if self._queue.__len__() > 0:
            cmd = self._queue.pop()
            return json.dumps(cmd)
        return json.dumps({'result': ''})
        # if cmd['cmd'] == "HIDE":
        #     return json.dumps(cmd)
        # if cmd['cmd'] == "ADD-RECORD":
        #     return json.dumps(cmd)

    def _attach_polling(self):
        if self._app is None:
            return
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                    (function %s_poll(){
                        setTimeout(function(){
                            $.ajax({
                                url: "/%s",
                                dataType: "json",
                                success: function(props){
                                    selector = $("#%s");
                                    if(selector != undefined){
                                        if(props.cmd != undefined){
                                            if(props.cmd == "HIDE"){
                                                w2ui.grid.toggleColumn(props.arg0);
                                            }
                                            if(props.cmd == "ADD-RECORD"){
                                                w2ui['%s'].add(props.arg0);
                                            }
                                            if(props.cmd == "SELECT-ALL"){
                                                w2ui.grid.selectAll();
                                            }
                                            if(props.cmd == "UNSELECT-ALL"){
                                                w2ui.grid.selectNone();
                                            }
                                            if(props.cmd == "SELECT"){
                                                w2ui.grid.select(props.arg0);
                                            }
                                            if(props.cmd == "UNSELECT"){
                                                w2ui.grid.unselect(props.arg0);
                                            }
                                        } else {
                                            alertify.warning("No command to process");
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
                """ % (url, url, self._name, self._name, url)
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == url:
                found = True
        if not found:
            self._app.add_url_rule('/' + url, url, self._sync_properties)
        return script

    def render(self):
        content = self._render_pre_content('div')
        content += self._render_post_content('div') + "\n"
        content += self._attach_script() + "\n" + self._attach_polling()
        return content


class ToolbarButton(Widget):
    """Shows a simple button with text or icon or both"""

    _name = None
    _title = None
    _icon = None
    _type = None
    _group = None

    def __init__(self, name, title=None, icon=None, group=None):
        """Default constructor parameters

            Args:
                name (string): An id or name of button to be used internally
                title (string, optional): Title of the button, if not provided, icon parm should have value
                icon (string, optional): Icon to be shown on the widget. If not provided, title should have some value
                group (string, optional): used by widgets like radiobutton to group wiidgets together
        """
        self._name = name
        self._title = title
        self._icon = icon
        self._type = "button"
        self._group = group
        if title is None and icon is None:
            raise ValueError("Either Title or Icon param should have value")

    @property
    def name(self):
        """Id or name of the widget"""
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def title(self):
        """Title of the widget"""
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def icon(self):
        """Icon to be used by the widget """
        return self._icon

    @icon.setter
    def icon(self, val):
        self._icon = val

    @property
    def group(self):
        """Groups widget under one Group"""
        return self._group

    @group.setter
    def group(self, val):
        return self._group

    def render(self):
        """Renders the widget under parent widget"""
        content = "{"
        content += "type: '" + self._type + "', "
        content += "id: '" + self._name + "', "
        if self._title is not None:
            content += "text: '" + self._title + "', "
        if self._icon is not None:
            content += "icon: '" + self._icon + "', "
        if self._group is not None:
            content += "group: '" + self._group + "', "
        content += "}"
        return content


class ToolbarCheck(ToolbarButton):
    """Adds an chexkbox widget to the toolbar """

    def __init__(self, name, title=None, icon=None, group=None):
        ToolbarButton.__init__(self, name, title, icon, group)
        self._type = "check"


class ToolbarRadio(ToolbarButton):
    """Adds an Radio button widget to the toolbar """

    def __init__(self, name, title=None, icon=None, group=None):
        ToolbarButton.__init__(self, name, title, icon, group)
        self._type = "radio"


class ToolbarSeparator(ToolbarButton):
    """Adds an separator widget to the toolbar """

    def __init__(self, name, title=None, icon=None, group=None):
        ToolbarButton.__init__(self, name, title, icon, group)
        self._type = "break"


class ToolbarSpacer(ToolbarButton):
    """Adds an spacer widget to the toolbar """

    def __init__(self, name, title=None, icon=None, group=None):
        ToolbarButton.__init__(self, name, title, icon, group)
        self._type = "spacer"


class ToolbarMenu(ToolbarButton):
    """Adds an menu widget and its subitems to toolbar
    """

    _count = None
    _items = None

    def __init__(self, name, title=None, icon=None, group=None, count=None, items=None):
        ToolbarButton.__init__(self, name, title, icon, group)
        if count is None:
            if items is not None and items.__len__() > 0:
                self._count = items.__len__()
            else:
                self._count = 0
        else:
            self._count = count
        if items is not None:
            self._items = items
        else:
            self._items = []
        self._type = 'menu'

    def add_item(self, text, icon=None, count=None, disabled=None):
        item = "{ text: '" + text + "', "
        if icon is not None:
            item += "icon: '" + icon + "', "
        if count is not None:
            item += "count: " + str(count) + ", "
        if disabled is not None and disabled:
            item += "disabled: true "
        item += "}"
        self._items.append(item)

    def render(self):
        items = "[\n"
        for itm in self._items:
            items += itm + ",\n"
        items += "\n]"
        content = "{ type: '" + self._type + "', "
        content += "id: '" + self._name + "', "
        if self._title is not None:
            content += "text: '" + self._title + "', "
        if self._icon is not None:
            content += "icon: '" + self._icon + "', "
        if self._count is not None:
            content += "count: " + str(self._count) + ", "
        if self._items is not None:
            content += "items: " + items
        content += "}"
        return content


class ToolbarMenuRadio(ToolbarMenu):
    """Adds an dropdown menu of radio buttons for selection. The selected radio button will
    appear as the text of the dropdown menu
    """

    def __init__(self, name, title=None, icon=None, group=None, count=None, items=None):
        ToolbarMenu.__init__(self, name, title, icon, group, count, items)
        self._type = 'menu-radio'

    def add_item(self, id, text, icon=None):
        item = "{ id: '" + id + "', "
        item += "text: '" + text + "', "
        if icon is not None:
            item += "icon: '" + icon + "', "
        item += "}"
        self._items.append(item)

    def render(self):
        items = "[\n"
        for itm in self._items:
            items += itm + ",\n"
        items += "\n]"
        content = "{ type: '" + self._type + "', "
        content += "id: '" + self._name + "', "
        if self._title is not None:
            content += "text: '" + self._title + "', "
            # content += """\ntext: function(item){
            #                 var text = item.selected;
            #                 var el = this.get('%s:' + item.selected);
            #                 return '%s: (' + el.txt + ')';
            #             },\n
            #            """ % (self._name, self._title)
        if self._icon is not None:
            content += "icon: '" + self._icon + "', "
        # if self._count is not None:
        #     content += "count: " + str(self._count) + ", "
        if self._items is not None:
            content += "items: " + items
        content += "}"
        return content


class ToolbarMenuCheck(ToolbarMenu):
    """Adds an dropdown menu of radio buttons for selection. The selected radio button will
    appear as the text of the dropdown menu
    """

    def __init__(self, name, title=None, icon=None, group=None, count=None, items=None):
        ToolbarMenu.__init__(self, name, title, icon, group, count, items)
        self._type = 'menu-check'

    def add_item(self, id, text, icon=None):
        item = "{ id: '" + id + "', "
        item += "text: '" + text + "', "
        if icon is not None:
            item += "icon: '" + icon + "', "
        item += "}"
        self._items.append(item)


class ToolbarDropDown(ToolbarButton):
    """Shows a dropdown panel having its content filled with user supplied HTML. This can
    be used to shown information, pictures, forms, etc
    """

    _html = None

    def __init__(self, name, html, title=None, icon=None, group=None):
        ToolbarButton.__init__(self, name, title, icon, group)
        self._html = html
        self._type = 'drop'

    def render(self):
        """Renders the widget under parent widget"""
        content = "{"
        content += "type: '" + self._type + "', "
        content += "id: '" + self._name + "', "
        content += "html: '" + self._html + "', "
        if self._title is not None:
            content += "text: '" + self._title + "', "
        if self._icon is not None:
            content += "icon: '" + self._icon + "', "
        if self._group is not None:
            content += "group: '" + self._group + "', "
        content += "}"
        return content


class ToolbarHTML(ToolbarDropDown):
    """Shows a panel having its content filled with the user supplied HTML. It is similr
    to `ToolbarDropDown` but it shows the HTML inplace of title. So this item don't
    have any dropdown to show its content
    """

    def __init__(self, name, html, title=None, icon=None):
        ToolbarDropDown.__init__(self, name, html, title=title, icon=icon, group=None)
        self._type = 'html'


class Toolbar(Widget):
    """A toolbar having collection of buttons, chexkbox,
    radio buttons, separaters, etc. An toolbar item can
    have title or button or both
    """

    _onclick_callback = None
    _onclick_client_script = None
    _app = None
    _clicked_item = None
    _queue = None

    def __init__(self, name, items=None, onclick_callback=None, onclick_client_script=None, app=None):
        """
            name (string): Name or Id for internal use
            items (Widget): Child items like, ToolbarButton, ToolbarRadio, etc
            onclick_callback (callable): will be called when mouse is clicked on any child item
            onclick_client_script (string): JS to be called when mouse is clicked on any item
            app (Flask): An instance of Flask app
        """
        Widget.__init__(self, name)
        if items is not None:
            self._child_widgets = items
        else:
            self._child_widgets = []
        self._onclick_callback = onclick_callback
        if onclick_client_script is not None:
            self._onclick_client_script = onclick_client_script
        else:
            self._onclick_client_script = ""
        self._app = app
        self._queue = {}

    def add_item(self, item):
        """Adds a new item to the toolbar passed as argument

            Args:
                item (ToolbarButton): An instance of ToolbarButton or its subclasses
        """
        self._queue.append({'cmd': 'ADD-ITEM', 'arg0': item.render()})

    def insert_item(self, item, ref_item):
        """Inserts a new item to the toolbar after the specified referenced item

            Args:
                item (ToolbarButton): Instance of ToolbarButton or its subclasses
                ref_item (string): Id or name of the item after which new item should be
                                    inserted
        """
        self._queue.append({'cmd': 'INSERT-ITEM', 'arg0': item.render(), 'ref': ref_item})

    def remove_item(self, index_of_item):
        """Removes an item from the toolbar available at the specified index location

            Args:
                index_of_item (int): Index of item that needs to be removed from toolbar
        """
        self._queue.append({'cmd': 'REMOVE-ITEM', 'arg0': index_of_item})

    def show_item(self, item_name):
        """Shows an item which was in hidden state previously

            Args:
                item_name (string): Name or Id of the toolbar item that needs to be set visible
        """
        self._queue.append({'cmd': 'SHOW-ITEM', 'arg0': item_name})

    def hide_item(self, item_name):
        """Hides an visible item available on the toolbar

            Args:
                item_name (string): Name or Id of the toolbar item that needs to be set as hidden
        """
        self._queue.append({'cmd': 'HIDE-ITEM', 'arg0': item_name})

    def enable_item(self, item_name):
        """Enables an visible toollbar item if its has been set as disiabled

            Args:
                item_name (string): Name or Id of item that needs to be enabled
        """
        self._queue.append({'cmd': 'ENABLE-ITEM', 'arg0': item_name})

    def disable_item(self, item_name):
        """Disable an visible toolbar item which is already in enabled state

            Args:
                item_name (string): Name or Id of the item that needs to be disabled
        """
        self._queue.append({'cmd': 'DISABLE-ITEM', 'arg0': item_name})

    def _sync_properties(self):
        if self._queue.__len__() > 0:
            cmd = self._queue.pop()
            return json.dumps(cmd)
        return json.dumps({'result': ''})

    def _attach_polling(self):
        if self._app is None:
            return
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                    (function %s_poll(){
                        setTimeout(function(){
                            $.ajax({
                                url: "/%s",
                                dataType: "json",
                                success: function(props){
                                    selector = w2ui['%s'];
                                    if(selector != undefined){
                                        if(props.cmd != undefined){
                                            if(props.cmd == "HIDE-ITEM"){
                                                selector.hide(props.arg0);
                                            }
                                            if(props.cmd == "SHOW-ITEM"){
                                                selector.show(props.arg0);
                                            }
                                            if(props.cmd == "ENABLE-ITEM"){
                                                selector.enable(props.arg0);
                                            }
                                            if(props.cmd == "DISABLE-ITEM"){
                                                selector.disable(props.arg0);
                                            }
                                            if(props.cmd == "ADD-ITEM"){
                                                selector.add(props.arg0);
                                            }
                                            if(props.cmd == "INSERT-ITEM"){
                                                selector.insert(props.ref, props.arg0);
                                            }
                                            if(props.cmd == "REMOVE-ITEM"){
                                                selector.remove(props.arg0);
                                            }
                                        } else {
                                            alertify.warning("No command to process");
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
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == url:
                found = True
        if not found:
            self._app.add_url_rule('/' + url, url, self._sync_properties)
        return script

    def _attach_script(self):
        url = ""
        if self._app is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + url, url, self._process_onclick_callback)
        child_widgets = "[\n"
        for child in self._child_widgets:
            child_widgets += child.render() + ",\n"
        child_widgets += "\n]"
        script = """
                <script>
                    $2(function(){
                        $2('#%s').w2toolbar({
                            name: '%s',
                            items: %s,
                            onClick: function(event){
                                %s
                                $2.ajax({
                                    url: '/%s',
                                    type: 'get',
                                    data: {'target': event.target},
                                    dataType: 'json',
                                    success: function(status){},
                                    error: function(err_status){
                                        alertify.error("Status Code: "
                                        + err_status.status + "<br />" + "Error Message:"
                                        + err_status.statusText);
                                    }
                                });
                            }
                        });
                    });
                </script>
                """ % (self._name, self._name, child_widgets, self._onclick_client_script, url)
        return script

    def _process_onclick_callback(self):
        if request.args.__len__() > 0:
            val = request.args['target']
            if val is not None:
                self._clicked_item = val
        if self._onclick_callback is not None:
            return json.dumps({'result': self._onclick_callback()})
        return json.dumps({'result': ''})

    @property
    def clicked_item(self):
        """Contains the name / id of item where mouse was clicked (i.e., the item which received the mouse
        click event)"""
        return self._clicked_item

    @clicked_item.setter
    def clicked_item(self, val):
        self._clicked_item = val

    def render(self):
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += "\n" + self._attach_script()
        content += "\n" + self._attach_polling()
        self._widget_content = content
        return self._widget_content


class SidebarNode(Widget):
    """A node within the sidebar widget. A node can have text, icon and sub-nodes
    Further a node can have expanded or collapsed state. It sub-nodes can be grouped
    under a one group. Any sidebar node can have a number of leaves which further
    can't have any child nodes
    """

    _name = None
    _text = None
    _icon = None
    _is_leaf = None
    _expanded = None
    _img = None
    _group = None
    _count = None
    # _nodes = None

    def __init__(self, name, text=None, icon=None, is_leaf=None, expanded=None,
                 img=None, group=None, count=None, nodes=None):
        Widget.__init__(self, name)
        self._text = text
        self._icon = icon
        if is_leaf is not None:
            self._is_leaf = is_leaf
        else:
            self._is_leaf = False
        if expanded is not None:
            self._expanded = expanded
        else:
            self._expanded = False
        self._img = img
        self._group = group
        self._count = count
        if nodes is not None:
            self._child_widgets = nodes
            # self._nodes = nodes
        else:
            # self._nodes = []
            self._child_widgets = []
        if is_leaf:
            if text is None and icon is None:
                raise ValueError("Either text or icon should have a value for an leaf")
        else:
            if text is None and img is None:
                raise ValueError("Either text or img should have a value for an node")

    @property
    def is_leaf(self):
        """Property which defines whether the current node is an leaf or a sub-node
        """
        return self._is_leaf

    @is_leaf.setter
    def is_leaf(self, val):
        self._is_leaf = val

    # def add(self, node, is_leaf=False):
    #     """Adds an subnode or a leaf to the current node

    #         Args:
    #             node (SidebarNode): An instance of sidebar node as a leaf or node
    #     """
    #     node.is_leaf = is_leaf
    #     self._nodes.append(node)

    # def remove(self, node):
    #     """Removes an node from the current node

    #         Args:
    #             node (SidebarNode): An instance of sidebar node
    #     """
    #     self._nodes.remove(node)

    def render(self):
        """Renders an node or leaf depending upon the value of `is_leaf' attribute
        """
        content = ""
        if self._is_leaf:
            content += "{ id: '" + self._name + "', "
            if self._text is not None:
                content += "text: '" + self._text + "', "
            if self._icon is not None:
                content += "icon: '" + self._icon + "', "
            if self._count is not None:
                content += "count: " + self._count + ", "
            content += "}"
            return content
        else:
            content += "{ id: '" + self._name + "', "
            if self._text is not None:
                content += "text: '" + self._text + "', "
            if self._img is not None:
                content += "img: '" + self._img + "', "
            if self._expanded is not None:
                content += "expanded: " + json.dumps(self._expanded) + ", "
            if self._group is not None:
                content += "group: " + json.dumps(self._group) + ", "
            if self._count is not None:
                content += "count: " + self._count + ", "
            if self._child_widgets is not None:
                content += "nodes: [\n"
                for node in self._child_widgets:
                    content += node.render() + ",\n"
                content += "]"
            content += "}"
            return content
        return content


class Sidebar(Widget):
    """The w2sidebar object provides a quick solution for a vertical menu. A sidebar can have
    multiple items and some of the items can be nested. The very same object can be used to create
    tree structures too.
    """

    _onclick_callback = None
    _onclick_client_script = None
    _app = None
    _topHTML = None
    _bottomHTML = None
    _flatButton = None
    _clicked_item = None

    def __init__(self, name, nodes=None, onclick_callback=None, onclick_client_script=None, app=None,
                 topHTML=None, bottomHTML=None, flatButton=None):
        """
            name (string): Name or Id for internal use
            nodes (Widget): Sub Nodes or leaves of the current node
            onclick_callback (callable): will be called when mouse is clicked on any child item
            onclick_client_script (string): JS to be called when mouse is clicked on any item
            app (Flask): An instance of Flask app
            topHTML (string): HTML to show at the top of the sidebar
            bottomHTML (string): HTML to be shown on the bottom of sidebar
            flatButton (boolean): If true, it will show button to minimize or flat the sidebar
        """
        Widget.__init__(self, name)
        if nodes is not None:
            self._child_widgets = nodes
        else:
            self._child_widgets = []
        self._onclick_callback = onclick_callback
        self._onclick_client_script = onclick_client_script
        self._app = app
        if topHTML is not None:
            self._topHTML = topHTML
        else:
            self._topHTML = ""
        if bottomHTML is not None:
            self._bottomHTML = bottomHTML
        else:
            self._bottomHTML = ""
        if flatButton is not None:
            self._flatButton = flatButton
        else:
            self._flatButton = False
        self.add_style("height", "500px")
        self.add_style("width", "200px")

    @property
    def clicked_item(self):
        """The sidebar item which was clicked"""
        return self._clicked_item

    @clicked_item.setter
    def clicked_item(self, val):
        self._clicked_item = val

    def _process_onclick_callback(self):
        if request.args.__len__() > 0:
            val = request.args['target']
            if val is not None:
                self._clicked_item = val
        if self._onclick_callback is not None:
            return json.dumps({'result': self._onclick_callback()})
        return json.dumps({'result': ''})

    def _attach_script(self):
        url = ""
        if self._app is not None:
            url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + url, url, self._process_onclick_callback)
        child_widgets = "[\n"
        for child in self._child_widgets:
            child_widgets += child.render() + ",\n"
        child_widgets += "\n]"
        script = """
                    <script>
                        $2(function(){
                            $2('#%s').w2sidebar({
                                name: '%s',
                                flatButton: %s,
                                topHTML: '%s',
                                bottomHTML: '%s',
                                nodes: %s,
                                onFlat: function(event){
                                    $('#%s').css('width', (event.goFlat ? '35px' : '200px'));
                                },
                                onClick: function(event){
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        data: {'target': event.target},
                                        success: function(status){},
                                        error: function(err_status){
                                            alertify.error("Status Code: "
                                            + err_status.status + "<br />" + "Error Message:"
                                            + err_status.statusText);
                                        }
                                    });
                                }
                            });
                        });
                    </script>
                """ % (self._name, self._name, json.dumps(self._flatButton), self._topHTML,
                       self._bottomHTML, child_widgets, self._name, url)
        return script

    def render(self):
        """Renders the sidebar with its nodes and subnodes"""
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += "\n" + self._attach_script()
        return content
