from django import forms

from .models import VitalSign


class VitalSignForm(forms.ModelForm):
    class Meta:
        model = VitalSign
        fields = [
            "temperature",
            "systolic_bp",
            "diastolic_bp",
            "pulse_rate",
            "respiratory_rate",
            "oxygen_saturation",
            "weight",
        ]