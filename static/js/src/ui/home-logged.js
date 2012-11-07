(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupInlineEdition();
		setupSolicitations();
	};
	
	function setupInlineEdition(){
		$("#main.can-edit .editable").click(function(){
			var $div = $(this);

			if($div.find('input').length){return;}

			this.originalContent = $.trim($div.html());
			var ipt = input($div);
			$div.html("").append(ipt);
			ipt[0].focus();
		}).keyup(function(e){
			if(e.keyCode == 13){ $(e.target).trigger('enterpress'); }
		});

		$("form.inline-form input").change(function(){
			$(this).closest('form').trigger('submit');
		});

		$(document).delegate('input.post-on-edit', 'change', function(e){
			var dataField = this.name.split('.'),
				val = this.value;

			var postData = {};
			postData[dataField[1]] = val;
			$.post('/musico/atualizar/' + dataField[0] + '/' + dataField[1], postData);
		});

		function input($elm, type){
			return $('<input type="text" class="post-on-edit" />')
					.attr('name', $elm.attr('data-field'))
					.width($elm.width())
					.val($elm[0].originalContent)
					.bind('blur enterpress', inlineInputBlur);
		}

		function inlineInputBlur(e){
			var $parent = $(this).parent(),
				val = this.value;

			$parent.html(val != "" ? val : $parent[0].originalContent );
		}
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