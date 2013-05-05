(function(){
	var boxMessages = $('.messages');
		boxSolicitations = $('.solicitations');
		messages = $('.nav-messages');
		invitations = $('.invitations');


	var markAsReadTimeout = 0;

	function countNotifications(){
		$.get('/total-notificacoes', function(response){
			var total = response.totals.messages + response.totals.solicitations;
			
			$("#total-notifications").html(total)[total > 0 ? 'fadeIn' : 'fadeOut']();

			$("#total-messages").html(response.totals.messages).data('total', response.totals.messages);
			$("#total-solicitations").html(response.totals.solicitations).data('total', response.totals.solicitations);
		});
	}

	function markMessagesAsRead(){
		if( $("#total-messages").data('total') <= 0 ){ return; }
		
		var ids = [],
			$unreadeds = $('.messages li.unreaded');

		$unreadeds.each(function(){
			ids.push('ids=' + $(this).data('messageid'));
		});

		$.get('/mensagem/marcar-como-lida', ids.join('&'), function(){
			setTimeout(function(){
				countNotifications();
				$unreadeds.removeClass('unreaded').addClass('readed');
			}, 1000);
		});
	}

	function printNotifications(response){
		if(!response.solicitations || response.solicitations.length == 0){
			boxSolicitations.html('<li class="default-message">Nenhuma notificação</li>');
			return;
		}

		var html = response.solicitations.map(function(n){
			return ['<li>',
						'<div class="info-user">',
						'	<div class="image"><img src="', n.from_avatar,'" /></div>',
						'	<div class="name">', n.from,'</div>',
						'</div>',
						'<div>',
						'	<div class="waiting">',
						'		<p><a href="', n.from_url,'" target="_blank"><strong>', n.from ,'</strong>',
						'		</a> te adicionou como membro ', n.instruments, ' da banda  <strong>', n.band, '</strong>.</p>',
						'	</div>',
						'	<div class="line">',
						'		<a href="aceitar" class="btn respond-invite" data-id="', n.id,'">Aceitar</a>',
						'		<a href="recusar" class="btn red respond-invite" data-id="', n.id,'">Não agora</a>',
						'		<a href="#send-message" data-toid="', n.from_id,'" class="btn send-msg">Enviar mensagem</a>',
						'	</div>',
						'</div>',
					'</li>'].join('');
		}).join('');

		boxSolicitations.html(html);
	}

	function printMessages(response){
		if(!response.messages || response.messages.length == 0){
			boxMessages.html('<li class="default-message">Nenhuma mensagem</li>');
		}

		var html = response.messages.map(function(m){
			return ['<li data-messageid="', m.id ,'" class="', m.is_read ? 'readed': 'unreaded','">',
					'<div class="info-user">',
						'	<div class="image"><img src="', m.from_avatar,'" /></div>',
						'	<div class="name">', m.from,'</div>',
					'</div>',
					'<div>',
					'	<div class="waiting">', m.message,'</div>',
					'</div>',
					'	<a href="#respond-message" data-toid="', m.from_id,'" class="btn send-msg">Responder</a>',
					'	<a href="#respond-message" data-toid="', m.from_id,'" class="btn">Ler mensagem completa</a>',
					'</li>'].join('');
		}).join('');

		boxMessages.html(html);

		markAsReadTimeout = setTimeout(markMessagesAsRead, 4000);
	}

	var isLoaded = false;
    $(document).delegate('.notification', 'click', function(e){
		e.preventDefault();
		$("#slider-notification").fadeToggle('fast', function(){
			if($(this).is(':visible')){ return; }
			clearTimeout(markAsReadTimeout);
		});

		if(!isLoaded){
			isLoaded = true;
			$('.invitations').trigger('click');
		}
	});

	$(document).delegate('body', 'click', function(e){
		if($(e.target).closest('.prevent-hide').length) {
			return;
		}

		$("#slider-notification").fadeOut('fast');
		clearTimeout(markAsReadTimeout);
	});

	 $(document).delegate('.nav-messages', 'click', function(e){
		e.preventDefault();

		boxSolicitations.hide();
		boxMessages.fadeIn();
		messages.addClass('active');
		invitations.removeClass('active');
		boxMessages.html('<li class="default-message">Aguarde...</li>');
		$.get('/mensagem/listar', printMessages);
	});

	$(document).delegate('.invitations', 'click', function(e){
		e.preventDefault();

		boxMessages.hide();
		boxSolicitations.fadeIn();
		invitations.addClass('active');
		messages.removeClass('active');
		boxSolicitations.html('<li class="default-message">Aguarde...</li>');
		$.get('/solicitacao/listar', printNotifications);
	});


	$(document).delegate('.send-msg', 'click', function(e){
		e.preventDefault();
		$("#slider-notification").fadeOut();  
	});

	setTimeout(countNotifications, 1500);
	setInterval(countNotifications, 60 * 1000);
}());