(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSubscribeForm();
		setupCepUpdate();
		setupSolicitations();
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
	
	function setupSolicitations(){
		$(".accept-solicitation, .decline-solicitation").click(function(e){
			e.preventDefault();
			
			var link = $(this),
				isAccepting = link.hasClass('accept-solicitation'),
				url = "/solicitacao/" + (isAccepting ? 'aceitar' : 'recusar');
			
			$.post(url, {id: link.attr('data-id')}, function(response){
				link.closest('.solicitation').hide(700, function(){
					$(this).remove();
				});
				
				if(isAccepting){
					new lb.message("Agora você está na banda #banda#", lb.message.SUCCESS);
				}
			});
		});
	}
	
	this.init();
	$(this.domLoaded);
})();