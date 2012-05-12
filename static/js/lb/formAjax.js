lb = window.lb || {};


lb.formAjax = function(){
	var prototype = lb.formAjax.prototype;
	var $ = jQuery;
	
	prototype.globalInit = function(selector){
		$(document).delegate(selector || 'form.ajax', 'submit validationsuccess', onSubmit);
	};

	prototype.execute = function(form){
		if(!(form instanceof jQuery)) {form = $(form);}
		form.trigger('validationsuccess');
	};
	
	function onSubmit(e){
		if(e.type == 'submit'){
			e.preventDefault();
		}
		
		var $form = $(this);
		
		/*if(e.type != 'validationsuccess' && $form.is(lb.formValidate.globalSelector)){
			return;
		}
		
		if(e.isDefaultPrevented() && e.type == 'validationsuccess'){
			return;
		}*/
		
		$form.find('.form_ajax_loader').show();
				
		var method = ($form.attr('method').toLowerCase() == 'post') ? 'post' : 'get';
		$[method]($form.attr('action'), $form.serialize(), function(response, isSuccess, httpReqObj){
			$form.find('.form_ajax_loader').hide();
			$form.trigger('ajaxcomplete', response);
		});
	}
};