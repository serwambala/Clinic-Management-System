from django.urls import path
from . import views


urlpatterns = [

    path(
        "results/<int:order_item_id>/",
        views.laboratory_result_entry,
        name="laboratory_result_entry",
    ),

]