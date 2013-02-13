(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupInlineEdition();
		setupCheckUncheckIcons();
		setupSkills();
		setupSolicitations();
		setupBornDate();
		setupSoundCloud();
		musicalStyles();
		bandCreation();
	};
	
	function setupInlineEdition(){

		$(document).delegate('input.post-on-edit, textarea.post-on-edit, select.post-on-edit', 'change', function(e){
			var $elm = $(this);

			var dataField = this.name.split('.'),
				val = this.value;

			var postData = {},
				url = "";

			if(dataField.length == 1){
				postData[dataField[0]] = val;
				url = dataField[0];
			} else {
				postData[dataField[1]] = val;
				url = dataField[0] + '/' + dataField[1];
			}

			if($elm.attr('data-single')){
				postData['single'] = true;
			}

			$.post('/musico/atualizar/' + url, postData);
		});

		function input($elm, type){
			return $('<input type="text" class="post-on-edit" />')
						.attr('name', $elm.attr('data-field'))
						.width($elm.width())
						.val($elm[0].originalContent)
						.bind('blur enterpress', inlineInputBlur);
		}

		function inlineInputBlur(e){
			var $parent = $(this).parent(),
			val = this.value;

			$parent.html(val != "" ? val : $parent[0].originalContent );
		}

		$("#main.can-edit .editable").click(function(){
			var $div = $(this);
			if($div.find('input').length){ return; }

			this.originalContent = $.trim($div.html());
			var ipt = input($div);
			$div.html("").append(ipt);
			ipt[0].focus();

		}).keydown(function(e){
			if(e.keyCode == 13){ 
				$(e.target).trigger('enterpress'); 
			}
		});

		$("form.inline-form input").change(function(){
			$(this).closest('form').trigger('submit');
		});
	}
	
	function setupCheckUncheckIcons(){
		$('.check-icon').each(function(){
			$(this).bind('mouseup', function(){
				var $icon = $(this);
				setTimeout(function(){
					var fn = $icon.find('input:checked').length ? 'addClass' : 'removeClass';
					$icon[fn]('active');
				}, 10)
			}).trigger('mouseup');
		});
	}

	function setupSkills(){
		$(".bar-marker").each(function(){
			var $marker = $(this),
				$barFill = $marker.siblings('.filled'),
				$input = $marker.siblings('.skill-value');

			var margin = 5;
			var barContainerOffset = $marker.parent().offset(),
				maxLeft = $marker.parent().width(),
				rate = 0;

			$marker.mousedown(function(e){
				e.preventDefault();
				
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

			var val = $input.val();
			if(val && val != "" && val.toLowerCase() != "none" && val != "-1"){
				var percentage = parseInt(val) * 10 + '%'
				$barFill.width(percentage);
				$marker.css('left', percentage)
					.closest('li').find('.on-off').attr('checked', 'checked');
			}
		});

		$(".skills input:checkbox").each(function(){
			var $check = $(this),
				$parent = $check.closest('li');

			$check.click(function(e, isTriggered){
				var fn = this.checked ? 'removeClass' : 'addClass';

				$parent[fn]('inactive');
				if(!this.checked && !isTriggered) {
					$parent.find('.skill-value').val('-1').trigger('change');
				}
			}).triggerHandler('click', true);
		});
	}

	function setupSolicitations(){
		$(".accept-solicitation, .decline-solicitation").click(function(e){
			e.preventDefault();
			
			var link = $(this),
				isAccepting = link.hasClass('accept-solicitation'),
				url = "/solicitacao/" + (isAccepting ? 'aceitar' : 'recusar');
			
			$.post(url, {id: link.attr('data-id')}, function(response){
				link.closest('.solicitation').hide(700, function(){
					$(this).remove();
				});
				
				if(isAccepting){
					new lb.message("Agora você está na banda #banda#", lb.message.SUCCESS);
				}
			});
		});
	}

	function setupBornDate(){
		function onchange(e){
			var musicians = $select.find('option[value='+ $select.val() +']').attr('data-artists').split(',');
			var someMusician = musicians[Math.round(Math.random() * musicians.length - 1)];
			$target.html(someMusician == "" ? "--" : someMusician);
			$phrase.show();
		}
		
		var $select = $("#born"),
			$target = $("#same-year-as");
			$phrase = $(".born-celebrity")

		var currentYear = parseInt($("#current-born-year").val());

		if(!isNaN(currentYear)){
			$select.find("option[value=" + currentYear + "]").attr('selected', 'selected');
		}

		$select.change(onchange);

		onchange();
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

		handleLabelAndGetSelecteds();
	}
	
	function bandCreation(){
		console.log("p");
		$(document).delegate("#new-band-form", "ajaxcomplete", function(e, response){
			if(!response.success){ return; }
			location.href = response.band_page_url;
		});
	}

	this.init();
	$(this.domLoaded);
})();