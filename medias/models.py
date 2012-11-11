#coding=ISO-8859-1
from django.db import models
from utils import ImageHandler, AmazonS3


class MediaType(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Media(models.Model):
    media = models.CharField(max_length=50)
    media_type = models.ForeignKey(MediaType)
    def __unicode__(self):
        return "%s %d" % (self.media_type.name, self.id)

class MusicianMedia(models.Model):
    BASE_URL_USER_IMAGES = "https://lasbandas.s3.amazonaws.com/u/"
    AVATAR_IMG_NAME = "avatar.png"
    AVATAR_SMALL_IMG_NAME = "avatar-small.png"
    COVER_IMG_NAME = "cover.png"

    AVATAR_TYPE = MediaType.objects.get(name="avatar")
    COVER_PHOTO_TYPE = MediaType.objects.get(name="cover_photo")

    media_list = models.ManyToManyField(Media, null=True, blank=True)

    def avatar():
        def fget(self):
            if not self.media_list.filter(media_type = self.AVATAR_TYPE):
                return None
            return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.musician.id, self.AVATAR_IMG_NAME)

        def fset(self, uploaded_image):
            handler = ImageHandler()
            images = handler.handle_profile_images(uploaded_image)
            
            s3 = AmazonS3()
            s3.upload_file(images['default'], '/u/%d/%s' % (self.musician.id, self.AVATAR_IMG_NAME))
            s3.upload_file(images['small'], '/u/%d/%s' % (self.musician.id, self.AVATAR_SMALL_IMG_NAME))

            if not self.media_list.filter(media_type = self.AVATAR_TYPE):
                self.media_list.add(Media.objects.create(media = "avatar", media_type = self.AVATAR_TYPE))
        return locals()
    avatar = property(**avatar())

    @property
    def avatar_small(self):
        if not self.media_list.filter(media_type = AVATAR):
            return None
        return "%s%d/%S" % (self.BASE_URL_USER_IMAGES, self.musician.id, self.AVATAR_SMALL_IMG_NAME)


    def cover():
        def fget(self):
            if not self.media_list.filter(media_type = self.COVER_PHOTO_TYPE):
                return None
            return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.musician.id, self.COVER_IMG_NAME)

        def fset(self, uploaded_image):
            handler = ImageHandler()
            images = handler.handle_cover_image(uploaded_image)
            
            s3 = AmazonS3()
            s3.upload_file(images['default'], '/u/%d/%s' % (self.musician.id, self.COVER_IMG_NAME))

            if not self.media_list.filter(media_type = self.COVER_PHOTO_TYPE):
                self.media_list.add(Media.objects.create(media = "cover", media_type = self.COVER_PHOTO_TYPE))
        return locals()
    cover = property(**cover())


    def __unicode__(self):
        return "Midia %d" % self.id