from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from boto.s3.key import Key
from labandas import settings
import Image
import StringIO
import boto
import logging

class AmazonS3(object):
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    
    def __connect_s3(self):
        return boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    
    def __get_bucket(self, conn):
        return conn.get_bucket(settings.BUCKET_NAME)
    
    def upload_file(self, localfile, remotepath):
        conn = self.__connect_s3()
        
        bucket_key = Key(self.__get_bucket(conn))
        bucket_key.key = remotepath
        
        if hasattr(localfile, 'read'):
            bucket_key.set_contents_from_file(localfile)
        else:
            bucket_key.set_contents_from_filename(localfile)
            
        bucket_key.make_public()
        
        return bucket_key.generate_url(1 * 60 * 60 * 24)

class ImageHandler():
    def __resize_image(self, image, size, crop=True):
        factor = 1

        clone = image.copy()

        while clone.size[0]/factor > 2*size[0] and clone.size[1]*2/factor > 2*size[1]:
            factor *=2

        if factor > 1:
            clone.thumbnail((clone.size[0]/factor, clone.size[1]/factor), Image.NEAREST)

        if crop:
            x1 = y1 = 0
            x2, y2 = clone.size
            wRatio = 1.0 * x2/size[0]
            hRatio = 1.0 * y2/size[1]

            if hRatio > wRatio:
                y1 = int(y2/2-size[1]*wRatio/2)
                y2 = int(y2/2+size[1]*wRatio/2)
            else:
                x1 = int(x2/2-size[0]*hRatio/2)
                x2 = int(x2/2+size[0]*hRatio/2)

            clone = clone.crop((x1,y1,x2,y2))

        clone.thumbnail(size, Image.ANTIALIAS)

        file_pointer = StringIO.StringIO()
        clone.save(file_pointer, "png")
        file_pointer.seek(0)

        return file_pointer
    
    def handle_profile_images(self, new_file):
        image = Image.open(new_file)
        return {
            'default': self.__resize_image(image, (100,100)),
            'small': self.__resize_image(image, (40,36))
        }

    def handle_cover_image(self, new_file, generate_small=False):
        image = Image.open(new_file)
        response = {
            'default': self.__resize_image(image, (948,315))
        }

        if generate_small:
            response['small'] = self.__resize_image(image, (744,130))

        return response 


class SoundCloud(object):
    @classmethod
    def validate_url(cls, url):
        validate = URLValidator()
        try:
            validate(url)
            if url.find("soundcloud.com/") == -1:
                raise ValidationError()
        except ValidationError, e:
            raise ValidationError("Url do sound cloud invalida")

        return True
