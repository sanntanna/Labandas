(function(){
	this.init = function(){};
	
	this.domLoaded = function(){
		setupSubscribeForm();
	};
	
	function setupSubscribeForm(){
		$("#subscribe-form").bind('ajaxcomplete', function(e, response){
			if(response.success){
				location.reload();
				return;
			}
		});
	}
	
	this.init();
	$(this.domLoaded);
})();