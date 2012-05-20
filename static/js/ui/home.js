(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSubscribeForm();
		setupCepUpdate();
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
	
	function setupCepUpdate(){
		$("#save-cep").click(function(){
			$.get('/musico/atualizar-endereco', {'cep': $("#cep").val()});
		});
	}
	
	this.init();
	$(this.domLoaded);
})();