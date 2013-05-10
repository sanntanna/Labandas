lb.facebook = (function(){

	var public = {},
		facebookApi = null;

	public.init = function(){
		load();
	};

	public.login = function(){
		facebookApi.login(function(user){

			var connectData = {
				token: user.accessToken,
				id: user.userID,
				name: 'facebook'
			};

			$.post('/network/connect', connectData, function(response){
				if(response.success){
					location.reload();
				}
			});
		});
	};

	public.friends = function(callback){
		facebookApi.friends(callback);
	}

	function load(){
		facebookApi = new facebook('363555127094643');
		facebookApi.permissionsNeeded('email,user_birthday,user_hometown,publish_stream,create_event');
	}

	return public;

}());