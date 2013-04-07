facebook = function(appid){

	var ready = false;

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

	function executeLogin(callback){
		FB.login(function(response) {
			console.log(response);

			callback.call(response);
		}, {scope: 'email,user_birthday,user_hometown,publish_stream,create_event'});
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