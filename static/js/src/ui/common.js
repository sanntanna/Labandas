(function(){
	
	this.init = function(){
		setupAjax();
		setupLogin();
		setupCollapseButtons();
		setupCheckUncheckIcons();
		handleActiveMenus();
		setupLightboxes();
		setupInlineEdit();
		setupSoundCloudPlayers();
		setupPushState();
		baloonNotifications();
		initCodaSlider();
	};
	
	this.domLoaded = function(){
		new lb.formAjax().globalInit();
		initFacebook();

		//TODO: ver uma solução melhor para o trigger inicial do popstate.
		if(!$.browser.webkit){
			$(window).load(function(){
				$(window).trigger('popstate');
			});
		}
	};
	
	function setupAjax(){
		jQuery(document).ajaxSend(function(event, xhr, settings) {
		    function getCookie(name) {
		        var cookieValue = null;
		        if (document.cookie && document.cookie != '') {
		            var cookies = document.cookie.split(';');
		            for (var i = 0; i < cookies.length; i++) {
		                var cookie = jQuery.trim(cookies[i]);
		                if (cookie.substring(0, name.length + 1) == (name + '=')) {
		                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                    break;
		                }
		            }
		        }
		        return cookieValue;
		    }
		    function sameOrigin(url) {
		        var host = document.location.host;
		        var protocol = document.location.protocol;
		        var sr_origin = '//' + host;
		        var origin = protocol + sr_origin;
		        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		            !(/^(\/\/|http:|https:).*/.test(url));
		    }
		    function safeMethod(method) {
		        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		    }
	
		    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
		        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		    }
		});
	}
	
	function setupLogin(){
		$(document).delegate('#lb-form-login', 'ajaxcomplete', function(e, data){
			if(data.success) {
				location.reload();
			}
		});

		$(document).delegate("#subscribe-form", "ajaxcomplete", function(e, data){
			if(data.success) {
				location.reload();
			}
		});
	}

	function setupCollapseButtons(){
		var collapsedClass = 'hidden';

		$(document).delegate('.toggle-button', 'click', function(e){
			e.preventDefault();
			var $link = $(this),
				$target = $($link.data('target'));

			this.innerHTML = $target.is(':visible') ? $link.data('collapsedlabel') : $link.data('noncollapsedlabel');
			$target.slideToggle();
		});

		$(window).bind('popstate pushstate', function(){
			$('.toggle-button').each(function(){
				var $link = $(this),
					$target = $($link.data('target'));
				
				$link.text($target.is(':visible') ? $link.data('noncollapsedlabel') : $link.data('collapsedlabel'));
			});
		});

	}

	function setupCheckUncheckIcons(){
		$(document).delegate('.check-icon', 'mouseup', function(){
			var $icon = $(this);
			setTimeout(function(){
				var fn = $icon.find('input:checked').length ? 'addClass' : 'removeClass';
				$icon[fn]('active');
			}, 10)
		});

		$(window).bind('popstate pushstate', function(){
			$('.check-icon').trigger('mouseup');
		});
	}

	function handleActiveMenus(){
		$('ul.markable').each(function(){
			var $links = $(this).find('a');

			$links.each(function(){
				var $link = $(this);

				var ex = new RegExp(this.href + '$');

				if(location.href.match(ex)){
					$link.addClass('active');
				}

				$link.click(function(){
					$links.filter('.active').removeClass('active');
					$link.addClass('active');
				});
			});

			$(window).bind('popstate pushstate', function(e, url){
				var $link = $links.filter('[href$="' + url + '"]');
				if(!$link.length){ return; }

				$links.filter('.active').removeClass('active');
				$link.addClass('active');
			});
		});
	}
	
	function setupLightboxes(){
		$(document).delegate("a.lightbox", "click", function(e){
			e.preventDefault();
			new lb.lightbox($(this).attr('href'));
		});
	}

	function setupInlineEdit(){
		lb.inlineEdit.globalSetup();
	}

	function setupSoundCloudPlayers(){
		lb.soundcloud.globalInit();
	}

	function setupPushState(){
		if(!Modernizr.history){
			return;
		}

		var $container = $("#no-refresh-content"),
			initialContent = $container.html();

		if(!$container.length) {return;}

		$(document).delegate('a.no-refresh', 'click', function(e){
			e.preventDefault();
			var url = this.href,
				link = this;

			$.get(url.param('partial', true), function(response){
			    var width = parseInt($('#no-refresh-content').css('width'));
		        var transfer = $('<div class="transfer"></div>').css({ 'width': (2 * width) + 'px' });
		        var current = $('<div class="current"></div>').css({ 'width': width + 'px', 'left': '0', 'float': 'left' }).html($('#no-refresh-content').html());
		        var next = $('<div class="next"></div>').css({ 'width': width + 'px', 'left': width + 'px', 'float': 'left' }).html(response);
		        
		        transfer.append(current).append(next);
		        
		        $('#no-refresh-content').html('').append(transfer);
		        transfer.animate({ 'margin-left': '-' + width + 'px' }, 300, function () {
		            $container.html(response);
					history.pushState({html: response, location: $(link).attr('href')}, null, url);
					$(window).trigger('pushstate');
		        });
		   
			});
		});
		var isPoped = false;
		$(window).bind('popstate', function(event){
			if(!isPoped){
				isPoped = true;
				return;
			}

			if(!event.state){ 
				$container.html(initialContent);
			} else {
				$container.html(event.state.html);
			}
		});
	}

	function baloonNotifications(){
		var boxMessages = $('.messages');
			boxSolicitations = $('.solicitations');
			messages = $('.nav-messages');
			invitations = $('.invitations');


	        $(document).delegate('.notification', 'click', function(e){
                    e.preventDefault();
                    $("#slider-notification").fadeIn();    
     
                $(document).delegate('.nav-messages', 'click', function(e){
					boxSolicitations.hide();
					boxMessages.fadeIn();
					messages.addClass('active');
					invitations.removeClass('active');
				});

				$(document).delegate('.invitations', 'click', function(e){
					boxMessages.hide();
					boxSolicitations.fadeIn();
					invitations.addClass('active');
					messages.removeClass('active');
				});

				$(document).delegate('.send-msg', 'click', function(e){
                    e.preventDefault();
                    $("#slider-notification").fadeOut();  
 				});

 // 				$(document).delegate('body', 'click', function(e){
 //                           $("#slider-notification").fadeOut();
 //                           $(document).unbind('click');
 //                 });
             });
	}

	function initCodaSlider(){
		$('#slider-id').codaSlider();
	}

	function initFacebook(){
		lb.facebook.init();
		
		$(document).delegate('.fb-login', 'click', function(e){
			e.preventDefault();
			lb.facebook.login();
		});
	}

	this.init();
	$(this.domLoaded);
	
}());