lb.inlineEdit = function(){

	this.init = function(){
		var pathToPost = $('body').data('inline-edit-path'),
			id = $('body').data('id');

		$(document).delegate('input.post-on-edit, textarea.post-on-edit, select.post-on-edit', 'change', function(e){
			var $elm = $(this);

			if($elm.closest('[data-disableautopost]').length){
				return;
			}

			var dataField = this.name.split('.'),
				val = this.value;

			var postData = {},
				url = "";

			if(dataField.length == 1){
				postData[dataField[0]] = val;
				url = dataField[0];
			} else {
				postData[dataField[1]] = val;
				url = dataField[0] + '/' + dataField[1];
			}

			if($elm.attr('data-single')){
				postData['single'] = true;
			}

			if(id){
				url = url.param('id', id);
			}

			$.post(pathToPost + url, postData);
		});

		$(document).delegate("#main.can-edit .editable", 'click', function(){
			var $div = $(this);
			if($div.find('input').length){ return; }

			this.originalContent = $.trim($div.text());
			var ipt = input($div);

			if($div.data('single')){
				ipt.attr('data-single', true);
			}

			$div.html("").append(ipt);
			ipt.focus();

		}).delegate('#main.can-edit .editable', 'keydown', function(e){
			if(e.keyCode == 13){ 
				$(e.target).trigger('enterpress'); 
			}
		});

		$(document).delegate("form.inline-form input", 'change', function(){
			$(this).closest('form').trigger('submit');
		});
	};

	function input($elm, type){
		var value = $elm[0].originalContent;

		if(value == $elm.data('default')){
			value = '';
		}

		return $('<input type="text" class="post-on-edit" />')
					.attr('name', $elm.attr('data-field'))
					.width($elm.width())
					.val(value)
					.bind('blur enterpress', inlineInputBlur);
	}

	function inlineInputBlur(e){
		var $parent = $(this).parent(),
			val = this.value,
			def = $parent.data('default');

		var value = val != "" ? val :  $parent[0].originalContent;

		if(val == '' && def){
			value = '<em>' + def + '</em>';
		}

		$parent.html(value);
	}
}

lb.inlineEdit.globalSetup = function(){
	new lb.inlineEdit().init();
}