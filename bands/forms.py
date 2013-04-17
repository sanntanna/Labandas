#coding=ISO-8859-1
from bands.models import MusicalStyle, Band, MusicianBand
from django import forms
from django.contrib.auth.models import User
from equipaments.models import EquipamentType

class ExpressRegistrationForm(forms.ModelForm): 
    first_name = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'placeholder':'Nome completo', 'autocomplete':'off'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'placeholder':'Email', 'autocomplete':'off'})) 
    password = forms.CharField(max_length=100, label="", widget=forms.PasswordInput(attrs={'placeholder':'Senha', 'autocomplete':'off'}))
    
    def save(self, *args, **kwargs):
        self.instance.username = self.instance.email
        self.instance.set_password(self.instance.password)
        super(ExpressRegistrationForm, self).save(*args, **kwargs)
    
    class Meta:
        model = User
        fields = ('first_name', 'email', 'password')

class BandForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Nome")
    musical_styles = forms.ModelMultipleChoiceField(queryset=MusicalStyle.objects.all(), label="A banda toca", widget=forms.CheckboxSelectMultiple)
    
    def save(self, force_insert=False, force_update=False, commit=True):
        band = super(BandForm, self).save(commit=False)
        if commit:
            band.save()
        band.musical_styles = self.cleaned_data['musical_styles']
        
        return band
        
    class Meta:
        model = Band
        fields = ('name', 'musical_styles')


class BandMusicianForm(forms.ModelForm):
    instruments = forms.ModelMultipleChoiceField(queryset=EquipamentType.objects.all(), label="Instrumentos que voce toca na banda", widget=forms.CheckboxSelectMultiple)
    
    def save(self, band, musician, musician_in_band=None, is_admin=False):
        musician_in_band.instruments = self.cleaned_data['instruments']
    
    def save_admin(self, musician, band):
        musician_in_band = MusicianBand.objects.create(band=band,musician=musician, active=True, is_admin=True)
        musician_in_band.instruments = self.cleaned_data['instruments']
        
    class Meta:
        model = MusicianBand
        fields = ('instruments',)