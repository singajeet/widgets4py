"""Python module to provide graphical or web bases widgets
using W2UI framework. This module wraps the required JavaScript
to make python objects and allows client-server to interact
using same instance of the widget i.e., a single widget instance
will render the widget at client side and same instance can be
used to execute server side code.

    Author: Ajeet Singh
    Date: 7/10/2019
"""
from flask_socketio import Namespace, emit
from widgets4py.base import Widget  # noqa
from flask import json, request  # noqa
from enum import Enum


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


class Grid(Widget, Namespace):
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
    _toolbar_delete_client_script = None
    _toolbar_delete_callback = None
    _footer = None
    _sort_on = None
    _sort_dir = None
    _data_load_callback = None
    _onclick_callback = None
    _disabled = None
    _select_column = None
    _multi_select = None
    _line_numbers = None
    _multi_search = None
    _namespace = None
    _socket_io = None

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, val):
        self._header = val

    @property
    def column_collection(self):
        return self._column_collection

    @column_collection.setter
    def column_collection(self, val):
        self._column_collection = val

    def __init__(self, name, header, column_collection, socket_io, row_collection=None, desc=None,  # noqa
                 prop=None, style=None, attr=None, disabled=False, onclick_callback=None,
                 css_cls=None, data_url=None, data_load_callback=None,
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
                socket_io (SocketIO): An instance of SocketIO class
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
        Namespace.__init__(self, '/' + str(__name__ + "_" + str(name) + "_grid_tb").replace('.', '_'))
        self._namespace = '/' + str(__name__ + "_" + str(name) + "_grid_tb").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._header = header
        self._column_collection = column_collection
        self._row_collection = row_collection
        self._search_collection = search_collection
        self.add_style("width", "100%")
        self.add_style("height", "100%")
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
        script = ""
        if self._data_url is None and self._data_load_callback is None:
            script = """
                    <script>
                        $2(function(){
                            var selector = $2('#%s');
                            var socket = io('%s');
                            selector.w2grid({
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
                                    //websocket call to click event
                                    var props = {};
                                    socket.emit('fire_click_event', props);
                                },
                                onAdd: function (event) {
                                    %s
                                    //websocket call to add event
                                    var props = {};
                                    socket.emit('fire_add_event', props);
                                },
                                onEdit: function (event) {
                                    %s
                                    //websocket call to edit event
                                    var props = {};
                                    socket.emit('fire_edit_event', props);
                                },
                                onDelete: function (event) {
                                    %s
                                    //webaocket call to delete event
                                    var props = {};
                                    socket.emit('fire_delete_event', props);
                                },
                                onSave: function (event) {
                                    %s
                                    //websocket call to save event
                                    var props = {};
                                    socket.emit('fire_save_event', props);
                                },
                                sortData: [{field: '%s', direction: '%s'}],
                                multiSearch: %s
                                %s  //searches placeholder
                            });
                            socket.on('sync_properties_%s', function(props){
                                    var name = '%s';
                                    var cmd = props["cmd"];
                                    var value = props["value"];
                                    if(selector != undefined){
                                        if(cmd != undefined){
                                            if(cmd === "HIDE"){
                                                w2ui[name].toggleColumn(value);
                                            }
                                            if(cmd == "ADD-RECORD"){
                                                w2ui[name].add(value);
                                            }
                                            if(cmd == "SELECT-ALL"){
                                                w2ui[name].selectAll();
                                            }
                                            if(cmd == "UNSELECT-ALL"){
                                                w2ui[name].selectNone();
                                            }
                                            if(cmd == "SELECT"){
                                                w2ui[name].select(JSON.parse(value));
                                            }
                                            if(cmd == "UNSELECT"){
                                                w2ui[name].unselect(JSON.parse(value));
                                            }
                                        } else {
                                            alertify.warning("No command to process");
                                        }
                                    }
                            });
                        });
                    </script>
                """ % (self._name, self._namespace, self._name, self._header, self._column_collection.render(),
                       self._row_collection.render() if self._row_collection is not None else "",
                       json.dumps(self._tool_bar), json.dumps(self._footer),
                       json.dumps(self._select_column), json.dumps(self._line_numbers),
                       json.dumps(self._toolbarAdd), json.dumps(self._toolbarDelete),
                       json.dumps(self._toolbarSave), json.dumps(self._toolbarEdit),
                       json.dumps(self._multi_select),
                       self._toolbar_add_client_script,
                       self._toolbar_edit_client_script,
                       self._toolbar_delete_client_script,
                       self._toolbar_save_client_script,
                       self._sort_on, self._sort_dir,
                       json.dumps(self._multi_search),
                       (", searches: " + self._search_collection if self._search_collection is not None else ""),
                       self._name, self._name)
        elif self._data_url is not None and self._data_load_callback is None:
            script = """
                    <script>
                        $2(function(){
                            var selector = $2('#%s');
                            var socket = io('%s');
                            selector.w2grid({
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
                                    //websocket call to click event
                                    var props = {};
                                    socket.emit('fire_click_event', props);
                                },
                                onAdd: function (event) {
                                    %s
                                    //websocket call to add event
                                    var props = {};
                                    socket.emit('fire_add_event', props);
                                },
                                onEdit: function (event) {
                                    %s
                                    //websocket call to edit event
                                    var props = {};
                                    socket.emit('fire_edit_event', props);
                                },
                                onDelete: function (event) {
                                    %s
                                    //webaocket call to delete event
                                    var props = {};
                                    socket.emit('fire_delete_event', props);
                                },
                                onSave: function (event) {
                                    %s
                                    //websocket call to save event
                                    var props = {};
                                    socket.emit('fire_save_event', props);
                                },
                                sortData: [{field: '%s', direction: '%s'}],
                                multiSearch: %s
                                %s  //searches placeholder
                            });
                            socket.on('sync_properties_%s', function(props){
                                    var name = '%s';
                                    var cmd = props["cmd"];
                                    var value = props["value"];
                                    if(selector != undefined){
                                        if(cmd != undefined){
                                            if(cmd === "HIDE"){
                                                w2ui[name].toggleColumn(value);
                                            }
                                            if(cmd == "ADD-RECORD"){
                                                w2ui[name].add(value);
                                            }
                                            if(cmd == "SELECT-ALL"){
                                                w2ui[name].selectAll();
                                            }
                                            if(cmd == "UNSELECT-ALL"){
                                                w2ui[name].selectNone();
                                            }
                                            if(cmd == "SELECT"){
                                                w2ui[name].select(JSON.parse(value));
                                            }
                                            if(cmd == "UNSELECT"){
                                                w2ui[name].unselect(JSON.parse(value));
                                            }
                                        } else {
                                            alertify.warning("No command to process");
                                        }
                                    }

                            });
                        });
                    </script>
                    """ % (self._name, self._namespace, self._name, self._header, self._column_collection.render(),
                           self._data_url, json.dumps(self._tool_bar), json.dumps(self._footer),
                           json.dumps(self._select_column), json.dumps(self._line_numbers),
                           json.dumps(self._toolbarAdd), json.dumps(self._toolbarDelete),
                           json.dumps(self._toolbarSave), json.dumps(self._toolbarEdit),
                           json.dumps(self._multi_select),
                           self._toolbar_add_client_script,
                           self._toolbar_edit_client_script,
                           self._toolbar_delete_client_script,
                           self._toolbar_save_client_script,
                           self._sort_on, self._sort_dir,
                           json.dumps(self._multi_search),
                           (", searches: " + self._search_collection if self._search_collection is not None else ""),
                           self._name, self._name)
        elif self._data_url is None and self._data_load_callback is not None:
            script = """
                    <script>
                        $2(function(){
                         var selector = $2('#%s');
                         var socket = io('%s');
                         socket.emit('get_grid_records', {});
                         socket.on('set_grid_records', function(data){
                            selector.w2grid({
                                name: '%s',
                                header: '%s',
                                columns: %s,
                                records: data
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
                                    //websocket call to click event
                                    var props = {};
                                    socket.emit('fire_click_event', props);
                                },
                                onAdd: function (event) {
                                    %s
                                    //websocket call to add event
                                    var props = {};
                                    socket.emit('fire_add_event', props);
                                },
                                onEdit: function (event) {
                                    %s
                                    //websocket call to edit event
                                    var props = {};
                                    socket.emit('fire_edit_event', props);
                                },
                                onDelete: function (event) {
                                    %s
                                    //webaocket call to delete event
                                    var props = {};
                                    socket.emit('fire_delete_event', props);
                                },
                                onSave: function (event) {
                                    %s
                                    //websocket call to save event
                                    var props = {};
                                    socket.emit('fire_save_event', props);
                                },
                                sortData: [{field: '%s', direction: '%s'}],
                                multiSearch: %s
                                %s  //searches placeholder
                            });
                         });
                            socket.on('sync_properties_%s', function(props){
                                    var name = '%s';
                                    var cmd = props["cmd"];
                                    var value = props["value"];
                                    if(selector != undefined){
                                        if(cmd != undefined){
                                            if(cmd === "HIDE"){
                                                w2ui[name].toggleColumn(value);
                                            }
                                            if(cmd == "ADD-RECORD"){
                                                w2ui[name].add(value);
                                            }
                                            if(cmd == "SELECT-ALL"){
                                                w2ui[name].selectAll();
                                            }
                                            if(cmd == "UNSELECT-ALL"){
                                                w2ui[name].selectNone();
                                            }
                                            if(cmd == "SELECT"){
                                                w2ui[name].select(JSON.parse(value));
                                            }
                                            if(cmd == "UNSELECT"){
                                                w2ui[name].unselect(JSON.parse(value));
                                            }
                                        } else {
                                            alertify.warning("No command to process");
                                        }
                                    }

                            });
                        });
                    </script>
                    """ % (self._name, self._namespace, self._name, self._header, self._column_collection.render(),
                           json.dumps(self._tool_bar), json.dumps(self._footer),
                           json.dumps(self._select_column), json.dumps(self._line_numbers),
                           json.dumps(self._toolbarAdd), json.dumps(self._toolbarDelete),
                           json.dumps(self._toolbarSave), json.dumps(self._toolbarEdit),
                           json.dumps(self._multi_select),
                           self._toolbar_add_client_script,
                           self._toolbar_edit_client_script,
                           self._toolbar_delete_client_script,
                           self._toolbar_save_client_script,
                           self._sort_on, self._sort_dir,
                           json.dumps(self._multi_search),
                           (", searches: " + self._search_collection if self._search_collection is not None else ""),
                           self._name, self._name)
        return script

    def on_fire_click_event(self, props):
        if self._onclick_callback is not None:
            self._onclick_callback(self._name, props)

    def on_get_grid_records(self):
        record_collection = self._data_load_callback()
        self._row_collection = record_collection
        result = {}
        result['total'] = record_collection.__len__()
        result['records'] = record_collection.render()
        emit('set_grid_records', result,
             namespace=self._namespace)

    def on_fire_add_event(self, props):
        if self._toolbar_add_callback is not None:
            self._toolbar_add_callback(self._name, props)

    def on_fire_edit_event(self, props):
        if self._toolbar_edit_callback is not None:
            self._toolbar_edit_callback(self._name, props)

    def on_fire_delete_event(self, props):
        if self._toolbar_delete_callback is not None:
            self._toolbar_delete_callback(self._name, props)

    def on_fire_save_event(self, props):
        if self._toolbar_save_callback is not None:
            self._toolbar_save_callback(self._name, props)

    def toggle_column(self, col_name):
        """Toggles the visibility of an column in the grid

            Args:
                col_name: Name of the column that needs to be toggled
        """
        self._sync_properties('HIDE', col_name)

    def add_record(self, record):
        """Adds an record to the grid

            Args:
                record (GridRecord): An record of GridRecord type
        """
        rec_count = self._row_collection.count
        self._row_collection.add(record)
        record.add_cell('recid', rec_count + 1)
        self._sync_properties('ADD-RECORD', record.render())

    def select_all_records(self):
        """Selects all the records available in the Grid Widget"""
        self._sync_properties('SELECT-ALL', '')

    def unselect_all_records(self):
        """Selects all the records available in the Grid Widget"""
        self._sync_properties('UNSELECT-ALL', '')

    def select_records(self, records):
        """Selects all the records available in the Grid Widget

            Args:
                records (string): A comma seperated string containing records to select
                                    e.g., "2,3,5" or "5"
        """
        self._sync_properties('SELECT', records)

    def unselect_records(self, records):
        """Selects all the records available in the Grid Widget

            Args:
                records (string): A comma seperated string containing records to select
                                    e.g., "2,3,5" or "5"
        """
        self._sync_properties('UNSELECT', records)

    def _sync_properties(self, cmd, value):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value},
             namespace=self._namespace)

    def render(self):
        content = self._render_pre_content('div')
        content += self._render_post_content('div') + "\n"
        content += self._attach_script()
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


