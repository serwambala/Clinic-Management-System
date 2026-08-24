from django.urls import path

from . import views


urlpatterns = [
    path(
        "<int:patient_id>/new/",
        views.create_visit,
        name="create_visit",
    ),

     path(
        "visits/<int:pk>/",
        views.visit_detail,
        name="visit_detail"
    ),
]