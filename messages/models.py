from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from labandas.helpers import EmailSender

class MessageManager(models.Manager):

	def send_message(self, from_user, to, subject, txt):
		message = Message.objects.create(from_user=from_user, to_user=to, text=txt, subject=subject)
		EmailSender.message_received(message)
		return message

	def total_unread_from_musician(self, user):
		return user.messages_received.filter(read_date__isnull=True).count()

	def mark_as_read(self, messages_ids):
		Message.objects.filter(id__in=messages_ids).update(read_date=timezone.now())

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