class Toolbar(Widget, Namespace):
    """A toolbar having collection of buttons, chexkbox,
    radio buttons, separaters, etc. An toolbar item can
    have title or button or both
    """

    _onclick_callback = None
    _onclick_client_script = None
    _clicked_item = None
    _namespace = None
    _socket_io = None

    def __init__(self, name, socket_io, items=None, desc=None,
                 prop=None, style=None, attr=None, css_cls=None,
                 onclick_callback=None, onclick_client_script=None):
        """
            Args:
                name (string): Name or Id for internal use
                socket_io (SocketIO): An instance of the SocketIO class
                items (Widget): Child items like, ToolbarButton, ToolbarRadio, etc
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                css_cls (list, optional): An list of CSS class names to be added to current widget
                onclick_callback (callable): will be called when mouse is clicked on any child item
                onclick_client_script (string): JS to be called when mouse is clicked on any item
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style,
                        attr=attr, css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + str(name) + "_toolbar").replace('.', '_'))
        self._namespace = '/' + str(__name__ + str(name) + "_toolbar").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        if items is not None:
            self._child_widgets = items
        else:
            self._child_widgets = []
        self._onclick_callback = onclick_callback
        if onclick_client_script is not None:
            self._onclick_client_script = onclick_client_script
        else:
            self._onclick_client_script = ""

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

    @property
    def items(self):
        return self._child_widgets

    @items.setter
    def items(self, val):
        self._child_widgets = val

    @property
    def clicked_item(self):
        """Contains the name / id of item where mouse was clicked (i.e., the item which received
        the mouse click event)"""
        return self._clicked_item

    def add_item(self, item):
        """Adds a new item to the toolbar passed as argument

            Args:
                item (ToolbarButton): An instance of ToolbarButton or its subclasses
        """
        self._sync_properties('ADD-ITEM', item.render())

    def insert_item(self, item, ref_item):
        """Inserts a new item to the toolbar after the specified referenced item

            Args:
                item (ToolbarButton): Instance of ToolbarButton or its subclasses
                ref_item (string): Id or name of the item after which new item should be
                                    inserted
        """
        self._sync_properties('INSERT-ITEM', item.render(), ref_item)

    def remove_item(self, index_of_item):
        """Removes an item from the toolbar available at the specified index location

            Args:
                index_of_item (int): Index of item that needs to be removed from toolbar
        """
        self._sync_properties('REMOVE-ITEM', index_of_item)

    def show_item(self, item_name):
        """Shows an item which was in hidden state previously

            Args:
                item_name (string): Name or Id of the toolbar item that needs to be set visible
        """
        self._sync_properties('SHOW-ITEM', item_name)

    def hide_item(self, item_name):
        """Hides an visible item available on the toolbar

            Args:
                item_name (string): Name or Id of the toolbar item that needs to be set as hidden
        """
        self._sync_properties('HIDE-ITEM', item_name)

    def enable_item(self, item_name):
        """Enables an visible toollbar item if its has been set as disiabled

            Args:
                item_name (string): Name or Id of item that needs to be enabled
        """
        self._sync_properties('ENABLE-ITEM', item_name)

    def disable_item(self, item_name):
        """Disable an visible toolbar item which is already in enabled state

            Args:
                item_name (string): Name or Id of the item that needs to be disabled
        """
        self._sync_properties('DISABLE-ITEM', item_name)

    def _sync_properties(self, cmd, value, ref_item=None):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value, 'ref_item': ref_item},
             namespace=self._namespace)

    def _attach_script(self):
        child_widgets = "[\n"
        for child in self._child_widgets:
            child_widgets += child.render() + ",\n"
        child_widgets += "\n]"
        script = """<script>
                    $2(document).ready(function(){
                        var name = '%s';
                        var socket = io('%s');

                        $2('#' + name).w2toolbar({
                            name: '%s',
                            items: %s,
                            onClick: function(event){
                                %s
                                socket.emit("fire_click_event", {"target": event.target});
                            }
                        });

                        socket.on("sync_properties_%s", function(props){
                            if(name != undefined){
                                if(props.cmd != undefined){
                                    if(props.cmd == "HIDE-ITEM"){
                                        w2ui[name].hide(props.value);
                                    }
                                    if(props.cmd == "SHOW-ITEM"){
                                        w2ui[name].show(props.value);
                                    }
                                    if(props.cmd == "ENABLE-ITEM"){
                                        w2ui[name].enable(props.value);
                                    }
                                    if(props.cmd == "DISABLE-ITEM"){
                                        w2ui[name].disable(props.value);
                                    }
                                    if(props.cmd == "ADD-ITEM"){
                                        w2ui[name].add(JSON.parse(props.value));
                                    }
                                    if(props.cmd == "INSERT-ITEM"){
                                        w2ui[name].insert(props.ref_item, JSON.parse(props.value));
                                    }
                                    if(props.cmd == "REMOVE-ITEM"){
                                        w2ui[name].remove(props.value);
                                    }
                                } else {
                                    alertify.warning("No command to process");
                                }
                            }
                        });
                    });
                    </script>
                """ % (self._name, self._namespace, self._name, child_widgets,
                       self._onclick_client_script, self._name)
        return script

    def on_fire_click_event(self, props):
        if props.__len__() > 0:
            val = props['target']
            if val is not None:
                self._clicked_item = val
        if self._onclick_callback is not None:
            self._onclick_callback(self._name, props)

    def on_click(self, onclick_callback):
        """Adds an event handler to on_click event of the widget. The event handler can be
        a method or function.

            Args:
                onclick_callback (function): The function/callback that will be called for this event
        """
        self._onclick_callback = onclick_callback

    def render(self):
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += "\n" + self._attach_script()
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


class Sidebar(Widget, Namespace):
    """The w2sidebar object provides a quick solution for a vertical menu. A sidebar can have
    multiple items and some of the items can be nested. The very same object can be used to create
    tree structures too.
    """

    _onclick_callback = None
    _onclick_client_script = None
    _topHTML = None
    _bottomHTML = None
    _flatButton = None
    _clicked_item = None
    _namespace = None
    _socket_io = None

    def __init__(self, name, socket_io, nodes=None, desc=None, prop=None,
                 style=None, attr=None, css_cls=None, onclick_callback=None,
                 onclick_client_script=None, topHTML=None, bottomHTML=None,
                 flatButton=None):
        """
            Args:
                name (string): Name or Id for internal use
                socket_io (SocketIO): An instance of the SocketIO class
                nodes (Widget): Sub Nodes or leaves of the current node
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                onclick_callback (callable): will be called when mouse is clicked on any child item
                onclick_client_script (string): JS to be called when mouse is clicked on any item
                topHTML (string): HTML to show at the top of the sidebar
                bottomHTML (string): HTML to be shown on the bottom of sidebar
                flatButton (boolean): If true, it will show button to minimize or flat the sidebar
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style, attr=attr,
                        css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + str(name) + "_sidebar").replace('.', '_'))
        self._namespace = '/' + str(__name__ + str(name) + "_sidebar").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        if nodes is not None:
            self._child_widgets = nodes
        else:
            self._child_widgets = []
        self._onclick_callback = onclick_callback
        if onclick_client_script is not None:
            self._onclick_client_script = onclick_client_script
        else:
            self._onclick_client_script = ""
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

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

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
        self._sync_properties('ADD-ITEMS', content)

    def insert_items(self, items, ref_item):
        """Insert specified items after the item passed for reference

            Args:
                items (list): List of sidebar nodes
                ref_item (string): Name of the referenced item
        """
        content = []
        for item in items:
            content.append(item.render())
        self._sync_properties('INSERT-ITEMS', content, ref_item)

    def remove_items(self, items):
        """Removes all items from the toolbar passed as arg to this method

            Args:
                items (list): A list of item names to be removed from toolbar
        """
        self._sync_properties('REMOVE-ITEMS', json.dumps(items))

    def show_items(self, items):
        """Shows the hidden items passed as list of item names

            Args:
                items (list): List of names of items
        """
        self._sync_properties('SHOW-ITEMS', json.dumps(items))

    def hide_items(self, items):
        """Hides the specified items passed as list of item names parameter

            Args:
                items (list): List of item names
        """
        self._sync_properties('HIDE-ITEMS', json.dumps(items))

    def enable_item(self, item):
        """Enables an already disabled item in the sidebar

            Args:
                item (string): Name or Id of the item that needs to be enabled
        """
        self._sync_properties('ENABLE-ITEM', item)

    def disable_item(self, item):
        """Disables an already enabled item in the sidebar

            Args:
                item (string): Name or Id of the item that needs to be enabled
        """
        self._sync_properties('DISABLE-ITEM', item)

    def expand_item(self, item):
        """Expands an collapsed item node

            Args:
                item (string): Name or Id of the node that needs to be expanded
        """
        self._sync_properties('EXPAND-ITEM', item)

    def collapse_item(self, item):
        """Collapse an expanded node in the sidebar

            Args:
                item (string): Collapse the provided node
        """
        self._sync_properties('COLLAPSE-ITEM', item)

    def select_item(self, item):
        """Selects the specified item in the sidebar

            Args:
                item (string): Name or Id of the node that needs to be selected
        """
        self._sync_properties('SELECT-ITEM', item)

    def unselect_item(self, item):
        """UnSelects the specidied item in the sidebar

            Args:
                item (string): Name or Id of the node that needs to be unselected
        """
        self._sync_properties('UNSELECT-ITEM', item)

    def click_item(self, item):
        """Emulates an click on the specified node

            Args:
                item (string): Name or Id of the node
        """
        self._sync_properties('CLICK-ITEM', item)

    def on_click(self, click_callback):
        """Registers an method or callback to be called whenever an mouse click event
        is triggered on the widget

            Args:
                click_callback (callable): Function or method that needs to be called
        """
        self._onclick_callback = click_callback

    def _sync_properties(self, cmd, value, ref_item=None):
        emit('sync_properties_' + self._name, {'cmd': cmd, 'value': value,
             'ref_item': ref_item},
             namespace=self._namespace)

    def _attach_script(self):
        child_widgets = "[\n"
        for child in self._child_widgets:
            child_widgets += json.dumps(child.render()) + ",\n"
        child_widgets += "\n]"
        script = """<script>
                    $2(document).ready(function(){
                        var name = '%s';
                        var socket = io("%s");

                        socket.on("sync_properties_%s", function(props){
                            if(name != undefined){
                                if(props.cmd != undefined){
                                    if(props.cmd == "HIDE-ITEMS"){
                                        w2ui[name].hide(JSON.parse(props.value));
                                    }
                                    if(props.cmd == "SHOW-ITEMS"){
                                        w2ui[name].show(JSON.parse(props.value));
                                    }
                                    if(props.cmd == "ENABLE-ITEM"){
                                        w2ui[name].enable(props.value);
                                    }
                                    if(props.cmd == "DISABLE-ITEM"){
                                        w2ui[name].disable(props.value);
                                    }
                                    if(props.cmd == "ADD-ITEMS"){
                                        w2ui[name].add(props.value);
                                    }
                                    if(props.cmd == "INSERT-ITEMS"){
                                        w2ui[name].insert(props.ref_item, props.value);
                                    }
                                    if(props.cmd == "REMOVE-ITEMS"){
                                        w2ui[name].remove(JSON.parse(props.value));
                                    }
                                    if(props.cmd == "COLLAPSE-ITEM"){
                                        w2ui[name].collapse(props.value);
                                    }
                                    if(props.cmd == "EXPAND-ITEM"){
                                        w2ui[name].expand(props.value);
                                    }
                                    if(props.cmd == "SELECT-ITEM"){
                                        w2ui[name].select(props.value);
                                    }
                                    if(props.cmd == "UNSELECT-ITEM"){
                                        w2ui[name].unselect(props.value);
                                    }
                                    if(props.cmd == "CLICK-ITEM"){
                                        w2ui[name].click(props.value);
                                    }
                                } else {
                                    alertify.warning("No command to process");
                                }
                            }
                        });

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
                                    %s
                                    var props = {'target': event.target};
                                    socket.emit('fire_click_event', props);
                                }
                            });
                    });
                    </script>
                """ % (self._name, self._namespace, self._name, self._name,
                       self._name, json.dumps(self._flatButton), self._topHTML,
                       self._bottomHTML, child_widgets, self._name,
                       self._onclick_client_script)
        return script

    def on_fire_click_event(self, props):
        if props.__len__() > 0:
            val = props['target']
            if val is not None:
                self._clicked_item = val
        print('Fire Click Event: ' + val)
        if self._onclick_callback is not None:
            self._onclick_callback()

    def render(self):
        """Renders the sidebar with its nodes and subnodes"""
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += "\n" + self._attach_script()
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


