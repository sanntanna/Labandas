from django.contrib import admin
from equipaments.models import Category, Brand, EquipamentType, Equipament

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(EquipamentType)
admin.site.register(Equipament)