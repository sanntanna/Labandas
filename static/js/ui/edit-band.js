(function(){
	this.init = function(){};
	this.domLoaded = function(){
		setupForm();
		setupFormation();
	};
	
	function setupForm(){
		$("#edit-band-form").bind('ajaxcomplete', function(e, response){
			if(response.success){
				location.href = "/";
			}
		});
	}
	
	function setupFormation(){
		$(document).delegate('.remove-musician', 'click', function(e){
			e.preventDefault();
			var link = $(this),
				parent = link.closest('.musician-info-line');
			
			$.post('/banda/formacao/remover', {id: link.attr('data-id')}, function(){
				parent.fadeOut(300, function(){ parent.remove() });
				new lb.message('Musico removido', lb.message.SUCCESS);
			});
		});
		
		$("#add-musicians").click(function(e){
			
		});
	}
	
	this.init();
	$(this.domLoaded);
}());