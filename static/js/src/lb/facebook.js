lb.facebook = (function(){

	var public = {},
		facebookApi = null;

	public.init = function(){
		load();
	};

	public.login = function(){
		facebookApi.login(function(user){
			console.log('lb class');
			console.log(user);
		});
	};

	function load(){
		facebookApi = new facebook('363555127094643');
		facebookApi.permissionsNeeded('email,user_birthday,user_hometown,publish_stream,create_event');
	}

	return public;

}());