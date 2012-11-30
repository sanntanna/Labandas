(function(s){

	s.param = function(name, value){
		var url = this.substr(0, this.indexOf('?') + 1),
			params = this.indexOf('?') > -1 ? this.substr(this.indexOf('?') + 1) : '';
		
		if(params == "" || !params)  { return undefined; }

		params = eval("({'" + params.split('&').join("','").split('=').join("':'")  + "'})");

		if(value == undefined) {
			return params[name];
		}

		params[name] = value;
		params = JSON.stringify(params).replace(/{|}|\"|"|\'|'/gi, "")
										.split(',').join('&')
										.split(':').join('=');

		return url + params;
	}

}(String.prototype));