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
    _footer = None
    _sort_on = None
    _sort_dir = None
    _data_load_callback = None
    _app = None
    _onclick_callback = None
    _disabled = None
    _select_column = None
    _multi_select = None
    _line_numbers = None
    _queue = None
    _multi_search = None

    def __init__(self, name, header, column_collection, row_collection=None, desc=None,
                 prop=None, style=None, attr=None, disabled=False, onclick_callback=None,
                 app=None, css_cls=None, data_url=None, data_load_callback=None,
                 toolbar=None, footer=None, sort_on=None, sort_dir=None, select_column=None,
                 multi_select=None, line_numbers=None, search_collection=None, multi_search=None):
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

    def _attach_script(self):
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
                                    lineNumbers: %s
                                },
                                multiSelect: %s,
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
                       json.dumps(self._multi_select), self._sort_on, self._sort_dir,
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
                                    lineNumbers: %s
                                },
                                multiSelect: %s
                                sortData: [{field: '%s', direction: '%s'}],
                                multiSearch: %s
                                %s  //searches placeholder
                            });
                        });
                    </script>
                    """ % (self._name, self._name, self._header, self._column_collection.render(),
                           self._data_url, json.dumps(self._tool_bar), json.dumps(self._footer),
                           json.dumps(self._select_column), json.dumps(self._line_numbers),
                           json.dumps(self._multi_select), self._sort_on, self._sort_dir,
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
                                    lineNumbers: %s
                                },
                                multiSelect: %s,
                                sortData: [{field: '%s', direction: '%s'}],
                                multiSearch: %s
                                %s  //searches placeholder
                            });
                        });
                    </script>
                    """ % (self._name, self._name, self._header, self._column_collection.render(),
                           url, json.dumps(self._tool_bar), json.dumps(self._footer),
                           json.dumps(self._select_column), json.dumps(self._line_numbers),
                           json.dumps(self._multi_select), self._sort_on, self._sort_dir,
                           json.dumps(self._multi_search),
                           (", searches: " + self._search_collection if self._search_collection is not None else ""))
            if not found:
                self._app.add_url_rule('/' + url, url,
                                       self._process_data_load_callback)
        return script

    def _process_data_load_callback(self):
        record_collection = self._data_load_callback()
        self._row_collection = record_collection
        result = "{\n'total': " + record_collection.records.__len__() + ",\n"
        result += "'records': " + record_collection.render()
        return result

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
                """ % (url, url, self._name, self._name, url)  # self._name, self._name, url)
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
