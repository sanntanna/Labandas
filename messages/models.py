from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone

class MessageManager(models.Manager):

	def send_message(self, from_user, to, subject, message):
		message = Message.objects.create(from_user=from_user, to_user=to, text=message, subject=subject)
		self.__send_email(message)
		return message

	def total_unread_from_musician(self, user):
		return user.messages_received.filter(read_date__isnull=True).count()

	def mark_as_read(self, messages_ids):
		Message.objects.filter(id__in=messages_ids).update(read_date=timezone.now())

	def __send_email(self, m):
		subject = '%s, %s te enviou uma mensagem.' % ( m.to_user.get_full_name(), m.from_user.get_full_name())
		body = get_template('emails/message-received.html')

		send_mail(subject, body.render(Context({'message': m})), settings.LB_DEFAULT_SENDER, [m.to_user.email])

class Message(models.Model):
	from_user = models.ForeignKey(User, related_name='messages_sent')
	to_user = models.ForeignKey(User, related_name='messages_received')
	text = models.CharField(max_length=1000)
	subject = models.CharField(max_length=200, null=True, blank=True)

	sent_date = models.DateTimeField()
	read_date = models.DateTimeField(null=True, blank=True)

	active = models.BooleanField(default=True)

	objects = MessageManager()

	def save(self, *args, **kwargs):
		self.sent_date = timezone.now()

		super(Message, self).save(*args, **kwargs)

	class Meta:
		ordering = ['-id']