facebook = function(appid){

	var ready = false,
		permissions ={};

	function init(){
		prepare();
	};

	this.login = function(callback){
		if(ready){
			executeLogin(callback);
			return;
		}
		$(document).bind('fb-loaded', function(){
			executeLogin(callback);
		});
	};

	this.permissionsNeeded = function(perms){
		permissions = {scope: perms};
	};

	function executeLogin(callback){
		FB.getLoginStatus(function(response){
			if(response.status == 'connected'){
				callback.call(null, response);
				return;
			}

			FB.login(function(loginResponse) {
				callback.call(null, loginResponse);
			}, permissions);
		});
	}

	function prepare(){
		if($("#fb-root").length){ return; }
		$(document.body).append('<div id="fb-root"></div>');

		$.getScript('http://connect.facebook.net/pt_BR/all.js', function(){
			ready = true;
			FB.init({
			  appId  : appid,
			  status : true, 
			  cookie : true, 
			  xfbml  : false
			});

			$(document).trigger('fb-loaded');
		});
	}

	init();
};