class Form(Widget, Namespace):
    """A form can have multiple fields embedded and provides option to
    either POST data from fields to server for further processing OR
    sends the data from fields to GET more information
    """

    _url = None
    _header = None
    _submit_callback = None
    _reset_callback = None
    _form_data = None
    _socket_io = None
    _namespace = None
    _app = None

    def __init__(self, name, socket_io, app, url=None, header=None,
                 fields=None, desc=None, prop=None, style=None, attr=None,
                 css_cls=None, submit_callback=None, reset_callback=None):
        """
            Args:
                name (string, required): Name or unique id of the object
                socket_io (SocketIO): An instance of the SocketIO class
                app (Flask): An instance of the Flask class
                url (string): Url to which data should be posted. If not
                            provided, the data will be submitted internally
                            to the submit callback handler
                header (string): An title to be shown on top of the form
                fields (FormFieldxxx): Objects of FormFfieldxxx type to read
                                        input from users
                desc (string, optional): description of the button widget
                prop (dict, optional): dict of objects to be added as properties of widget
                style (dict, optional): dict of objects to be added as style elements to HTML tag
                attr (list, optional): list of objects to be added as attributes of HTML tag
                css_cls (list, optional): An list of CSS class names to be added to current widget
                submit_callback (callable): Gets called when form is submitted
                                            and Url parameter is None
                reset_callback (callable): Called when user clicks on the form's
                                            reset button
        """
        Widget.__init__(self, name, desc=desc, prop=prop, style=style,
                        attr=attr, css_cls=css_cls)
        Namespace.__init__(self, '/' + str(__name__ + str(name) + "_form").replace('.', '_'))
        self._namespace = '/' + str(__name__ + str(name) + "_form").replace('.', '_')
        self._socket_io = socket_io
        self._socket_io.on_namespace(self)
        self._app = app
        if url is not None:
            self._url = url
        else:
            self._url = self._namespace
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
        if self._app is None:
            raise ValueError("The value of the 'app' attribute can't be empty")
        found = False
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint == self._url:
                found = True
        if not found:
            self._app.add_url_rule(self._url, self._url,
                                   self.on_submit_click_event,
                                   methods=['POST'])

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = val

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

    def on_submit_click_event(self):
        self._form_data = request.form
        if self._submit_callback is not None:
            try:
                self._submit_callback(request.form)
            except Exception as err:
                return json.dumps({'status': 'error', 'message': str(err)})
        return json.dumps({'status': 'success'})

    def on_reset_click_event(self):
        if self._reset_callback is not None:
            self._reset_callback()

    def _attach_script(self):
        # Prepare the fields to be added to form
        fields = "[\n"
        for field in self._child_widgets:
            fields += field.render() + ",\n"
        fields += "\n]"
        script = """
                <script>
                    $2(function(){
                        var socket = io('%s');

                        $2('#%s').w2form({
                            name: '%s',
                            url: '%s',
                            header: '%s',
                            fields: %s,
                            actions: {
                                reset: function(){
                                    this.clear();
                                    socket.emit('reset_click_event');
                                },
                                save: function(){
                                    this.save();
                                }
                            }
                        });
                    });
                </script>
                """ % (self._namespace, self._name, self._name, self._url,
                       self._header, fields)
        return script

    def render(self):
        """Renders the content of Form widget with its fields to the parent widget"""
        content = self._render_pre_content('div')
        content += self._render_post_content('div')
        content += self._attach_script()
        return content
