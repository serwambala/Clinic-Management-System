from django.db import models

# Create your models here.

from visits.models import Visit


class Consultation(models.Model):

    visit = models.OneToOneField(
        Visit,
        on_delete=models.PROTECT,
        related_name="consultation",
    )

    history = models.TextField(
        blank=True
    )

    examination = models.TextField(
        blank=True
    )

    assessment = models.TextField(
        blank=True
    )

    plan = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Consultation - {self.visit}"