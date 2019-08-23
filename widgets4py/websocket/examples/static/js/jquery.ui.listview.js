$(function() {

  //ListView widget to display list of items and provides ability to
  //select list elements
  $.widget("widgets4py.listview", {
    options: {
      selectedItems: [],
      disabled: false,
      corners: false,
      //selected item callback
      onSelected: null
    },

    _create: function() {
      //Add css classes
      this.element.addClass('ui-widget');
      this.element.addClass('ui-widget-shadow');
      this.element.addClass('listview');

      //Get H1 and UL elements and add css
      var mainChilds = this.element.children();
      mainChilds[0].classList.add('ui-widget-header'); //H1 element
      this._ul = mainChilds[1]; //UL element
      this._ul.classList.add('ui-widget-content');
      this._childElements = this._ul.children;

      //bind click to all child elements
      for (i = 0; i < this._childElements.length; i++) {
        var li = this._childElements[i];
        li.classList.add('ui-widget-content');

        $(li).bind("mouseover", function() {
          this.classList.add('ui-state-hover');
        });
        $(li).bind("mouseleave", function() {
          this.classList.remove('ui-state-hover');
        });

        this._on(li, {
          click: "select"
        });
      }
    },

    _refresh: function() {
      var childs = this._ul.children;
      var count = childs.length;
      var newLi = childs[count - 1];
      newLi.classList.add('ui-widget-content');

      $(newLi).bind("mouseover", function() {
        this.classList.add('ui-state-hover');
      });
      $(newLi).bind("mouseleave", function() {
        this.classList.remove('ui-state-hover');
      });

      this._on(newLi, {
        click: "select"
      });
    },

    addItem: function(id, val) {
      itemCounter = this._childElements.length;
      $('<li id="' + id + '"><label>' + val + '</label></li>').appendTo(this._ul)
      this._refresh();
    },

    removeItem: function(id) {
      $('#' + id).remove();
    },

    select: function(event) {
      var li = event.currentTarget;
      li.classList.toggle('ui-state-active');
      if (this.options.selectedItems.includes(li.id)) {
        this._removeArrayItem(this.options.selectedItems, li.id);
      } else {
        this.options.selectedItems.push(li.id);
      }

      this._trigger("onSelected");
    },

    selectItems: function(items) {
      this.options.selectedItems = []
      for (i = 0; i < items.length; i++) {
        for (j = 0; j < this._childElements.length; j++) {
          var li = this._childElements[j];
          var item_id = li.id;
          if (item_id == items[i]) {
            li.classList.add('ui-state-active');
            this.options.selectedItems.push(item_id);
          }
        }
      }
    },

    unselectItems: function(items) {
      for (i = 0; i < items.length; i++) {
        for (j = 0; j < this._childElements; j++) {
          var li = this._childElements[j];
          var item_id = li.id;
          if (item_id == items[i]) {
            li.classList.remove('ui-state-active');
            this._removeArrayItem(this.options.selectedItems, item_id);
          }
        }
      }
    },

    _removeArrayItem: function(arr, item) {
      for (var i = 0; i < arr.length; i++) {
        if (arr[i] === item) {
          arr.splice(i, 1);
        }
      }
    },

    _destroy: function() {},
    _setOption: function(key, value) {
      if (key === "disabled") {
        if (value != undefined && value) {
          this.element.addClass('li-state-disabled');
        } else if (value != undefined && !value) {
          this.element.removeClass('ui-state-disabled');
        }
      } else if (key === "corners") {
        if (value != undefined && value) {
          this.element.addClass('ui-corner-all');
        } else if (value != undefined && !value) {
          this.element.removeClass('ui-corner-all');
        }
      }
      this._super(key, value);
    }
  });
});
