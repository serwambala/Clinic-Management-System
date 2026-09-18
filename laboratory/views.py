from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from django.utils import timezone
from visits.models import Visit

from .models import (
    LaboratoryOrderItem,
    LaboratoryResult,
    Specimen,
    SpecimenAssignment,
)

from .forms import (
    LaboratoryResultForm,
    SpecimenCollectionForm,
    SpecimenAssignmentForm,
)

def laboratory_result_entry(request, order_item_id):

    order_item = get_object_or_404(
        LaboratoryOrderItem,
        id=order_item_id
    )

    if request.method == "POST":

        form = LaboratoryResultForm(
            request.POST,
            order_item=order_item
        )

        if form.is_valid():

            for parameter in order_item.test.parameters.all():

                value = form.cleaned_data.get(
                    str(parameter.id)
                )

                if value:

                    LaboratoryResult.objects.update_or_create(
                        order_item=order_item,
                        parameter=parameter,
                        defaults={
                            "value": value,
                        },
                    )

                    

            return redirect(
                "visit_detail",
                pk=order_item.order.visit.pk
            )

    else:

        form = LaboratoryResultForm(
            order_item=order_item
        )

    return render(
        request,
        "laboratory/result_entry.html",
        {
            "form": form,
            "order_item": order_item,
        }
    )

def laboratory_result_detail(request, order_item_id):

    order_item = get_object_or_404(
        LaboratoryOrderItem,
        id=order_item_id
    )

    results = order_item.results.select_related(
        "parameter"
    ).all()

    return render(
        request,
        "laboratory/result_detail.html",
        {
            "order_item": order_item,
            "results": results,
        }
    )

def specimen_collection(request, visit_id):

    visit = get_object_or_404(
        Visit,
        id=visit_id
    )

    if request.method == "POST":

        form = SpecimenCollectionForm(
            request.POST
        )

        if form.is_valid():

            specimen = form.save(
                commit=False
            )

            specimen.visit = visit
            specimen.status = "collected"
            specimen.collected_at = timezone.now()

            specimen.save()

            return redirect(
                "visit_detail",
                pk=visit.id
            )

    else:

        form = SpecimenCollectionForm()

    return render(
        request,
        "laboratory/specimen_collection.html",
        {
            "form": form,
            "visit": visit,
        }
    )

def specimen_assignment(request, order_item_id):
    order_item = get_object_or_404(
        LaboratoryOrderItem,
        id=order_item_id
    )

    visit = order_item.order.visit

    if request.method == "POST":
        form = SpecimenAssignmentForm(
            request.POST,
            order_item=order_item
        )

        if form.is_valid():
            with transaction.atomic():
                # Deactivate the current active assignment, if one exists.
                SpecimenAssignment.objects.filter(
                    order_item=order_item,
                    is_active=True,
                ).update(
                    is_active=False
                )

                # Create the new active assignment.
                assignment = form.save(commit=False)
                assignment.order_item = order_item
                assignment.is_active = True

                assignment.full_clean()
                assignment.save()

                # The test now has a collected specimen assigned to it.
                order_item.status = "collected"
                order_item.save(update_fields=["status"])

            return redirect(
                "visit_detail",
                pk=visit.id
            )

    else:
        form = SpecimenAssignmentForm(
            order_item=order_item
        )

    return render(
        request,
        "laboratory/specimen_assignment.html",
        {
            "form": form,
            "order_item": order_item,
            "visit": visit,
        }
    )