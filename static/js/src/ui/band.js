(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSoundCloud();
		setupSetlist();
		announcements();
		addMusician();
	};
	
	function setupSoundCloud(){
		$(document).delegate("#sound-cloud-url", "textchanged", function(){
			try{
				var config = {url: $("#sound-cloud-url").val(), autoPlay: true};
				new lb.soundcloud(config, "#sound-cloud-player-preview");
				$("#preview-message-default").hide();
			} catch(e){
				$("#preview-message-default").show();
				new lb.message("Url de perfil do soundcloud inválida", lb.message.ERROR);
			}
		});

		$(document).delegate("#confirm-soundcloud-music", "click", function(){
			var url = $("#sound-cloud-url").val();
			$("#sound-cloud-url-value").val(url).trigger('change');
			$(".soundcloud").hide();
			new lb.soundcloud(url, "#user-soundcloud-player");
		});
	}

	function setupSetlist(){
		$(document).delegate('#setlist', 'ajaxcomplete', function(e, response){
			if(!response.success){
				new lb.message("Erro ao adicionar a musica", lb.message.ERROR);
				return;
			}

			if(!response.music_title){
				location.reload();
				return;
			}

			var $list = $(".list-music"),
				$newItem = $list.find("li:first").clone();

			$newItem.find('span').html(response.music_title);
			$newItem.find('a').attr('data-id', response.music_id);

			$list.prepend($newItem);

			$("#music-title").val("");

		});

		$(document).delegate(".remove-music", "click", function(e){
			e.preventDefault();
			var $link = $(this),
				$li = $link.closest('li');
			$.post('/banda/remover/setlist', {id: $link.data('id')}, function(){

				if($(".list-music li").length <= 1){
					location.reload();
					return;
				}

				$li.hide(300, function(){
					$li.remove();
				});
			});
		});
	}

	function announcements(){
		$(document).delegate("#create-announcement-form", "ajaxcomplete", function(e, response){
			if(!response.success){
				return;
			}
			$("#collpase-announcement").trigger("click");
			new lb.message("O anuncio foi criado. Busque musicos que se enquadram nele.", lb.message.SUCCESS);

		});

		$(document).delegate(".candidate-to-announcement", "click", function(e){
			e.preventDefault();
			var $link = $(this);

			$.post('/anuncio/se-candidatar', {id: $link.data('id') }, function(response){
				if(!response.success){ return; }

				$link.closest('.candidade-wrapper')
					.after('<div class="already-candidated">Você se candidatou para esse anuncio, agora só aguardar.</div>')
					.fadeOut();
			});
		});
	}

	function addMusician(){
		function printResults(musicians){
			if(musicians.length == 0){
				$('#founded-musicians').html('<li> <em>Nenhum musico encontrado</em> </li>')
				return;
			}

			var result = musicians.map(function(musician){
				return ['<li>',
					musician.avatar ? '<img class="fl" src="' + musician.avatar + '"/>' : '',
					'<div class="name fl">', musician.name, '</div>',
					'<div class="button fl"><a href="#add-to-band" data-id="', musician.id, '" class="btn add">Adicionar a banda</a></div>',
				'</li>'].join('');
			});

			$('#founded-musicians').html(result.join(''));
		}

		$(document).delegate('#find-musicians-to-band', 'click', function(e){
			$.get('/musico/buscar', {kw: $('#musician-kw').val()}, function(response){
				printResults(response.musicians);
			})
		});

		var currentId = null,
			$lightbox = null;

		$(document).delegate('#founded-musicians a.add', 'click', function(e){
			e.preventDefault();
			var $link = $(this);

			if(!$lightbox){ $lightbox = $("#add-musician-lightbox"); }

			currentId = $link.data('id');
			$("#target-musician-name").html( $link.closest('li').find('.name').html() );
			$lightbox.find(".instruments").html( $("#band-looking .instruments").html() );

			$lightbox.find(".search-musician").fadeOut(200, function(){
				$(".what-play").fadeIn();
			});
		});

		$(document).delegate('#back-to-search', 'click', function(){
			$(".what-play").fadeOut(200, function(){
				$lightbox.find(".search-musician").fadeIn();
			});
		});

		$(document).delegate('#send-solicitation', 'click', function(e){
			var dataToSend = [$lightbox.find('input:checkbox:checked').serialize(),
								'target=' + currentId,
								'band=' + $('body').data('id')].join('&');
			$.post('/solicitacao/enviar-para-musico', dataToSend, function(response){
				window.lastLightbox.close();

				if(response.success){
					new lb.message("Sua solicitação foi enviada", lb.message.SUCCESS);
					return;
				}

				new lb.message("Erro ao enviar a solicitação", lb.message.ERROR);
			});
		});
	}

	this.init();
	$(this.domLoaded);
})();