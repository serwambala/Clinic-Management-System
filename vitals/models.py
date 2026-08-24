from django.db import models

# Create your models here.
from visits.models import Visit


class VitalSign(models.Model):

    visit = models.ForeignKey(
        Visit,
        on_delete=models.PROTECT,
        related_name="vital_signs",
    )

    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )

    systolic_bp = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    diastolic_bp = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    pulse_rate = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    respiratory_rate = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    oxygen_saturation = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    recorded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Vitals - {self.visit}"