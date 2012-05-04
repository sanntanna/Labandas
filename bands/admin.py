from bands.models import Musician, Band, MusicalStyle, MusicianType
from django.contrib import admin

admin.site.register(Musician)
admin.site.register(MusicianType)
admin.site.register(MusicalStyle)
admin.site.register(Band)