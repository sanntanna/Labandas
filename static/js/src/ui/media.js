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

			$box.find(".prev-media, .next-media").show();

			if(index == 0){
				$box.find(".prev-media").hide();
			} 

			if(index == $gallery.length - 1){
				$box.find(".next-media").hide();
			}
		}

		var handlers = {
			'default': function($link, $last){
				var url = $link.attr('href'),
					legend = $link.attr('title');

				return ['<img src="', url ,'" alt="', legend ,'" />'].join('');
			},

			'video': function($link, $last){
				var url = $link.attr('href'),
					baseUrl = 'http://www.youtube.com/embed/',
					legend = $link.attr('title');

				return ['<iframe width="735" height="550" src="', baseUrl, url, '" frameborder="0" allowfullscreen></iframe>'].join('');
			}
		};

		function handleNavigation(e){
			if(e.keyCode == LEFT){
				$('.prev-media:visible').click();
				return; 
			} 
			
			if(e.keyCode == RIGHT){
				$('.next-media:visible').click();
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

			var $items = $('.media-gallery'),
				whereAppend = Math.min(Math.ceil(parseInt($link.data('pos'), 10) / 4) * 4 - 2, $items.length - 1);

			var url = $link.attr('href'),
				legend = $link.attr('title');

			var $expanded = $('.expanded');

			if($expanded.length){
				$expanded.remove();
			} else {
				$link.closest('ul').addClass('with-zoom');
			}

			$expanded = $(['<li class="expanded">',
								'<div class="hide-zoom close">x</div>',
								'<div class="line">',
									'<div class="fl image">',
										handlers[$link.data('type') || 'default'].apply(this, [$link]),
									'</div>',
									'<div class="fl legend">', legend, '</div>',
								'</div>',
								'<div class="prev-media"><span>&lt;</span></div>',
								'<div class="next-media"><span>&gt;</span></div>',
							'</li>'].join(''));

			$items.eq(whereAppend).parent().after($expanded);

			$('.active').removeClass('active');
			$link.closest('li').addClass('active');
			$current = $link;

			handleNextPrev.call(this, $expanded);

			$('body').animate({'scrollTop': $expanded.offset().top - 50}, 500);

			$(document).unbind('keyup').bind('keyup', handleNavigation);
		});

		$(document).delegate('.expanded .close', 'click', function(e){
			e.preventDefault();
			$(document).unbind('keyup');
			$(this).closest('.expanded').slideUp(300, function(){
				$('.active').removeClass('active');
				$(this).closest('.media-container').removeClass('with-zoom');
				$(this).remove();
			});
		});

		$(document).delegate('.next-media, .prev-media', 'click', function(e){
			e.preventDefault();

			var step = $(this).is('.prev-media') ? -1 : 1;

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