from django.urls import path

from . import views


urlpatterns = [
    path(
        "<int:patient_id>/new/",
        views.create_visit,
        name="create_visit",
    ),
]