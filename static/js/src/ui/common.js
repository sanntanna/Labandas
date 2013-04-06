(function(){
	
	this.init = function(){
		setupAjax();
		setupLogin();
		setupCollapseButtons();
		handleActiveMenus();
		setupLightboxes();
		setupInlineEdit();
		setupSoundCloudPlayers();
		setupPushState();
	};
	
	this.domLoaded = function(){
		new lb.formAjax().globalInit();
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
		$('.toggle-button').each(function(){
			var $link = $(this);

			this.targetElement = $($link.data('target'));
			this.noncollapsedlabel = $link.data('noncollapsedlabel');
			this.collapsedlabel = $link.data('collapsedlabel');

			this.innerHTML = this.targetElement.hasClass(collapsedClass) ? this.collapsedlabel : this.noncollapsedlabel;

			$link.click(function(e){
				e.preventDefault();
				this.innerHTML = this.targetElement.is(':visible') ? this.collapsedlabel : this.noncollapsedlabel;
				this.targetElement.slideToggle();
			});
		});
	}

	function handleActiveMenus(){
		$('ul.markable').each(function(){
			var $links = $(this).find('a');
			$links.each(function(){
				var $link = $(this);

				if(location.href.indexOf(this.href) > -1){
					$link.addClass('active');
				}

				$link.click(function(){
					$links.filter('.active').removeClass('active');
					$link.addClass('active');
				});
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

		$('a.no-refresh').click(function(e){
			e.preventDefault();
			var url = this.href;

			$.get(url.param('partial', true), function(response){
				$("#no-refresh-content").html(response);
				history.pushState({html: response}, null, url);
			});
		});

		window.onpopstate = function(event){
			if(!event.state){ return; }
			$("#no-refresh-content").html(event.state.html);
		}
	}

	this.init();
	$(this.domLoaded);
	
}());