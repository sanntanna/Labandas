lb = window.lb || {}

lb.formAjax = function(){
	this.init = function(selector){
		$(document).delegate(selector, 'submit', function(e){
			e.preventDefault();
			handleSubmit.call(this, e);
		});
	}
	
	function handleSubmit(e){
		var data = {},
			form = $(this);
		form.find('input:text, input:password, input:checked, select, textarea').each(function(){
			if(this.name == '') return;
			data[this.name] = this.value;
		})
		
		$.post(this.action, data, function(response){
			form.trigger('ajaxcomplete', response);
		});
	}
};