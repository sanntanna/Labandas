#coding=ISO-8859-1
from django import forms
from models import Record

class RecordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nome"
        self.fields['instrument'].label = "Instrumentos que toca"
        self.fields['uf'].label = "Estado"

    class Meta:
        model = Record