from django import forms
from .models import *


class riskPredForm(forms.ModelForm):
    class Meta():
        model=riskPredModel
        fields=['Stock']
