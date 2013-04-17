(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSoundCloud();
		setupSetlist();
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
			var $link = $(this);
			$.post('/banda/remover/setlist' {id: $link.data('id')}, function(){
				$link.hide(300, function(){
					$link.remove();
				});
			});
		});
	}

	this.init();
	$(this.domLoaded);
})();