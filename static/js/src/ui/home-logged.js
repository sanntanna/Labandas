(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSkills();
		setupBornDate();
		setupSoundCloud();
		musicalStyles();
		bandCreation();
		photoAlbum();
	};
	
	function setupSkills(){
		$(document).delegate('.bar-marker', 'mousedown', function(e){
			e.preventDefault();
			var $marker = $(this),
				$barFill = $marker.siblings('.filled'),
				$input = $marker.siblings('.skill-value');

			var margin = 5;
			var barContainerOffset = $marker.parent().offset(),
				maxLeft = $marker.parent().width(),
				rate = 0;

			$(document).mousemove(function(e){
				var left = e.clientX - barContainerOffset.left;
				left = Math.min(Math.max(left, margin), maxLeft);

				var proportion = left / maxLeft;
				rate = Math.round(proportion * 10);

				$marker.css('left', left);
				$barFill.width(Math.round(proportion * 100) + '%');
			});

			$(document).mouseup(function(){
				$(document).unbind('mousemove mouseup');
				$input.val(rate).trigger('change');
			});
		});

		$(document).delegate('.skills input:checkbox', 'click', function(e, isTriggered){
			var $check = $(this),
				$parent = $check.closest('li');

			var fn = this.checked ? 'removeClass' : 'addClass',
				$input = $parent.find('.skill-value');

			$parent[fn]('inactive');

			if(isTriggered){ return; }
			
			$input.val(this.checked ? 5 : -1).trigger('change');
		});

		$(window).bind('popstate pushstate', function(){
			$(".skills.editable li").each(function(){
				var $skill = $(this),
					$check = $skill.find('input:checkbox'),
					$ipt = $skill.find('input.skill-value'),
					value = parseInt($ipt.val());

				if(isNaN(value) || value < 0 ){
					$skill.addClass('inactive');
					return;
				}

				$check.attr('checked', true);

				$skill.find('.filled').width((value * 10 )+ '%');
				$skill.find('.bar-marker').css('left', (value * 10 )+ '%')
			});
		});
	}

	function setupBornDate(){
		function onchange(e){
			var artists = $select.find('option[value='+ $select.val() +']').attr('data-artists');

			if(!artists){ return; }

			var musicians = artists.split(','),
				someMusician = musicians[Math.round(Math.random() * musicians.length - 1)];
			$target.html(someMusician == "" ? "--" : someMusician);
			$phrase.show();
		}
		
		var $select = null,
			$target = null,
			$phrase = null;

		$(document).delegate("#born", 'change', onchange);

		$(window).bind('popstate', function(){
			$select = $("#born");
			$target = $("#same-year-as");
			$phrase = $(".born-celebrity");

			var currentYear = parseInt($("#current-born-year").val());

			if(!isNaN(currentYear)){
				$select.find("option[value=" + currentYear + "]").attr('selected', 'selected');
			}
			onchange();
		});
	}

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

	function musicalStyles(){
		function handleLabelAndGetSelecteds(){
			var $selectedStyles = $('input[name=musical_styles]:checked'),
				$link = $("#edit-musical-styles-button");

			var textAttr = $selectedStyles.length > 0 ? "withselection" : "withoutselection";
			$link.text( $link.data(textAttr) );

			return $selectedStyles;
		}

		$(document).bind('lightboxclosed', function(e, lightboxInstance){
			if(lightboxInstance.id != "#lb-lightbox-musical-styles"){
				return;
			}

			var $selecteds = handleLabelAndGetSelecteds();
			var content = $selecteds.map(function(i){
				return $(this).closest('label').text().trim();
			}).get().join(', ');

			$("#selected-musical-styles").text(content);
		});

		$(window).bind('popstate pushstate', function(e){
			handleLabelAndGetSelecteds();
		});
	}
	
	function bandCreation(){
		$(document).delegate('a.next', 'click', function(e){
			e.preventDefault();
			$('.name-band').hide();
			$('.musical-style').fadeIn();
		});

		$(document).delegate('a.continue', 'click', function(e){
			e.preventDefault();
			$('.musical-style').hide();
			$('.musician-info').fadeIn();
		});

		$(document).delegate("#new-band-form", "ajaxcomplete", function(e, response){
			if(!response.success){ return; }
			location.href = response.band_page_url;
		});
	}

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