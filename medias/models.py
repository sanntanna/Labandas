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
    BASE_URL_USER_IMAGES = "http://lasbandas.s3.amazonaws.com/u/"
    AVATAR_IMG_NAME = "avatar.png"
    AVATAR_SMALL_IMG_NAME = "avatar-small.png"
    COVER_IMG_NAME = "cover.png"

    __avatar_type = None
    __cover_photo_type = None

    @property
    def AVATAR_TYPE(self):
        if self.__avatar_type is None:
            self.__avatar_type = MediaType.objects.get(name="avatar")
        return self.__avatar_type

    @property
    def COVER_PHOTO_TYPE(self):
        if self.__cover_photo_type is None:
            self.__cover_photo_type = MediaType.objects.get(name="cover_photo")
        return self.__cover_photo_type

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
        if not self.media_list.filter(media_type = self.AVATAR_TYPE):
            return None
        return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.musician.id, self.AVATAR_SMALL_IMG_NAME)


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