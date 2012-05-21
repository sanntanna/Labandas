(function(){
	this.init = function(){};
	this.domLoaded = function(){
		setupForm();
	};
	
	function setupForm(){
		$("#edit-band-form").bind('ajaxcomplete', function(e, response){
			if(response.success){
				location.href = "/";
			}
		});
	}
	
	this.init();
	$(this.domLoaded);
}());