(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupAskMusician();
	};
	
	var bandsLoaded = false,
		equipamentsLoaded = false,
		selectedBandId = -1;
	
	function setupAskMusician(){
		$("#ask-musician").click(function(e){
			e.preventDefault();
			showBands();
		});
		
		$(document).delegate('.add-in-this-band', 'click', function(e){
			e.preventDefault();
			
			var link = $(this);
			selectedBandId = link.attr('data-id');
			link.closest('ul').find('.selected').removeClass('selected');
			link.addClass('selected');
			showInstruments();
		});
		
		$("#ask-musician-complete").click(function(e){
			e.preventDefault();
			var postData = {
				band_id: $("#instruments").attr('data-id'),
				instruments: $("#list-instruments input:checked").val(),
				musician: 6
			}
			
			$.post('/solicitacao/musico/enviar', postData, function(){
				
			}); 
		});
	}
	
	function showBands(){
		if(bandsLoaded){
			$("#list-your-bands").slideToggle();
			$("#instruments").fadeOut()
			return;
		}
		
		$.get('/musico/bandas', null, function(response){
			var list = response.bands;
			
			$("#bands").html(list.map(function(band){
				return '<li><a href="#adicionar-nessa" class="add-in-this-band" data-id="' + band.band__id + '">' + band.band__name + '</a>';
			}).join(''));
			
			$("#list-your-bands").slideDown();
			
			bandsLoaded = true;
		});
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
							'<input type="checkbox" value="', instrument.pk, '" />', instrument.name,
						'</label>'].join('');
			}).join(''));
			
			$("#instruments").fadeIn();
			equipamentsLoaded = true;
		});
	}
	
	
	this.init();
	$(this.domLoaded);
})();