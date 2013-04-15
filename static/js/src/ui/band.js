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
		$(document).delegate('#form-setlist', 'ajaxcomplete', function(e, response){
			console.log('response');
		});

		$(document).delegate(".remove-music", "click", function(e){
			e.preventDefault();
			alert('remover musica');
		});
	}

	this.init();
	$(this.domLoaded);
})();