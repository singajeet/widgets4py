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
        """Renders the GridColumn as `dict` object which will be converted to JSON
        for final rendering on the browser
        """
        obj = {}
        obj['field'] = self._field_name
        obj['caption'] = self._caption
        obj['size'] = self._size
        if self._attributes is not None:
            obj['attr'] = self._attributes
        if self._render is not None:
            obj['render'] = self._render
        if self._sortable is not None:
            obj['sortable'] = self._sortable
        return obj


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
        """Collect all the columns and render it as JSON array on the browser"""
        content = []
        for col in self._columns:
            content.append(col.render())
        return json.dumps(content)


class GridRecord:
    """A row or record in the dataset of a Grid widget. This class
    keeps all the fields or cells for an given record along its values.
    The object or instace of this class is rendered as `dict` object,
    which further is converted to JSON by the collection class
    """

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
        """Renders the instance of this class as `dict` object which will be
        further used by the collection class
        """
        obj = {}
        for cell in self._cells:
            obj[cell] = self._cells.get(cell)
        if self._style is not None:
            style = {}
            style['style'] = self._style
            obj['w2ui'] = style
        return obj


class SummaryGridRecord(GridRecord):
    """Renders an summary row at the end of the grid. The cell names should be same as
    available in `GridRecord' but its content should have the summary details. For example,
    if GridRecord have the following columns {'fname': 'Jane', lname: 'Doe', qty: 1000},
    the summary record can have the following structure {'fname': 'Total', qty: '1000'}

    The cell value can have HTML included to format it e.g., {'fname': '<span>Total</span>'}
    """

    def render(self):
        """Renders the summary record as `dict` object. The summary record is always
        rendered as the last record of an Grid widget"""
        summary = {}
        summary['summary'] = True
        obj = {}
        obj['w2ui'] = summary
        for cell in self._cells:
            obj[cell] = self._cells.get(cell)
        return obj


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
        """Function to render all the records in the JSON list format"""
        content = []
        for rec in self._records:
            content.append(rec.render())
        return json.dumps(content)


class GridSearch:
    """Defines an search option for the Grid widget. It contains the information of
    field name, caption, type, etc to define an search option for the Grid
    """

    _field = None
    _caption = None
    _type = None
    _options = None

    def __init__(self, field, caption, fld_type, options=None):
        """Default constructor parameters

            field (string): Name of the existing field in the Grid widget
            caption (string): A title of the field used for search
            fld_type (string): type of the field that will be used to search
            options (dict): shows a predefined options to select in the search toolbar
                            e.g., ['ABC', 'DEF', 'GHI']
        """
        self._field = field
        self._caption = caption
        self._fld_type = fld_type
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
        def fld_type(self):
            """Type (eg int, text, list, etc) of the field used in search"""
            return self._fld_type

        @fld_type.setter
        def fld_type(self, val):
            self._fld_type = val

        @property
        def options(self):
            """Predefined options list to be used with an field for selection"""
            return self._options

        @options.setter
        def options(self, val):
            self._options = val

        def render(self):
            """Renders the search options to be included in the grid"""
            obj = {}
            obj['field'] = self._field
            obj['caption'] = self._caption
            obj['type'] = self._fld_type
            if self._options is not None:
                items = {}
                items['items'] = self._options
                obj['options'] = items
            return json.dumps(obj)


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
        """Function to render the search collection as JSON list format"""
        content = []
        for search in self._searches:
            content.append(search.render())
        return json.dumps(content)


