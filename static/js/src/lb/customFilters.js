lb.customFilters = (function($){
	var exports = {};
	
	exports.init = function(){
		
		_initEvents();
	};
	
	function _initEvents(){
		
		$('.custom_select a').click(function(e){
			e.preventDefault();
		});
		
		$('.custom_select').click(function(e){
			e.stopPropagation();
			
			var $t = $(this),
				$dropdown = $t.find('.dropdown'),
				$list = $t.find('ul'),
				generated = false;
			
			if(!$dropdown.length){
				$dropdown = $('<div class="dropdown"></div>');
				var $newOptions = $list.clone();
				$newOptions.find('li:first').remove();
				
				$dropdown.append( $newOptions );
				$t.append($dropdown);
				
				generated = true;
			}
			
			if ($dropdown.is(':visible') && !generated) {
				$dropdown.hide();
			} else {
				$dropdown.show();
			}
			
			$('.custom_select').not($(this)).find('.dropdown').hide();
			
			$(document).delegate('body', 'click', function(e){
				$('.dropdown').hide();
				$(document).unbind('click');
			});
		}).each(function(){
			var childsSelecteds = $(this).find('li.selected');
			if(childsSelecteds.length > 1){
				childsSelecteds.filter(':gt(0)').hide();
			}
		});
	}
	
	return exports;
}(jQuery));