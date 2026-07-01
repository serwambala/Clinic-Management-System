from django import forms

from .models import Visit


class VisitForm(forms.ModelForm):

    class Meta:

        model = Visit

        fields = [
            "chief_complaint",
        ]