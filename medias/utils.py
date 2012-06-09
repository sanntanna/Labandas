from boto.s3.key import Key
from labandas import settings
import boto
import logging

class AmazonS3(object):
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    
    def _connect_s3_(self):
        return boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    
    def _get_bucket_(self, conn):
        return conn.get_bucket(settings.BUCKET_NAME)
    
    def upload_file(self, localfile, remotepath):
        conn = self._connect_s3_()
        
        bucket_key = Key(self._get_bucket_(conn))
        bucket_key.key = remotepath
        bucket_key.set_contents_from_filename(localfile)

        bucket_key.make_public()
        
        return bucket_key.generate_url(1 * 60 * 60 * 24)
