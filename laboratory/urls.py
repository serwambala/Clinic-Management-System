from django.urls import path
from . import views


urlpatterns = [

    path(
        "results/<int:order_item_id>/",
        views.laboratory_result_entry,
        name="laboratory_result_entry",
    ),

    path(
        "results/<int:order_item_id>/view/",
        views.laboratory_result_detail,
        name="laboratory_result_detail",
    ),

    path(
        "specimens/collect/<int:visit_id>/",
        views.specimen_collection,
        name="specimen_collection",
    ),

    path(
        "specimens/assign/<int:order_item_id>/",
        views.specimen_assignment,
        name="specimen_assignment",
    ),
]