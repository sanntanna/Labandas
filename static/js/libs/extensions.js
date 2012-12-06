(function(s){

	s.param = function(name, value){
		var paramIndex = this.indexOf('?');
		var url = paramIndex > -1 ? this.substr(0, paramIndex + 1) : this,
			params = paramIndex > -1 ? this.substr(paramIndex + 1) : '';
		
		params = params == "" ? {} : eval("({'" + params.split('&').join("','").split('=').join("':'")  + "'})");

		if(value == undefined) {
			return params[name];
		}

		params[name] = value;
		params = JSON.stringify(params).replace(/{|}|\"|"|\'|'/gi, "")
										.split(',').join('&')
										.split(':').join('=');

		return (url.indexOf('?') > -1 ? url : url + '?') + params;
	}

}(String.prototype));

$(document).delegate('input[type=text],textarea', 'keyup', function(e){
	var elm = this;
	clearTimeout(elm.interval);
	elm.interval = setTimeout(function(){
		$(elm).trigger('textchanged');
	}, 1000);
});