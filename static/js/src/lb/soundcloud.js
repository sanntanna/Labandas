lb = window.lb || {};

lb.soundcloud = function(instanceParams, targetElement){
	var instance = this;
	
	var urlRegex = /^(https\:\/\/)?([a-z.]*)\/([^\/?]*)([^\/]*)$/gi;

	function init(){
		instanceParams = handleDefaults(instanceParams);
		render(instanceParams);
	}

	function handleDefaults(p){
		if(typeof p == "string"){
			var url = p;
			p = {url: url};
		}

		if(p.width == undefined) p.width = '100%';
		if(p.height == undefined) p.height = '250';
		if(p.autoPlay == undefined) p.autoPlay = false;
		if(p.showArtwork == undefined) p.showArtwork = true;
		if(p.show_comments == undefined) p.show_comments = false;
		if(p.liking == undefined) p.liking = false;
		return p;
	}

	function render(p){
		if(p.url == undefined) {
			throw new Error("Informe a url do perfil");
		}

		if(!isUrlSoundCloud(p.url)){
			throw new Error("Url de perfil do soundcloud inválida");	
		}

		instance.frame = $("<iframe></iframe>");
		instance.frame[0].playerInstance = this;

		instance.frame.attr({
			'width': p.width,
			'height': p.height,
			'scrolling': 'no',
			'frameborder': 'no',
			'src': frameUrl(p)
		});

		$(targetElement).html(instance.frame);
	}

	function frameUrl(p){
		var userName = p.url.replace(urlRegex, "$3")

		return ('https://w.soundcloud.com/player/?color=8fb04e')
				.param('auto_play', p.autoPlay)
				.param('show_artwork', p.showArtwork)
				.param('liking', p.liking)
				.param('show_comments', p.show_comments)
				.param('url', escape("http://api.soundcloud.com/" + userName));
	}

	function isUrlSoundCloud(url){
		return url.match(urlRegex) != null;
	}

	init();

	return instance;
};

lb.soundcloud.globalInit = function(){
	$('.soundcloud-player').each(function(){
		var $elm = $(this);
		new lb.soundcloud($elm.attr('data-src'), $elm);
	});
}