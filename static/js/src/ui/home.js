(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSubscribeForm();
		parallax();
	};
	
	function setupSubscribeForm(){
		$("#subscribe-form").bind('ajaxcomplete', function(e, response){
			if(response.success){
				location.reload();
				return;
			}
		});
	}

	function parallax(){
		$('div.parallax').each(function(){
		var $obj = $(this);

			$(window).scroll(function() {
				var yPos = -($(window).scrollTop() / $obj.data('speed')); 

				var bgpos = '1250px '+ yPos + 'px';

				$obj.css('background-position', bgpos );

			}); 
		});	
	}
	
	this.init();
	$(this.domLoaded);
})();