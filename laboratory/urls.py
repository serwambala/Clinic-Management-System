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
        "results/<int:order_item_id>/verify/",
        views.laboratory_result_verify,
        name="laboratory_result_verify",
    ),

    path(
        "specimens/collect/<int:visit_id>/",
        views.specimen_collection,
        name="specimen_collection",
    ),

    path(
        "specimens/receive/<int:specimen_id>/",
        views.specimen_receiving,
        name="specimen_receiving",
    ),

    path(
        "specimens/assign/<int:order_item_id>/",
        views.specimen_assignment,
        name="specimen_assignment",
    ),

    
]
