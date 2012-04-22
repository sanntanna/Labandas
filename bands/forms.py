from django import forms

class ExpressRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="Email")
    password = forms.CharField(max_length=100, label="Senha",   widget=forms.PasswordInput())
    accept = forms.BooleanField(label="Aceito os termos de uso e quero me cadastrar")
