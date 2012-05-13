from django.db import models

class MediaType(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Media(models.Model):
    media = models.CharField(max_length=50)
    mediaType = models.ForeignKey(MediaType)
    def __unicode__(self):
        return self.mediaType.name + " " + self.id