from django.contrib import admin
from .models import Patient

# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "mrn",
        "first_name",
        "last_name",
        "gender",
        "phone_number",
        "created_at",

    )

    search_fields = (
        "mrn",
        "first-name",
        "last_name",
        "phone_number",
    )

    list_filter = (
        "gender",
        "created_at",
    )

    ordering = ("-created_at",)