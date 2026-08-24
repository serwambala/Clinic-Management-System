from django import forms
from .models import LaboratoryTest


class LaboratoryOrderForm(forms.Form):

    tests = forms.ModelMultipleChoiceField(
        queryset=LaboratoryTest.objects.filter(active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )