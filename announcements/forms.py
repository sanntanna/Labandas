#coding=ISO-8859-1
from announcements.models import Announcement
from django import forms
from equipaments.models import EquipamentType

class AnnouncementForm(forms.ModelForm):
    instruments = forms.ModelMultipleChoiceField(queryset=EquipamentType.objects.all(), label="A vaga é para", widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Announcement
        fields = ('instruments','title', 'text',)