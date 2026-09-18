from django.urls import path

from . import views


urlpatterns = [
    path(
        "visits/<int:visit_id>/",
        views.vital_sign_create,
        name="vital_sign_create",
    ),
]