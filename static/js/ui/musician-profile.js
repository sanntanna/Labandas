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
		});
	}
	
	function setupCepUpdate(){
		$("#save-cep").click(function(){
			$.get('/musico/atualizar-endereco', {'cep': $("#cep").val()}, function(){
				new lb.message('Seu cep foi atualizado', lb.message.SUCCESS);
			});
		});
	}
	
	this.init();
	$(this.domLoaded);
})();