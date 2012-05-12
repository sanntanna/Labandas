from bands.models import MusicianType, Musician
from django import forms
from django.contrib.auth.models import User

class ExpressRegistrationForm(forms.Form): 
    name = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="Email")
    password = forms.CharField(max_length=100, label="Senha",   widget=forms.PasswordInput())
    musicianType = forms.ModelMultipleChoiceField(queryset=MusicianType.objects.all(), label="", widget=forms.CheckboxSelectMultiple)
    #accept = forms.BooleanField(label="Aceito os termos de uso e quero me cadastrar")
    
    def save(self):
        user = User()
        user.first_name = self.cleaned_data['name']
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.save()
        user.get_profile().musician_type = self.cleaned_data['musicianType']
        
            
        
    
    
    