class Grid(Widget):
    """Grid renders the columns and records in crosstab format. Grid can have any number
    of columns and records in the Grid should follow the column structure as defined by
    the collection of columns. The Grid widget can have its data loaded at the server side
    during rendering of the widget or it can be populated dynamically from the client side
    using the callback interface. Grid widget provides the option to perform the CRUD
    (Create, Rename, Update and Delete) operations though the method calls and the AJAX
    framework syncup the data at client side dynamically. Further it provides the options
    to select, filter, search, etc operations and also have events defined which can call
    the methods/callbacks defined at server side.

    This class is an wrapper on top of the Grid widget from W2UI and almost provides all
    the functionalities available in W2UI Grid widget through serve-side method calls.
    Please visit http://www.w2ui.com to get more information about this widget.
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
                toolbar_add_client_script (string): This attribute provides the options to add your
                                                    custom javascript code to be included and
                                                    rendered in the client browser. The script
                                                    can use the JQuery which is already included in
                                                    the module. Use "$" for JQuery version 3.xx or
                                                    use "$2" for version 2.xx. The script will be
                                                    called in browser when the add button event is
                                                    fired
                toolbar_add_callback (callable): This callback will be executed during the Add button
                                                    click event at the server-side. So in case any
                                                    custom action needs to be done at server, same
                                                    can be hooked to this attribute by attaching the
                                                    callback
                toolbar_delete_client_script (string): Same as `toolbar_add_client_script` but is
                                                        executed on "delete" button click event
                toolbar_delete_callback (callable): Same as `toolbar_add_callback` but is called on
                                                    "delete" button click event
                toolbar_save_client_script (string): Same as `toolbar_add_client_script` but is
                                                        executed on "save" button click event
                toolbar_save_callback (callable): Same as `toolbar_add_callback` but is called on
                                                    "save" button click event
                toolbar_edit_client_script (string): Same as `toolbar_add_client_script` but is
                                                        executed on "edit" button click event
                toolbar_edit_callback (callable): Same as `toolbar_add_callback` but is called on
                                                    "edit" button click event
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
        # result = "{\n'total': " + record_collection.records.__len__() + ",\n"
        # result += "'records': " + record_collection.render()
        result = {}
        result['total'] = record_collection.__len__()
        result['records'] = record_collection.render()
        return json.dumps(result)

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

    def _attach_polling(self):
        if self._app is None:
            return
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                    (function %s_poll(){
                        setTimeout(function(){
                            $2.ajax({
                                url: "/%s",
                                dataType: "json",
                                success: function(props){
                                    selector = $2("#%s");
                                    if(selector != undefined){
                                        if(props.cmd != undefined){
                                            if(props.cmd === "HIDE"){
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
                                                w2ui.grid.select(JSON.parse(props.arg0));
                                            }
                                            if(props.cmd == "UNSELECT"){
                                                w2ui.grid.unselect(JSON.parse(props.arg0));
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
        obj = {}
        obj['type'] = self._type
        obj['id'] = self._name
        if self._title is not None:
            obj['text'] = self._title
        if self._icon is not None:
            obj['icon'] = self._icon
        if self._group is not None:
            obj['group'] = self._group
        return json.dumps(obj)


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
        """Renders menu in the toolbar with submenu as its child nodes

            Args:
                name (string, required): A unique identifier for instance of this class
                title (string): Title to be shown on the the menu, if not provided only icon
                                will be visible
                icon (string): An icon CSS class, if not provided only Title will be visible
                group (string): Group menus under one category
                count (int): An integer value that will be shown next to title in the menu
                items (Item): Sub menus or items of this object
        """
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
        """Adds an submenu or item to the instance of main menu class

            Args:
                text (string): Title to be shown on the the menu, if not provided only icon
                                will be visible
                icon (string): An icon CSS class, if not provided only Title will be visible
                count (int): An integer value that will be shown next to title in the menu
                disabled (boolean): Whether to enable or disable the menu item
        """
        item = {}
        item['text'] = text
        if icon is not None:
            item['icon'] = icon
        if count is not None:
            item['count'] = count
        if disabled is not None:
            item['disabled'] = disabled
        self._items.append(item)

    def render(self):
        """Renders the content of Menu as JSON format """
        obj = {}
        obj['type'] = self._type
        obj['id'] = self._name
        if self._title is not None:
            obj['text'] = self._title
        if self._icon is not None:
            obj['icon'] = self._icon
        if self._count is not None:
            obj['count'] = self._count
        if self._items is not None:
            obj['items'] = self._items
        return json.dumps(obj)


class ToolbarMenuRadio(ToolbarMenu):
    """Adds an dropdown menu of radio buttons for selection. The selected radio button will
    appear as the text of the dropdown menu
    """

    def __init__(self, name, title=None, icon=None, group=None, count=None, items=None):
        """Renders menu in the toolbar with radiobuttons as its child nodes

            Args:
                name (string, required): A unique identifier for instance of this class
                title (string): Title to be shown on the the menu, if not provided only icon
                                will be visible
                icon (string): An icon CSS class, if not provided only Title will be visible
                group (string): Group menus under one category
                count (int): An integer value that will be shown next to title in the menu
                items (Item): Sub menus or items of this object
        """
        ToolbarMenu.__init__(self, name, title, icon, group, count, items)
        self._type = 'menu-radio'

    def add_item(self, id, text, icon=None):
        """Adds an radiobutton to the instance of main menu class

            Args:
                id (string, required): A unique identifier for instance of this class
                text (string): Title to be shown on the the menu, if not provided only icon
                                will be visible
                icon (string): An icon CSS class, if not provided only Title will be
                                visible
        """
        obj = {}
        obj['id'] = id
        obj['text'] = text
        if icon is not None:
            obj['icon'] = icon
        self._items.append(obj)

    def render(self):
        """Renders the content of menu with radiobuttons as it child items"""
        obj = {}
        obj['type'] = self._type
        obj['id'] = self._id
        if self._title is not None:
            obj['text'] = self._title
        if self._icon is not None:
            obj['icon'] = self._icon
        if self._items is not None:
            obj['items'] = self._items
        return json.dumps(obj)


class ToolbarMenuCheck(ToolbarMenu):
    """Adds an dropdown menu of checkbox buttons for selection.
    """

    def __init__(self, name, title=None, icon=None, group=None, count=None, items=None):
        """Renders menu in the toolbar with checkboxes as its child nodes

            Args:
                name (string, required): A unique identifier for instance of this class
                title (string): Title to be shown on the the menu, if not provided only icon
                                will be visible
                icon (string): An icon CSS class, if not provided only Title will be visible
                group (string): Group menus under one category
                count (int): An integer value that will be shown next to title in the menu
                items (Item): Sub menus or items of this object
        """
        ToolbarMenu.__init__(self, name, title, icon, group, count, items)
        self._type = 'menu-check'

    def add_item(self, id, text, icon=None):
        """Adds an checkbox to the instance of main menu class

            Args:
                id (string, required): A unique identifier for instance of this class
                text (string): Title to be shown on the the menu, if not provided only icon
                                will be visible
                icon (string): An icon CSS class, if not provided only Title will be
                                visible
        """
        item = {}
        item['id'] = id
        item['text'] = text
        if icon is not None:
            item['icon'] = icon
        self._items.append(item)


class ToolbarDropDown(ToolbarButton):
    """Shows a dropdown panel having its content filled with user supplied HTML. This can
    be used to shown information, pictures, forms, etc
    """

    _html = None

    def __init__(self, name, html, title=None, icon=None, group=None):
        """Below are the parameters for this class's constructor

            Args:
                name (string, required): A unique identifier for instance of this class
                html (string): An HTML to be displayed inside of the dropdown box
                title (string): Title to be shown on the the menu, if not provided only icon
                                will be visible
                icon (string): An icon CSS class, if not provided only Title will be visible
                group (string): Group menus under one category
        """
        ToolbarButton.__init__(self, name, title, icon, group)
        self._html = html
        self._type = 'drop'

    def render(self):
        """Renders the widget under parent widget"""
        obj = {}
        obj['type'] = self._type
        obj['id'] = self._id
        obj['html'] = self._html
        if self._title is not None:
            obj['text'] = self._title
        if self._icon is not None:
            obj['icon'] = self._icon
        if self._group is not None:
            obj['group'] = self._group
        return json.dumps(obj)


class ToolbarHTML(ToolbarDropDown):
    """Shows a panel having its content filled with the user supplied HTML. It is similr
    to `ToolbarDropDown` but it shows the HTML inplace of title. So this item don't
    have any dropdown to show its content
    """

    def __init__(self, name, html, title=None, icon=None):
        """Below are the parameters for this class's constructor

            Args:
                name (string, required): A unique identifier for instance of this class
                html (string): An HTML to be displayed inside of the dropdown box
                title (string): Title to be shown on the the menu, if not provided only icon
                                will be visible
                icon (string): An icon CSS class, if not provided only Title will be visible
                group (string): Group menus under one category
        """
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
            Args:
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
        self._queue = []

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
                            $2.ajax({
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
                                                selector.add(JSON.parse(props.arg0));
                                            }
                                            if(props.cmd == "INSERT-ITEM"){
                                                selector.insert(props.ref, JSON.parse(props.arg0));
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
        """Contains the name / id of item where mouse was clicked (i.e., the item which received
        the mouse click event)"""
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

    def __init__(self, name, text=None, icon=None, is_leaf=None, expanded=None,
                 img=None, group=None, count=None, nodes=None):
        """Below are the parameters of the SidebarNode class

            Args:
                name (string, required): A unique identifier for instance of this class
                text (string): Text to be displayed as label on the Sidebar
                icon (string): An CSS class icon to be displayed along label
                is_leaf (boolean): Tells whether the current node have child nodes or not
                expanded (boolean): Renders the sidebar with have current node and its child
                                    displayed as expanded
                img (string): Image to be displayed if icon attribute is None
                group (string): Group nodes under one category
                count (int): An integer value to be displayed next to the label of node
                nodes (SidebarNode): The child nodes of the current node
        """
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
        else:
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

    def render(self):
        """Renders an node or leaf depending upon the value of `is_leaf' attribute
        """
        obj = {}
        if self._is_leaf:
            obj['id'] = self._name
            if self._text is not None:
                obj['text'] = self._text
            if self._icon is not None:
                obj['icon'] = self._icon
            if self._count is not None:
                obj['count'] = self._count
            return obj
        else:
            obj['id'] = self._name
            if self._text is not None:
                obj['text'] = self._text
            if self._icon is not None:
                obj['img'] = self._img
            if self._count is not None:
                obj['count'] = self._count
            if self._group is not None:
                obj['group'] = self._group
            if self._expanded is not None:
                obj['expanded'] = self._expanded
            if self._child_widgets is not None:
                obj['nodes'] = []
                for child in self._child_widgets:
                    obj['nodes'].append(child.render())
            return obj


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
    _queue = None

    def __init__(self, name, nodes=None, onclick_callback=None, onclick_client_script=None, app=None,
                 topHTML=None, bottomHTML=None, flatButton=None):
        """
            Args:
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
        self._queue = []

    @property
    def onclick_client_script(self):
        """The Javascript that will be executed at client side on mouse click event
        """
        return self._onclick_client_script

    @onclick_client_script.setter
    def onclick_client_script(self, val):
        self._onclick_client_script = val

    @property
    def topHTML(self):
        """HTML to be displayed on top of the sidebar"""
        return self._topHTML

    @topHTML.setter
    def topHTML(self, val):
        self._topHTML = val

    @property
    def bottomHTML(self):
        """HTML to be displayed on bottom of the sidebar"""
        return self._bottomHTML

    @bottomHTML.setter
    def bottomHTML(self, val):
        self._bottomHTML = val

    @property
    def clicked_item(self):
        """The sidebar item which was clicked"""
        return self._clicked_item

    @clicked_item.setter
    def clicked_item(self, val):
        self._clicked_item = val

    def add_items(self, items):
        """Adds items to sidebar which are passed as list of items to
        this method

            Args:
                items (list): List of SidebarNode items
        """
        content = []
        for item in items:
            content.append(item.render())
        self._queue.append({'cmd': 'ADD-ITEMS', 'arg0': content})

    def insert_items(self, items, ref_item):
        """Insert specified items after the item passed for reference

            Args:
                items (list): List of sidebar nodes
                ref_item (string): Name of the referenced item
        """
        content = []
        for item in items:
            content.append(item.render())
        self._queue.append({'cmd': 'INSERT-ITEMS', 'arg0': content, 'ref': ref_item})

    def remove_items(self, items):
        """Removes all items from the toolbar passed as arg to this method

            Args:
                items (list): A list of item names to be removed from toolbar
        """
        self._queue.append({'cmd': 'REMOVE-ITEMS', 'arg0': json.dumps(items)})

    def show_items(self, items):
        """Shows the hidden items passed as list of item names

            Args:
                items (list): List of names of items
        """
        self._queue.append({'cmd': 'SHOW-ITEMS', 'arg0': json.dumps(items)})

    def hide_items(self, items):
        """Hides the specified items passed as list of item names parameter

            Args:
                items (list): List of item names
        """
        self._queue.append({'cmd': 'HIDE-ITEMS', 'arg0': json.dumps(items)})

    def enable_item(self, item):
        """Enables an already disabled item in the sidebar

            Args:
                item (string): Name or Id of the item that needs to be enabled
        """
        self._queue.append({'cmd': 'ENABLE-ITEM', 'arg0': item})

    def disable_item(self, item):
        """Disables an already enabled item in the sidebar

            Args:
                item (string): Name or Id of the item that needs to be enabled
        """
        self._queue.append({'cmd': 'DISABLE-ITEM', 'arg0': item})

    def expand_item(self, item):
        """Expands an collapsed item node

            Args:
                item (string): Name or Id of the node that needs to be expanded
        """
        self._queue.append({'cmd': 'EXPAND-ITEM', 'arg0': item})

    def collapse_item(self, item):
        """Collapse an expanded node in the sidebar

            Args:
                item (string): Collapse the provided node
        """
        self._queue.append({'cmd': 'COLLAPSE-ITEM', 'arg0': item})

    def select_item(self, item):
        """Selects the specified item in the sidebar

            Args:
                item (string): Name or Id of the node that needs to be selected
        """
        self._queue.append({'cmd': 'SELECT-ITEM', 'arg0': item})

    def unselect_item(self, item):
        """UnSelects the specidied item in the sidebar

            Args:
                item (string): Name or Id of the node that needs to be unselected
        """
        self._queue.append({'cmd': 'UNSELECT-ITEM', 'arg0': item})

    def click_item(self, item):
        """Emulates an click on the specified node

            Args:
                item (string): Name or Id of the node
        """
        self._queue.append({'cmd': 'CLICK-ITEM', 'arg0': item})

    def on_sidebar_item_clicked(self, click_callback):
        """Registers an method or callback to be called whenever an mouse click event
        is triggered on the widget

            Args:
                click_callback (callable): Function or method that needs to be called
        """
        self._onclick_callback = click_callback

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
                            $2.ajax({
                                url: "/%s",
                                dataType: "json",
                                success: function(props){
                                    selector = w2ui['%s'];
                                    if(selector != undefined){
                                        if(props.cmd != undefined){
                                            if(props.cmd == "HIDE-ITEMS"){
                                                selector.hide(JSON.parse(props.arg0));
                                            }
                                            if(props.cmd == "SHOW-ITEMS"){
                                                selector.show(JSON.parse(props.arg0));
                                            }
                                            if(props.cmd == "ENABLE-ITEM"){
                                                selector.enable(props.arg0);
                                            }
                                            if(props.cmd == "DISABLE-ITEM"){
                                                selector.disable(props.arg0);
                                            }
                                            if(props.cmd == "ADD-ITEMS"){
                                                selector.add(props.arg0);
                                            }
                                            if(props.cmd == "INSERT-ITEMS"){
                                                selector.insert(props.ref, props.arg0);
                                            }
                                            if(props.cmd == "REMOVE-ITEMS"){
                                                selector.remove(JSON.parse(props.arg0));
                                            }
                                            if(props.cmd == "COLLAPSE-ITEM"){
                                                selector.collapse(props.arg0);
                                            }
                                            if(props.cmd == "EXPAND-ITEM"){
                                                selector.expand(props.arg0);
                                            }
                                            if(props.cmd == "SELECT-ITEM"){
                                                selector.select(props.arg0);
                                            }
                                            if(props.cmd == "UNSELECT-ITEM"){
                                                selector.unselect(props.arg0);
                                            }
                                            if(props.cmd == "CLICK-ITEM"){
                                                selector.click(props.arg0);
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
            child_widgets += json.dumps(child.render()) + ",\n"
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
                                    $2('#%s').css('width', (event.goFlat ? '35px' : '200px'));
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
        content += "\n" + self._attach_polling()
        return content


class FormFieldText(Widget):
    """A most basic form of field in an form. It allows user to enter any kind of text as input"""

    _type = None
    _required = None
    _options = None
    _items = None
    _caption = None
    _attributes = None

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        """
            Args:
                name (string, required): A unique  identifier for the object
                required (boolean): Whether this field is required or not
                options (boolean): Whether the current field have any options
                                    associated. If True, the options must be
                                    given through items parameter
                items (dict): The various options for this field in dict format
                caption (string): A title to be shown along the field. If empty,
                                    field's name will used to show the lable
                attributes (dict): Any other attributes as comma sep list
        """
        Widget.__init__(self, name)
        self._type = 'text'
        if required is not None:
            self._required = required
        else:
            self._required = False
        if options is not None:
            self._options = options
        else:
            self._options = False
        self._items = items
        if caption is not None:
            self._caption = caption
        else:
            self._caption = name
        self._attributes = attributes

    def render(self):
        content = "{ "
        content += "field: '" + self._name + "', "
        content += "type: '" + self._type + "', "
        content += "required: " + json.dumps(self._required) + ", "
        if self._options is not None and self._options:
            content += "options: {items: ["
            if self._items is not None:
                for item in self._items:
                    content += "'" + item + "', "
            content += "]}, "
        if self._caption is not None:
            content += "html: { caption: '" + self._caption + "', "
            if self._attributes is not None:
                content += "attr: '" + self._attributes + "' "
            content += "}"
        content += "}"
        return content


class FormFieldAlpha(FormFieldText):
    """Field which can hold only alpha and numeric values """

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'alphaNumeric'


class FormFieldInt(FormFieldText):
    """This field allows to hold integer values as a whole number only"""

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'int'


class FormFieldFloat(FormFieldText):
    """Field which allows to store floating point numbers or values """

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'float'


class FormFieldDate(FormFieldText):
    """Field which can hold date values and provides an calendar widget for selection"""

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'date'


class FormFieldList(FormFieldText):
    """Field which can hold list of values and display them as dropdown widget """

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'list'


class FormFieldEnum(FormFieldText):
    """Field which to select multiple options and display it as tokens in the textfield widget"""

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'enum'


class FormFieldSelect(FormFieldText):
    """Field which can hold list of values and provides either dropdown or listbox
    to select an element. Based on the browser, it renders the widget as ListBox or Dropdown
    """

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'select'


class FormFieldCheckbox(FormFieldText):
    """Field which can hold only one of two values: true or false """

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'checkbox'


class FormFieldRadio(FormFieldText):
    """Field which allows to select single option among the may provided"""

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'radio'


class FormFieldTextArea(FormFieldText):
    """Field which can hold multiple line text in it"""

    def __init__(self, name, required=None, options=None, items=None,
                 caption=None, attributes=None):
        FormFieldText.__init__(self, name, required, options, items,
                               caption, attributes)
        self._type = 'textarea'


class Form(Widget):
    """A form can have multiple fields embedded and provides option to
    either POST data from fields to server for further processing OR
    sends the data from fields to GET more information
    """

    _url = None
    _header = None
    _submit_callback = None
    _reset_callback = None
    _app = None
    _form_data = None

    def __init__(self, name, url=None, header=None, fields=None,
                 submit_callback=None, reset_callback=None, app=None):
        """
            Args:
                name (string, required): Name or unique id of the object
                url (string): Url to which data should be posted. If not
                            provided, the data will be submitted internally
                            to the submit callback handler
                header (string): An title to be shown on top of the form
                fields (FormFieldxxx): Objects of FormFfieldxxx type to read
                                        input from users
                submit_callback (callable): Gets called when form is submitted
                                            and Url parameter is None
                reset_callback (callable): Called when user clicks on the form's
                                            reset button
        """
        Widget.__init__(self, name)
        self._app = app
        if url is not None:
            self._url = url
        if header is not None:
            self._header = header
        else:
            self._header = 'FORM'
        if fields is not None:
            self._child_widgets = fields
        else:
            self._child_widgets = []
        self._submit_callback = submit_callback
        self._reset_callback = reset_callback

    @property
    def URL(self):
        """URL that will be called when form data is posted. If no external URL is provided,
        this attribute will point to `submit_callback` and will provide the form data as
        parameter of the callback
        """
        return self._url

    @URL.setter
    def URL(self, val):
        self._url = val

    @property
    def header(self):
        """The text to be shown as title / header of the form"""
        return self._header

    @header.setter
    def header(self, val):
        self._header = val

    @property
    def form_data(self):
        """User submitted form data, it will be available only after user submits the form
        """
        return self._form_data

    @form_data.setter
    def form_data(self, val):
        self._form_data = val

    def on_form_submit(self, submit_callback):
        """Attaches the provided function/method to form's submit event

            Args:
                submit_callback (callable): Function or method that needs to be called when
                                            event triggers. The callable should have a parameter
                                            which will be used to pass the form data to the
                                            callable
            Example:
                def handle_form_submit(form):
                    pass
        """
        self._submit_callback = submit_callback

    def on_form_reset(self, reset_callback):
        """Attaches the provided function/method to form's reset event

            Args:
                reset_callback (callable): Function or Method that will be called when
                                            event triggers
        """
        self._reset_callback = reset_callback

    def _process_submit_callback(self):
        self._form_data = request.form
        if self._submit_callback is not None:
            return json.dumps({'result': self._submit_callback(request.form)})
        return json.dumps({'result': ''})

    def _process_reset_callback(self):
        if self._reset_callback is not None:
            return json.dumps({'result': self._reset_callback()})
        return json.dumps({'result': ''})

    def _attach_script(self):
        reset_url = ""
        if self._app is not None and self._url is None:
            # Prepare the form submit URL if no external URL is provided
            self._url = str(__name__ + "_" + self._name).replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == self._url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + self._url, self._url, self._process_submit_callback,
                                       methods=['POST'])
            # Prepare the form reset URL to call the reset callback
            reset_url = str(__name__ + "_" + self._name + "reset").replace('.', '_')
            found = False
            for rule in self._app.url_map.iter_rules():
                if rule.endpoint == reset_url:
                    found = True
            if not found:
                self._app.add_url_rule('/' + reset_url, reset_url, self._process_reset_callback)
        # Prepare the fields to be added to form
        fields = "[\n"
        for field in self._child_widgets:
            fields += field.render() + ",\n"
        fields += "\n]"
        script = """
                <script>
                    $2(function(){
                        $2('#%s').w2form({
                            name: '%s',
                            url: '%s',
                            header: '%s',
                            fields: %s,
                            actions: {
                                reset: function(){
                                    this.clear();
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        success: function(status){},
                                        error: function(err_status){
                                            alertify.error("Status Code: "
                                            + err_status.status + "<br />" + "Error Message:"
                                            + err_status.statusText);
                                        }
                                    });
                                },
                                save: function(){
                                    this.save();
                                }
                            }
                        });
                    });
                </script>
                """ % (self._name, self._name, self._url, self._header,
                       fields, reset_url)
        return script

    def render(self):
        """Renders the content of Form widget with its fields to the parent widget"""
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += self._attach_script()
        return content


class Popup(Widget):
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
    _url = None
    _color = None
    _opacity = None
    _speed = None
    _transition = None
    _show_close = None
    _show_max = None
    _keyboard = None

    _on_open_callback = None
    _open_callback_url = None
    _on_close_callback = None
    _close_callback_url = None
    _on_max_callback = None
    _max_callback_url = None
    _on_min_callback = None
    _min_callback_url = None
    _on_toggle_callback = None
    _toggle_callback_url = None
    _on_keydown_callback = None
    _keydown_callback_url = None
    _queue = None
    _app = None

    def __init__(self, name, title=None, body=None, buttons=None, style=None, modal=None, width=None,
                 height=None, url=None, color=None, opacity=None, speed=None, transition=None,
                 show_close=None, show_max=None, keyboard=None, on_open_callback=None,
                 on_close_callback=None, on_max_callback=None, on_min_callback=None,
                 on_toggle_callback=None, on_keydown_callback=None, app=None):
        """
            Args:
                name (string, required): A unique identifier for the current object
                title (string): Title of the popup box
                body (string): The text to be displayed in the body of Popup. It can
                                be an HTML script also to display formatted text
                buttons (string): An HTML string consisting of HTML input tag of type
                                Button. In line, javascript can also be provided in the
                                string
                style (string): An string which contains CSS style attributes for Popup
                modal (boolean): Whether the popup should be opened as modal or not
                width (int): Width of the popup box
                height (int): Height of the popup box
                url (string): An url to load the content of popup from
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
                app (Flask): An instance of flask app
        """
        Widget.__init__(self, name)
        self._title = title
        self._body = body
        self._buttons = buttons
        self._modal = modal
        self._width = width
        self._height = height
        self._url = url
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
        self._queue = []
        self._app = app

    def _process_on_open_callback(self):
        if self._on_open_callback is not None:
            return json.dumps({'result': self._on_open_callback()})
        return json.dumps({'result': ''})

    def _process_on_close_callback(self):
        if self._on_close_callback is not None:
            return json.dumps({'result': self._on_close_callback()})
        return json.dumps({'result': ''})

    def _process_on_max_callback(self):
        if self._on_max_callback is not None:
            return json.dumps({'result': self._on_max_callback()})
        return json.dumps({'result': ''})

    def _process_on_min_callback(self):
        if self._on_min_callback is not None:
            return json.dumps({'result': self._on_min_callback()})
        return json.dumps({'result': ''})

    def _process_on_toggle_callback(self):
        if self._on_toggle_callback is not None:
            return json.dumps({'result': self._on_toggle_callback()})
        return json.dumps({'result': ''})

    def _process_on_keydown_callback(self):
        if self._on_keydown_callback is not None:
            return json.dumps({'result': self._on_keydown_callback()})
        return json.dumps({'result': ''})

    def _register_url(self, url, func):
        if self._app is None:
            raise ValueError("The value of the 'app' attribute can't be empty")
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == url:
                found = True
        if not found:
            self._app.add_url_rule('/' + url, url, func)

    def _process_urls(self):
        # open callback url
        self._open_callback_url = str(__name__ + "_" + self._name + "_open").replace('.', '_')
        self._register_url(self._open_callback_url, self._process_on_open_callback)
        # close callback url
        self._close_callback_url = str(__name__ + "_" + self._name + "_close").replace('.', '_')
        self._register_url(self._close_callback_url, self._process_on_close_callback)
        # max callback url
        self._max_callback_url = str(__name__ + "_" + self._name + "_max").replace('.', '_')
        self._register_url(self._max_callback_url, self._process_on_max_callback)
        # min callback url
        self._min_callback_url = str(__name__ + "_" + self._name + "_min").replace('.', '_')
        self._register_url(self._min_callback_url, self._process_on_min_callback)
        # toggle callback url
        self._toggle_callback_url = str(__name__ + "_" + self._name + "_toggle").replace('.', '_')
        self._register_url(self._toggle_callback_url, self._process_on_toggle_callback)
        # keydown callback url
        self._keydown_callback_url = str(__name__ + "_" + self._name + "_keydown").replace('.', '_')
        self._register_url(self._keydown_callback_url, self._process_on_keydown_callback)

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
        self._queue.append({'cmd': 'OPEN'})

    def load(self, url):
        """Opens the popup and displays the content loaded from url"""
        self._queue.append({'cmd': 'LOAD', 'arg0': url})

    def close(self):
        """Closes the already opened popup"""
        self._queue.append({'cmd': 'CLOSE'})

    def lock(self, message, showSpinner=False):
        """Locks the dialogbox using an overlay and shows the spinner if set to True
        """
        self._queue.append({'cmd': 'LOCK', 'arg0': message, 'arg1': json.dumps(showSpinner)})

    def lock_screen(self, options=None):
        """Locks the whole screen using the overlay"""
        self._queue.append({'cmd': 'LOCK-SCREEN', 'arg0': options})

    def max(self):
        """Maximize the popup window"""
        self._queue.append({'cmd': 'MAX'})

    def min(self):
        """Minimizes the popup window"""
        self._queue.append({'cmd': 'MIN'})

    def message(self, options=None):
        """Shows an message in the popup box

            Example:
                message({'height':200, 'width': 200, 'html': '<span>Some message</span>}')
        """
        self._queue.append({'cmd': 'MSG', 'arg0': json.dumps(options)})

    def resize(self, height, width, callback=None):
        """Resize the popup to desired size and calls the callback"""
        if callback is not None:
            self._queue.append({'cmd': 'RESIZE', 'arg0': width, 'arg1': height, 'arg2': json.dumps(callback)})
        else:
            self._queue.append({'cmd': 'RESIZE', 'arg0': width, 'arg1': height})

    def unlock(self):
        """Unlocks the locked popup"""
        self._queue.append({'cmd': 'UNLOCK'})

    def unlock_screen(self):
        """Unlocks the whole screen"""
        self._queue.append({'cmd': 'UNLOCK-SCREEN'})

    def _sync_properties(self):
        if self._queue.__len__() > 0:
            cmd = self._queue.pop()
            return json.dumps(cmd)
        return json.dumps({'result': ''})

    def _attach_polling(self):
        if self._app is None:
            raise ValueError("The value of 'app' attribute can't be empty")
        url = str(__name__ + "_" + self._name + "_props").replace('.', '_')
        script = """<script>
                    (function %s_poll(){
                        setTimeout(function(){
                            $2.ajax({
                                url: "/%s",
                                dataType: "json",
                                success: function(props){
                                        if(props.cmd != undefined){
                                            if(props.cmd == "OPEN"){
                                                %s_popup();
                                            }
                                            if(props.cmd == "CLOSE"){
                                                w2popup.close();
                                            }
                                            if(props.cmd == "LOAD"){
                                                w2popup.load({url: props.arg0});
                                            }
                                            if(props.cmd == "LOCK"){
                                                w2popup.lock(props.arg0, props.arg1);
                                            }
                                            if(props.cmd == "LOCK-SCREEN"){
                                                w2popup.lockScreen(props.arg0);
                                            }
                                            if(props.cmd == "MAX"){
                                                w2popup.max();
                                            }
                                            if(props.cmd == "MIN"){
                                                w2popup.min();
                                            }
                                            if(props.cmd == "MSG"){
                                                w2popup.message(JSON.parse(props.arg0));
                                            }
                                            if(props.cmd == "RESIZE"){
                                                if(props.arg2 == null){
                                                    w2popup.resize(props.arg0, props.arg1);
                                                    }
                                                else{
                                                    w2popup.resize(props.arg0, props.arg1, props.arg2);
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
        self._process_urls()
        script = """
                    <script>
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
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        error: function(err_status){
                                            alertify.error("Status Code: "
                                            + err_status.status + "<br />" + "Error Message:"
                                            + err_status.statusText);
                                        }
                                    });
                                },
                                onClose: function(event){
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        error: function(err_status){
                                            alertify.error("Status Code: "
                                            + err_status.status + "<br />" + "Error Message:"
                                            + err_status.statusText);
                                        }
                                    });
                                },
                                onMax: function(event){
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        error: function(err_status){
                                            alertify.error("Status Code: "
                                            + err_status.status + "<br />" + "Error Message:"
                                            + err_status.statusText);
                                        }
                                    });
                                },
                                onMin: function(event){
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        error: function(err_status){
                                            alertify.error("Status Code: "
                                            + err_status.status + "<br />" + "Error Message:"
                                            + err_status.statusText);
                                        }
                                    });
                                },
                                onKeydown: function(event){
                                    $2.ajax({
                                        url: '/%s',
                                        type: 'get',
                                        dataType: 'json',
                                        error: function(err_status){
                                            alertify.error("Status Code: "
                                            + err_status.status + "<br />" + "Error Message:"
                                            + err_status.statusText);
                                        }
                                    });
                                }
                            });
                        }
                    </script>
                """ % (self._name,
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
                       self._open_callback_url,
                       self._close_callback_url,
                       self._max_callback_url,
                       self._min_callback_url,
                       self._keydown_callback_url
                       )
        return script

    def render(self):
        """Renders the popup as HTML"""
        content = ""
        content += self._attach_script()
        content += "\n" + self._attach_polling()
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
