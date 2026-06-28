from django.contrib import admin

# Register your models here.

from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):

    list_display = (
        "patient",
        "visit_date",
        "chief_complaint",
    )

    search_fields = (
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "chief_complaint",
    )

    list_filter = (
        "visit_date",
    )