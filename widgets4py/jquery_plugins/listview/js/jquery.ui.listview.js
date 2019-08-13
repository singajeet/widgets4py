$ (function(){

    //ListView widget to display list of items and provides ability to
    //select list elements
    $.widget("widgets4py.listview", {
      options: {
        selectedItems: [],
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
        for(i=0; i<this._childElements.length; i++){
        	var li = this._childElements[i];
	    		li.classList.add('ui-widget-content');
        	var liChilds = li.children;
        	var inputCheck = liChilds[0];

          $(li).bind("mouseover", function(){this.classList.add('ui-state-hover');});
        	$(li).bind("mouseleave", function(){this.classList.remove('ui-state-hover');});

          this._on(inputCheck, {
            click: "select"
          });
        }
      },

      _refresh: function(){
		    var childs = this._ul.children;
		    var count = childs.length;
		    var newLi = childs[count-1];
		    newLi.classList.add('ui-widget-content');
		    var liChilds = newLi.children;
		    var inputCheck = liChilds[0];

        $(newLi).bind("mouseover", function(){this.classList.add('ui-state-hover');});
        $(newLi).bind("mouseleave", function(){this.classList.remove('ui-state-hover');});

        this._on(inputCheck, {
          click: "select"
        });
      },

      addItem: function(id, val){
	  	  itemCounter = this._childElements.length;
		    $('<li><input type="checkbox" id="' + id + '" /><label for="' + id + '" >' + val + '</label></li>').appendTo(this._ul);
		    this._refresh();
      },

      removeItem: function(id){
        $('#' + id).remove();
      },

      select: function(event){
        var checkBox = event.currentTarget;
        checkBox.parentElement.classList.toggle('ui-state-active');
		    if(this.options.selectedItems.includes(checkBox.id)){
			   this._removeArrayItem(this.options.selectedItems, checkBox.id);
		    } else {
			   this.options.selectedItems.push(checkBox.id);
		    }

        this._trigger("onSelected");
      },

      _removeArrayItem: function(arr, item){
        for(var i=0; i < arr.length; i++){
          if(arr[i] === item){
            arr.splice(i, 1);
          }
        }
      }
    });
});
