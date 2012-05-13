from bands.models import Musician, Band, MusicalStyle, MusicianBand
from django.contrib import admin

admin.site.register(Musician)
admin.site.register(MusicalStyle)
admin.site.register(MusicianBand)
admin.site.register(Band)