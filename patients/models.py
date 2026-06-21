from django.db import models
from django.conf import settings
# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    mrn = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )

    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.mrn:
            self.mrn = f"{settings.CLINIC_MRN_PREFIX}{self.pk:06d}"
            super().save(update_fields=["mrn"])

    def __str__(self):
        return f"{self.mrn} - {self.first_name} {self.last_name}"