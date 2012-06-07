#coding=ISO-8859-1
from bands.models import MusicalStyle, Band, MusicianBand
from django import forms
from django.contrib.auth.models import User
from equipaments.models import EquipamentType

class ExpressRegistrationForm(forms.Form): 
    name = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="Email") 
    password = forms.CharField(max_length=100, label="Senha",   widget=forms.PasswordInput())
    instruments = forms.ModelMultipleChoiceField(queryset=EquipamentType.objects.all(), label="", widget=forms.CheckboxSelectMultiple)
    #accept = forms.BooleanField(label="Aceito os termos de uso e quero me cadastrar")
    
    def save(self):
        user = User()
        user.first_name = self.cleaned_data['name']
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.save()
        user.get_profile().type_instruments_play = self.cleaned_data['instruments']


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


class UserInfoForm(forms.ModelForm):
    cep = forms.CharField(max_length=8, label="Cep", required=False)
    musical_styles = forms.ModelMultipleChoiceField(queryset=MusicalStyle.objects.all(), label="Estilos musicais", widget=forms.CheckboxSelectMultiple, required=False)
    type_instruments_play = forms.ModelMultipleChoiceField(queryset=EquipamentType.objects.all(), label="Instrumentos que toca", widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        
        if any(self.initial):
            musician = self.instance.get_profile()
            
            self.fields['first_name'].label = "Nome"
            self.fields['first_name'].required = True
            
            self.fields['email'].label = "Email"
            self.fields['email'].required = True
            
            self.fields['cep'].initial = musician.cep
            
            self.fields['type_instruments_play'].initial = [m.pk for m in musician.type_instruments_play.filter()]
            self.fields['musical_styles'].initial = [m.pk for m in musician.musical_styles.filter()]
            
    
    def save(self, force_insert=False, force_update=False, commit=True):
        user = super(UserInfoForm, self).save(commit=False)
        
        musician = user.get_profile()
        musician.cep = self.cleaned_data['cep']
        musician.type_instruments_play = self.cleaned_data['type_instruments_play']
        musician.musical_styles = self.cleaned_data['musical_styles']
        
        if commit:
            user.save()
            musician.save()
        return user
    class Meta:
        model = User
        fields = ('first_name', 'email')