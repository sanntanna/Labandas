(function(){
	this.init = function(){};
	this.domLoaded = function(){
		setupForm();
		setupFormation();
	};
	
	
	var lightboxSearch = null,
		equipamentsLoaded = false;
	
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
			
			$.post('/banda/formacao/remover', {id: link.attr('data-id')}, function(response){
				if(!response.success){
					new lb.message('Erro ao remover o músico', lb.message.ERROR);
					return;
				}
				parent.fadeOut(300, function(){ parent.remove() });
				new lb.message('Musico removido', lb.message.SUCCESS);
			});
		});
		
		$(document).delegate('.remove-solicitation', 'click', function(e){
			e.preventDefault();
			var link = $(this),
				parent = link.closest('.musician-info-line');
			
			$.post('/solicitacao/cancelar', {id: link.attr('data-id')}, function(response){
				if(!response.success){
					new lb.message('Erro ao remover a solicitação', lb.message.ERROR);
					return;
				}
				
				parent.fadeOut(300, function(){ parent.remove() });
				new lb.message('Solicitação removida', lb.message.SUCCESS);
			});
		});
		
		
		$("#add-musicians").click(function(e){
			e.preventDefault();
			openMusiciansSearch();
		});
		
		
		$(document).delegate("#search-musicians-form", 'ajaxcomplete', function(e, response){
			e.preventDefault();
			if(!response.success){
				return;
			}
			
			renderMusicians(response.musicians);
		});
		
		$(document).delegate(".musician-finded", 'click', function(e){
			e.preventDefault();
			showInstruments();
			$("#target_id").val($(this).attr('data-id'))
		});
		
		$(document).delegate("#add-to-band", "ajaxcomplete", function(e, data){
			if(data.success){
				lightboxSearch.close();
				$("#instruments").hide();
				new lb.message('Solicitação enviada para o musico #musico#', lb.message.SUCCESS);
			}
		});
	}
	
	function openMusiciansSearch(){
		var content = ['<div id="wrapper-search">',
		               	   '<form id="search-musicians-form" method="get" action="/musico/buscar" class="ajax">',
			               '<input type="text" id="musician-search-field" placeholder="digite o nome ou email" name="q" />',
			               '<input type="submit" id="button-do-search" value="buscar" />',
			               '</form>',
			               '<div id="musician-search-results">',
				               '<ul id="results-list">',
				               '</ul>',
				           '</div>',    
			           '</div>'].join('');
		
		lightboxSearch = new lb.lightbox({content: content, width:600, height: 250});
	}
	
	function renderMusicians(musiciansList){
		var content = musiciansList.map(function(m){
			return '<li><a href="#add-this-musician" class="musician-finded" data-id="' + m.pk + '">' + m.user__first_name + '</a></li>';
		}).join('');
		
		$("#results-list").html(content);
	}
	
	
	function showInstruments(){
		if(equipamentsLoaded){
			$("#instruments").fadeIn();
			return;
		}
		
		$.get('/equipamentos/instrumentos', null, function(response){
			var list = response.instruments;
			
			$("#list-instruments").html(list.map(function(instrument){
				return 	['<label>' ,
							'<input type="checkbox" value="', instrument.pk, '" name="instruments" />', instrument.name,
						'</label>'].join('');
			}).join(''));
			
			$("#instruments").fadeIn();
			equipamentsLoaded = true;
		});
	}
	
	this.init();
	$(this.domLoaded);
}());