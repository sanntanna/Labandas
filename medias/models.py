#coding=ISO-8859-1
from django.db import models
import os
from utils import ImageHandler, AmazonS3, SoundCloud

class MediaType(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Media(models.Model):
    media = models.CharField(max_length=255)
    legend = models.CharField(max_length=125)
    media_type = models.ForeignKey(MediaType)

    def __unicode__(self):
        return self.media

class MusicianMedia(models.Model):
    BASE_URL_USER_IMAGES = "http://lasbandas.s3.amazonaws.com/u/"
    AVATAR_IMG_NAME = "avatar.png"
    AVATAR_SMALL_IMG_NAME = "avatar-small.png"
    COVER_IMG_NAME = "cover.png"

    media_list = models.ManyToManyField(Media, null=True, blank=True)

    def get_avatar(self):
        if not self.media_list.filter(media_type__name = "avatar"):
            return None
        return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.musician.id, self.AVATAR_IMG_NAME)

    def set_avatar(self, uploaded_image):
        handler = ImageHandler()
        images = handler.handle_profile_images(uploaded_image)
        
        s3 = AmazonS3()
        s3.upload_file(images['default'], '/u/%d/%s' % (self.musician.id, self.AVATAR_IMG_NAME))
        s3.upload_file(images['small'], '/u/%d/%s' % (self.musician.id, self.AVATAR_SMALL_IMG_NAME))

        if not self.media_list.filter(media_type__name = "avatar"):
            self.media_list.add(Media.objects.create(media = "avatar", media_type = self.__type("avatar")))

    avatar = property(get_avatar, set_avatar)

    @property
    def avatar_small(self):
        if not self.media_list.filter(media_type__name = "avatar"):
            return None
        return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.musician.id, self.AVATAR_SMALL_IMG_NAME)


    def get_cover(self):
        if not self.media_list.filter(media_type__name = "cover_photo"):
            return None
        return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.musician.id, self.COVER_IMG_NAME)

    def set_cover(self, uploaded_image):
        handler = ImageHandler()
        images = handler.handle_cover_image(uploaded_image)
        
        s3 = AmazonS3()
        s3.upload_file(images['default'], '/u/%d/%s' % (self.musician.id, self.COVER_IMG_NAME))

        if not self.media_list.filter(media_type__name = "cover_photo"):
            self.media_list.add(Media.objects.create(media = "cover", media_type = self.__type("cover_photo")))

    cover = property(get_cover, set_cover)


    def get_sound_cloud(self):
        objs = self.media_list.filter(media_type__name = "sound_cloud")
        return None if len(objs) == 0 else objs[0]
    
    def set_sound_cloud(self, value):
        
        if not SoundCloud.validate_url(value):
            return

        sound_cloud = self.get_sound_cloud()

        if sound_cloud is None:
            self.media_list.add(Media.objects.create(media = value, media_type = self.__type("sound_cloud")))
            return

        sound_cloud.media = value
        sound_cloud.save()

    sound_cloud = property(get_sound_cloud, set_sound_cloud)

    @property
    def photos(self):
        return self.media_list.filter(media_type__name = "musician_photo")

    def add_photo(self, image, legend=None):
        filename, ext = os.path.splitext(image.name)
        
        photo = Media.objects.create(media=image.name, legend=legend, media_type=self.__type("photo"))
        self.media_list.add(photo)

        AmazonS3().upload_file(image, '/u/%d/photo/%d%s' % (self.musician.id, photo.id, ext))


    def __type(self, name):
        return MediaType.objects.get(name=name)

    def __unicode__(self):
        return "Midia %s" % self.id


class BandMedia(models.Model):
    BASE_URL_USER_IMAGES = "http://lasbandas.s3.amazonaws.com/banda/"
    COVER_IMG_NAME = "cover.png"
    COVER_SMALL_IMG_NAME = "cover-small.png"

    media_list = models.ManyToManyField(Media, null=True, blank=True)

    def get_cover(self):
        if not self.media_list.filter(media_type__name = "cover_photo"):
            return None
        return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.band.id, self.COVER_IMG_NAME)

    @property
    def cover_small(self):
        if not self.media_list.filter(media_type__name = "cover_photo"):
            return None
        return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.band.id, self.COVER_SMALL_IMG_NAME)

    def set_cover(self, uploaded_image):
        handler = ImageHandler()
        images = handler.handle_cover_image(uploaded_image, True)
        
        s3 = AmazonS3()
        s3.upload_file(images['default'], '/banda/%d/%s' % (self.band.id, self.COVER_IMG_NAME))
        s3.upload_file(images['small'], '/banda/%d/%s' % (self.band.id, self.COVER_SMALL_IMG_NAME))

        if not self.media_list.filter(media_type__name = "cover_photo"):
            self.media_list.add(Media.objects.create(media = "cover", media_type = self.__type("cover_photo")))

    cover = property(get_cover, set_cover)

    def get_sound_cloud(self):
        objs = self.media_list.filter(media_type__name = "sound_cloud")
        return None if len(objs) == 0 else objs[0]
    
    def set_sound_cloud(self, value):
        
        if not SoundCloud.validate_url(value):
            return
            
        sound_cloud = self.get_sound_cloud()

        if sound_cloud is None:
            self.media_list.add(Media.objects.create(media = value, media_type = self.__type("sound_cloud")))
            return

        sound_cloud.media = value
        sound_cloud.save()

    sound_cloud = property(get_sound_cloud, set_sound_cloud)

    def __type(self, name):
        return MediaType.objects.get(name=name)

    def __unicode__(self):
        return "Midia %s" % self.id