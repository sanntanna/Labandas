(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		photoAlbum();
	};

	function photoAlbum(){
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

			var $current = null;
			$(document).delegate('.photo-gallery', 'click', function(e){
				e.preventDefault();

				$current = $(this);

				var $photoLarge = $('#photo-large');

				if(!$photoLarge.length){
					$photoLarge = $(['<div id="photo-large">',
										'<span class="close">x</span>',
										'<span class="prev">&lt;</span>',
										'<img src="' + this.href + '" />',
										'<span class="next">&gt;</span>',
								   '</div>'].join(''));

					$('body').append($photoLarge);
				} else {
					$photoLarge.find('img').attr('src', this.href);
				}

				var $gallery = $('.photo-gallery'),
					index = $gallery.index($(this));

				$photoLarge.find(".prev, .next").show();

				if(index == 0){
					$photoLarge.find(".prev").hide();
				} else if(index == $gallery.length - 1){
					$photoLarge.find(".next").hide();
				}
			});

			$(document).delegate('#photo-large .close', 'click', function(e){
				e.preventDefault();
				$(this).closest('#photo-large').hide(300, function(){
					$(this).remove();
				})
			});

			$(document).delegate('#photo-large .next, #photo-large .prev', 'click', function(e){
				e.preventDefault();

				var step = $(this).is('.prev') ? -1 : 1;

				var $gallery = $('.photo-gallery'),
					index = $gallery.index($current) + step;

				$($gallery[index]).trigger('click');
			});
		}

	this.init();
	$(this.domLoaded);
})();