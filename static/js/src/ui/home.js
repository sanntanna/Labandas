(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSubscribeForm();
		setupInlineEdition();
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
	
	function setupInlineEdition(){
		$("form.inline-form input").change(function(){
			$(this).closest('form').trigger('submit');
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