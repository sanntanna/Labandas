(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		gallery();
		photos();
		videos();
	};

	function gallery(){
		var $current = null;

		var LEFT = 37,
			RIGHT = 39,
			ESC = 27;

		function handleNextPrev($box){
			var $gallery = $('.media-gallery'),
					index = $gallery.index($(this));

			$box.find(".prev, .next").show();

			if(index == 0){
				$box.find(".prev").hide();
			} 

			if(index == $gallery.length - 1){
				$box.find(".next").hide();
			}
		}

		var handlers = {
			'default': function(url){
				var $photoLarge = $('#photo-large');

				if(!$photoLarge.length){
					$photoLarge = $(['<div id="photo-large" class="opened-media">',
										'<span class="close">x</span>',
										'<span class="prev">&lt;</span>',
										'<img src="', url, '" />',
										'<span class="next">&gt;</span>',
								   '</div>'].join(''));

					$('body').append($photoLarge);
				} else {
					$photoLarge.find('img').attr('src', url);
				}

				$current = $(this);

				handleNextPrev.call(this, $photoLarge);
			},

			'video': function(url){
				var $videoLarge = $('#video-large'),
					baseUrl = 'http://www.youtube.com/embed/';

				if(!$videoLarge.length){
					$videoLarge = $(['<div id="video-large" class="opened-media">',
										'<span class="close">x</span>',
										'<span class="prev">&lt;</span>',
										'<iframe width="853" height="480" src="', baseUrl, url, '" frameborder="0" allowfullscreen></iframe>',
										'<span class="next">&gt;</span>',
								   '</div>'].join(''));

					$('body').append($videoLarge);
				} else {
					$videoLarge.find('iframe').attr('src', baseUrl + url);
				}

				$current = $(this);

				handleNextPrev.call(this, $videoLarge);
			}
		};

		function handleNavigation(e){
			if(e.keyCode == LEFT){
				$('.prev:visible').click();
				return;
			} 
			
			if(e.keyCode == RIGHT){
				$('.next:visible').click();
				return;
			}

			if(e.keyCode == ESC){
				$('.close').click();
				return;
			}
		}

		$(document).delegate('.media-gallery', 'click', function(e){
			e.preventDefault();
			handlers[$(this).data('type') || 'default'].call(this, $(this).attr('href'));

			$(document).unbind('keyup').bind('keyup', handleNavigation);
		});

		$(document).delegate('.opened-media .close', 'click', function(e){
			e.preventDefault();
			$(document).unbind('keyup');
			$(this).closest('.opened-media').hide(300, function(){
				$(this).remove();
			})
		});

		$(document).delegate('.opened-media .next, .opened-media .prev', 'click', function(e){
			e.preventDefault();

			var step = $(this).is('.prev') ? -1 : 1;

			var $gallery = $('.media-gallery'),
				index = $gallery.index($current) + step;

			$($gallery[index]).trigger('click');
		});
	}

	function photos(){
		$(document).delegate("#new-photo", "change", function(){
			$(this).closest('form').submit();
		});

		var inprogress = false;

		$(document).delegate(".remove-photo", "click", function(e){
			e.preventDefault();

			if(inprogress){ return; }
			inprogress = true;

			var $link = $(this),
				$photo = $link.closest('li');

			$.get('/musico/remover-foto', {id: $link.data('id')}, function(response){
				new lb.message('A foto foi removida',lb.message.INFO);
				$photo.hide(300, function(){
					$photo.remove();
					inprogress = false;
				});
			});
		});
	}

	function videos(){
		$(document).delegate('#add-video-form', 'ajaxcomplete', function(e, response){
			location.reload();
		});

		var inprogress = false;
		$(document).delegate(".remove-video", "click", function(e){
			e.preventDefault();

			if(inprogress){ return; }
			inprogress = true;

			var $link = $(this),
				$photo = $link.closest('li');

			$.get('/musico/remover-video', {id: $link.data('id')}, function(response){
				new lb.message('O vídeo foi removido',lb.message.INFO);
				$photo.hide(300, function(){
					$photo.remove();
					inprogress = false;
				});
			});
		});
	}

	this.init();
	$(this.domLoaded);
})();