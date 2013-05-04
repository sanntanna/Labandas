from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MessageManager(models.Manager):

	def send_message(self, from_user, to, subject, message):
		return Message.objects.create(from_user=from_user, to_user=to, text=message, subject=subject)

	def total_unread_from_musician(self, musician):
		return musician.messages_received.count()

	def mark_as_read(self, message):
		message.read_date = timezone.now()
		message.save()

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