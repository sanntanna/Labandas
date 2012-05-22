from django import forms
from equipaments.models import EquipamentType
from solicitations.models import Solicitation

class AskMusicianForm(forms.ModelForm):
    instruments = forms.ModelMultipleChoiceField(queryset=EquipamentType.objects.all(), label="O que vai tocar?", widget=forms.CheckboxSelectMultiple)
    
    def save(self):
        return None
    
    class Meta:
        model = Solicitation
        fields = ('instruments')