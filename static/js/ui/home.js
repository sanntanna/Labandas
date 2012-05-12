lb = window.lb || {};

lb.home = function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSubscribeForm();
	};
	
	function setupSubscribeForm(){
		$("#subscribe-form").bind('ajaxcomplete', function(e, response){
			if(response.success){
				location.reload();
				return;
			}
			
			var messageBuilder = [],
				field;
			
			for(field in response.errors){
				messageBuilder.push(field + ':' + response.errors[field][0]);
			}
			
			new lb.message(messageBuilder.join('<br />'), lb.message.type.ERROR);
		});
	}
	
	this.init();
	$(this.domLoaded);
}

new lb.home();