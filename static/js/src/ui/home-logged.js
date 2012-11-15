(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupInlineEdition();
		setupCheckUncheckIcons();
		setupSolicitations();
	};
	
	function setupInlineEdition(){

		var updateData = function(){
			var $elm = $(this);

			var dataField = (this.name || $elm.attr('data-field')).split('.'),
				val = this.value || $.trim(this.innerHTML);

			var postData = {},
				url = "";

			if(dataField.length == 1){
				postData[dataField[0]] = val;
				url = dataField[0];
			} else {
				postData[dataField[1]] = val;
				url = dataField[0] + '/' + dataField[1];
			}

			if($elm.attr('data-single')){
				postData['single'] = true;
			}

			$.post('/musico/atualizar/' + url, postData);
		}

		$("#main.can-edit .editable").click(function(){
			$(this).attr('contenteditable', true)
					.html($.trim(this.innerHTML));
		}).keydown(function(e){
			if(e.keyCode == 13){ 
				$(e.target).trigger('enterpress'); 
				return false;
			}
		}).bind('blur enterpress', function(){
			$(this).removeAttr('contenteditable');
			updateData.apply(this, arguments);
		});

		$("form.inline-form input").change(function(){
			$(this).closest('form').trigger('submit');
		});
	}
	
	function setupCheckUncheckIcons(){
		$('.check-icon').each(function(){
			$(this).bind('mouseup', function(){
				var $icon = $(this);
				setTimeout(function(){
					var fn = $icon.find('input:checked').length ? 'addClass' : 'removeClass';
					$icon[fn]('active');
				}, 10)
			}).trigger('mouseup');
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