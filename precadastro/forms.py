#coding=ISO-8859-1
from django import forms
from models import Record

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record