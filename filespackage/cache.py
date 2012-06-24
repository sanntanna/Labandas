from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor
import os.path

def get_hexdigest(plaintext, length=None):
    digest = md5_constructor(smart_str(plaintext)).hexdigest()
    if length:
        return digest[:length]
    return digest

def get_hashed_mtime(filename, length=12):
    try:
        filename = os.path.realpath(filename)
        mtime = str(int(os.path.getmtime(filename)))
    except OSError:
        return None
    return md5_constructor(smart_str(mtime)).hexdigest()[:length]