lb.customCheckbox = (function($){

	var exports = {},
		defaultSettings = {
			normalClass = 'normal_input',
			cssClass = 'bp_custom_input'
		};

	exports.init = function(settings) {
		_settings = $.extend(defaultSettings, settings);

	}

	function _handleEvents(){
		$(document).bind('loginboxloaded', function() {
			_wrapCheckbox();
			_handleClick();
			_handleEvents();
			_customRadio();
		})
	}

	function _wrapCheckbox(){
		$('input[type=checkbox]').each(function() {
			var $_t = $(this),
				normalClass = _settings.normalClass,
				cssClass = _settings.cssClass;

				if($_t.hasClass(normalClass)){
					return;
				}

				if ($_t.parent().hasClass(cssClass)) {
					return;
				};

				var $_fakeDiv = $('<div class="' + cssClass + '"></div>');

				$_t.wrap($_fakeDiv);

				if ($_t.is('checked')) {
					$_t.parent().addClass('checked');
				};
		})
	}

	function _handleClick(){
		$(document).delegate('.' + _settings.cssClass, 'click', function(){
			var $_t = $(this);
			$_t[$_t.find('input').is(':checked') ? 'addClass' : 'removeClass']('checked');
		}})
	}

	function _customRadio(){
		$(document).ready(function(){
			$('.custom_radio').click(function(){
				$( '.custom_radio').css('background-position', 'left top');
				$(this).css('background-position', 'left bottom');
				$('#custom_gender').val($(this).attr('data-id'));
			})
		})
	}

	return exports;

} (jquery));