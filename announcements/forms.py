#coding=ISO-8859-1
from announcements.models import Announcement
from django import forms
from equipaments.models import EquipamentType

class AnnouncementForm(forms.ModelForm):
    title = forms.CharField(max_length=50, label="", widget=forms.TextInput(attrs={'placeholder':'Título', 'autocomplete':'off'}))
    text = forms.CharField(max_length=140, label="", widget=forms.Textarea(attrs={'placeholder':'Digite aqui o anuncio da sua banda', 'autocomplete':'off'}))
    instruments = forms.ModelMultipleChoiceField(queryset=EquipamentType.objects.all(), label="A vaga é para", widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Announcement
        fields = ('instruments','title', 'text',)