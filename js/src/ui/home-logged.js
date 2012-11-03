(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupInlineEdition();
		setupSolicitations();
	};
	
	function setupInlineEdition(){
		$("#main.can-edit .editable").click(function(){
			var $t = $(this);

			if($t.find('input').length){return;}

			this.originalContent = $.trim($t.html());
			var ipt = input($t);
			$t.html("").append(ipt);
			ipt[0].focus();
		})
		.keyup(function(e){
			if(e.keyCode == 13){ $(e.target).trigger('enterpress'); }
		});

		$("form.inline-form input").change(function(){
			$(this).closest('form').trigger('submit');
		});

		function input($elm, type){
			return $('<input type="text" />')
					.attr('name', $elm.attr('data-field'))
					.css('width', $elm.width())
					.val($elm[0].originalContent)
					.bind('blur enterpress', function(){
						var $parent = $(this).parent();
						$parent.html(this.value != "" ? this.value : $parent[0].originalContent );
					});
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