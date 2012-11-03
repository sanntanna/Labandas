(function(){
	this.init = function(){};
	this.domLoaded = function(){
		setupForm();
	};
	
	function setupForm(){
		$("#lp-form").bind('ajaxcomplete', function(e, response){
			if(response.success){
				$(this).fadeOut(300, function(){
					$("#success-message").fadeIn();
				});
			}
		});
	}
	
	this.init();
	$(this.domLoaded);
}());