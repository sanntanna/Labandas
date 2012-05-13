from bands.models import MusicalStyle, Band
from datetime import datetime
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

class BandForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nome")
    musical_styles = forms.ModelMultipleChoiceField(queryset=MusicalStyle.objects.all(), label="Estilos musicais", widget=forms.CheckboxSelectMultiple)
    instruments = forms.ModelMultipleChoiceField(queryset=EquipamentType.objects.all(), label="O que voce toca na banda?", widget=forms.CheckboxSelectMultiple)
    
    def save(self, user):
        band = Band()
        band.name = self.cleaned_data['name']   
        band.registration_date = datetime.now()
        band.save_adding_musician(user.get_profile(), self.cleaned_data['instruments'])
        
        band.admins.add(user.get_profile())
        band.musical_styles = self.cleaned_data['musical_styles']