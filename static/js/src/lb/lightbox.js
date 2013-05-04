lb = window.lb || {};

lb.lightbox = function(param){
	var instance = this;

	window.lastLightbox = instance;

	instance.defaults = {
		minWidth: 380,
		minHeight: 150,
		overlay: null
	};
	
	instance.container = null;
	instance.box = null;
	instance.content = null;

	var url, width, height, text;
	
	var cssOverlay = {
		width: '100%',
		height: '100%',
		position:'fixed',
		top: '0px',
		left: '0px',
		background: '#000',
		opacity: '0.55',
		display: 'none',	
		zIndex: 1
	};
	
	var cssContainer = {
		position: 'fixed',
		width: '100%',
		height: '100%',
		textAlign: 'center',
		top: '0px',
		left: '0px',
		zIndex: 2
	}
	
	var cssWrapper = {
		margin: '180px auto auto',
		position: 'relative',
		textAlign:'left'
	}
	
	var csssContent = {
		background: '#454545',
		display:'table'
	}
	
	
	function init(param){
		if(typeof param == 'string'){
			if(isCssSelector(param)) {
				text = $(param).show();
				instance.id = param;
			} 
			else if(isText(param)){
				text = param;
			} 
			else {
				url = param;
				width = url.param('width');
				height = url.param('height');
				instance.id = url;
			}
		} else if(typeof param == 'object'){
			url = param.url || url;
			text = param.content || text;
			width = param.width;
			height = param.height;
			instance.id = url;
		}

		open();
	}

	function isText(str){
		return typeof str == 'string' && str.match(/^([^<>'"])*(\/)*/gi) == null;
	}

	function isCssSelector(str){
		return str.match(/^(#|\.[a-zA-Z])([^\/?<]*)$/g) != null;
	}

	function open(){
		instance.container = render().appendTo('body');
		instance.box = instance.container.find('.lightbox-wrapper');
		instance.content = instance.box.find('.lightbox-content');
		instance.loading = instance.box.find('.lightbox-loading');
		loadContent(show);
	}
	
	function render(){
		if(instance.defaults.overlay === null){
			instance.defaults.overlay = $('<div id="lightbox-overlay"></div>').css(cssOverlay).appendTo('body');
		}
		
		var content = $(['<div class="lightbox-container">',
		                 	'<div class="lightbox-wrapper">',
			               		'<div class="lightbox-content"></div>',
			               		'<div class="lightbox-loading"></div>',
			               		'<div class="tr"><a href="#close" class="lightbox-close lightbox-close-tr">x</a></div>',
			               '</div>',
			             '</div>'].join('')).css(cssContainer);
		
		
		content.find('.lightbox-wrapper').css(cssWrapper).find('.lightbox-content').css(csssContent).hide();
		content.delegate('.lightbox-close', 'click', function(e){
			e.preventDefault();
			instance.close();
		});
		
		return content;
	}
	
	function loadContent(callback){
		if(url == null){
			callback.call();
			return;
		}

		instance.loading.show();

		$.get(url, null, function(response){
			instance.loading.hide();
			callback.apply(null, arguments);
		}).error(function(){
			var msg = 'Erro ao carregar a url "<a href="' +  url + '" target="_blank">' + url + '</a>"';
			new lb.message(msg, lb.message.ERROR);
			instance.close();
		});
	}
	
	function show(response){
		instance.defaults.overlay.show();
		
		var content = response || text;

		if(content instanceof jQuery){
			instance.originalContent = content;
			content.after('<input type="hidden" id="lightbox-replacer" />');
		}

		instance.content.html(content);

		if(width){ instance.content.width(width); }
		if(height){ instance.content.height(height); }

		var _width = Math.max(instance.content.width() || 0, instance.defaults.minWidth);
		var _height = Math.max(instance.content.height() || 0, instance.defaults.minHeight);

		
		instance.box.centralize(_height).width(_width).height(_height);

		instance.content.hide().fadeIn();
	}

	instance.close = function(callback){
		instance.box.fadeOut(300, function(){
			$(document).trigger('lightboxclosed', instance);

			instance.container.remove();
			instance.defaults.overlay.hide();

			if(callback){
				callback.call();
			}
			
			if(instance.originalContent){
				$("#lightbox-replacer").replaceWith(instance.originalContent.hide())
			}
		});
	};
	
	init(param);

	return instance;
};

lb.lightbox.globalSetup = function(settings){
	$.extend(this.defaults, settings);
};

(function($){
	$.fn.centralize = function(expectedHeight){
		var t = $(this),
			height = (expectedHeight || t.height()),
			totalHeight = t.parent().height();
		
		t.css('margin-top', ((totalHeight - height) / 2) + 'px');

		return this;
	}
}(jQuery));