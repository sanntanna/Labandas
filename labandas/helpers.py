from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

class EmailSender(object):

	@classmethod
	def add_in_band(cls, solicitation):
		subject = '%s, %s disse que voce toca na banda %s' % ( solicitation.to_musician.name(), solicitation.from_musician.name(), solicitation.band.name)
		body = get_template('emails/solicitation-received.html')
		
		c = Context({'solicitation': solicitation})

		send_mail(subject, body.render(c), settings.LB_DEFAULT_SENDER, [solicitation.to_musician.user.email])

	@classmethod
	def announcement_reply(cls, solicitation, announcement):
		subject = '%s se candidatou para a banda %s' % ( solicitation.from_musician.name(), solicitation.band.name)
		body = get_template('emails/announcement-reply.html')

		c = Context({'solicitation': solicitation, 'announcement': announcement})

		send_mail(subject, body.render(c), settings.LB_DEFAULT_SENDER, [solicitation.to_musician.user.email])

	@classmethod
	def message_received(cls, message):
		subject = '%s, %s te enviou uma mensagem.' % ( message.to_user.get_full_name(), message.from_user.get_full_name())
		body = get_template('emails/message-received.html')

		send_mail(subject, body.render(Context({'message': message})), settings.LB_DEFAULT_SENDER, [message.to_user.email])