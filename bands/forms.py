from django import forms
from django.contrib.auth.models import User

class ExpressRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="Email")
    password = forms.CharField(max_length=100, label="Senha",   widget=forms.PasswordInput())
    accept = forms.BooleanField(label="Aceito os termos de uso e quero me cadastrar")
    
    def save(self):
        new_user = User()
        new_user.first_name = self.cleaned_data['name']
        new_user.username = self.cleaned_data['email']
        new_user.email = self.cleaned_data['email']
        new_user.password = self.cleaned_data['password']
        new_user.save()
        