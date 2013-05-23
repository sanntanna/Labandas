(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		gallery();
		photos();
		videos();
		legends();
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
			'default': function(url, legend){
				var $photoLarge = $('.expanded'),
					animate = true;

				if($photoLarge.length){
					console.log('remove');
					$photoLarge.remove();
					animate = false;
				}

				$photoLarge = $(['<li class="expanded">',
									'<div class="hide-zoom toggle-button" data-target=".expanded">x</div>',
									legend,
									'<img src="', url ,'" alt="', legend ,'" />',
								'</li>'].join(''));

				if(animate){
					$('.media-container').append($photoLarge.slideDown());
				} else {
					$('.media-container').append($photoLarge);
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
			var $link = $(this);
			handlers[$link.data('type') || 'default'].apply(this, [$link.attr('href'), $link.attr('title')]);

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

	function legends(){
		$(document).delegate('.media-container .post-on-edit', 'blur', function(){
			var $input = $(this);
			var data = {
				'id_media': $input.closest('[data-id]').data('id'),
				'legend': $input.val()
			};

			$.post('/midia/atualizar-legenda', data);
		});
	}

	this.init();
	$(this.domLoaded);
})();