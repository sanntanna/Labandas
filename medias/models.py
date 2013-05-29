#coding=ISO-8859-1
from django.db import models
import os
import urlparse
from utils import ImageHandler, AmazonS3, SoundCloud, VideoValidator

S3_DOMAIN = "http://lasbandas.s3.amazonaws.com"

class MediaType(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Media(models.Model):
    media = models.CharField(max_length=255)
    legend = models.CharField(max_length=125, null=True, blank=True)
    media_type = models.ForeignKey(MediaType)

    def __unicode__(self):
        return self.media

    class Meta:
        ordering = ['-id']

class MusicianMedia(models.Model):
    BASE_URL_USER_IMAGES = "%s/u/" % S3_DOMAIN
    AVATAR_IMG_NAME = "avatar.png"
    AVATAR_SMALL_IMG_NAME = "avatar-small.png"
    COVER_IMG_NAME = "cover.png"

    media_list = models.ManyToManyField(Media, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        instance = super(MusicianMedia, self).__init__(*args, **kwargs)

        self.__has_avatar = self.media_list.filter(media_type__name = "avatar").count() > 0
        self.__has_cover = self.media_list.filter(media_type__name = "cover_photo").count() > 0

        return instance

    def get_avatar(self):
        if not self.__has_avatar:
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
        if not self.__has_avatar:
            return None
        return "%s%d/%s" % (self.BASE_URL_USER_IMAGES, self.musician.id, self.AVATAR_SMALL_IMG_NAME)


    def get_cover(self):
        if not self.__has_cover:
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
        photos = self.media_list.filter(media_type__name = "photo").all()

        return [{
            'thumb': '%s%s' % (S3_DOMAIN, p.media % (self.musician.id, str(p.id) + '-thumb')),
            'large': '%s%s' % (S3_DOMAIN, p.media % (self.musician.id, p.id)),
            'id': p.id,
            'legend': p.legend
        } for p in photos]

    def add_photo(self, image, legend=None):
        default_filename = '/u/%s/photo/%s%s'
        filename, ext = os.path.splitext(image.name)
        
        photo = Media.objects.create(media=default_filename % ('%s', '%s', ext), legend=legend, media_type=self.__type("photo"))
        self.media_list.add(photo)

        thumb, normal = ImageHandler().handle_photo_album(image)    
        s3 = AmazonS3()
        s3.upload_file(thumb, default_filename % (self.musician.id, str(photo.id) + '-thumb', ext))
        s3.upload_file(normal, default_filename % (self.musician.id, photo.id, ext))


    def remove_photo(self, photo_id):
        photo = Media.objects.get(id=photo_id)
        
        self.media_list.remove(photo)
        photo.delete()

        s3 = AmazonS3()
        thumb_path = photo.media % (self.musician.id, str(photo_id) + '-thumb')
        large_path = photo.media % (self.musician.id, photo_id)
        
        s3.delete_file(thumb_path)
        s3.delete_file(large_path)


    @property
    def videos(self):
        return self.media_list.filter(media_type__name = "video").all()

    def add_video(self, video_url, legend=None):
        if not VideoValidator.validate_url(video_url):
            return

        url_data = urlparse.urlparse(video_url)
        query = urlparse.parse_qs(url_data.query)
        video = query["v"][0]

        video = Media.objects.create(media=video, legend=legend, media_type=self.__type("video"))
        self.media_list.add(video)

    def remove_video(self, video_id):
        video = Media.objects.get(id=video_id)
        
        self.media_list.remove(video)
        video.delete()

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

    @property
    def photos(self):
        photos = self.media_list.filter(media_type__name = "photo").all()

        return [{
            'thumb': '%s%s' % (S3_DOMAIN, p.media % (self.band.id, str(p.id) + '-thumb')),
            'large': '%s%s' % (S3_DOMAIN, p.media % (self.band.id, p.id)),
            'id': p.id,
            'legend': p.legend
        } for p in photos]

    def add_photo(self, image, legend=None):
        default_filename = '/b/%s/photo/%s%s'
        filename, ext = os.path.splitext(image.name)
        
        photo = Media.objects.create(media=default_filename % ('%s', '%s', ext), legend=legend, media_type=self.__type("photo"))
        self.media_list.add(photo)

        thumb, normal = ImageHandler().handle_photo_album(image)    
        s3 = AmazonS3()
        s3.upload_file(thumb, default_filename % (self.band.id, str(photo.id) + '-thumb', ext))
        s3.upload_file(normal, default_filename % (self.band.id, photo.id, ext))


    def remove_photo(self, photo_id):
        photo = Media.objects.get(id=photo_id)
            
        self.media_list.remove(photo)
        photo.delete()

        s3 = AmazonS3()
        thumb_path = photo.media % (self.band.id, str(photo_id) + '-thumb')
        large_path = photo.media % (self.band.id, photo_id)
        
        s3.delete_file(thumb_path)
        s3.delete_file(large_path)

    @property
    def videos(self):
        return self.media_list.filter(media_type__name = "video").all()

    def add_video(self, video_url, legend=None):
        if not VideoValidator.validate_url(video_url):
            return

        url_data = urlparse.urlparse(video_url)
        query = urlparse.parse_qs(url_data.query)
        video = query["v"][0]

        video = Media.objects.create(media=video, legend=legend, media_type=self.__type("video"))
        self.media_list.add(video)

    def remove_video(self, video_id):
        video = Media.objects.get(id=video_id)
        
        self.media_list.remove(video)
        video.delete()

    def __type(self, name):
        return MediaType.objects.get(name=name)

    def __unicode__(self):
        return "Midia %s" % self.id