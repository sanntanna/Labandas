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
	}

	return public;

}());