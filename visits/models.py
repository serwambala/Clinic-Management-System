from django.db import models

# Create your models here.
from patients.models import Patient

class Visit(models.Model):

    patient = models.ForeignKey(

        Patient,
        on_delete=models.PROTECT,
        related_name="visits",
    )

    visit_date = models.DateTimeField(
        auto_now_add=True
    )

    chief_complaint = models.TextField()

    def __str__(self):
        return f"{self.patient.mrn} - {self.visit_date:%Y-%m-%d}"