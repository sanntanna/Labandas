lb = window.lb || {};

lb.soundcloud = function(instanceParams, targetElement){
	var instance = this;
	
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
		if(p.height == undefined) p.height = '166';
		if(p.autoPlay == undefined) p.autoPlay = false;
		if(p.showArtwork == undefined) p.showArtwork = false;

		return p;
	}

	function render(p){
		if(p.url == undefined) {
			throw new Error("Informe a url do player");
		}

		if(!isUrlSoundCloud(p.url)){
			throw new Error("Url de player do soundcloud inválida");	
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
		return ('https://w.soundcloud.com/player/?color=ff6600')
				.param('auto_play', p.autoPlay)
				.param('show_artwork', p.showArtwork)
				.param('url', escape(p.url));
	}

	function isUrlSoundCloud(url){
		return url.indexOf("//soundcloud.com/") > -1;
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