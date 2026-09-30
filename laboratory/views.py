from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
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
    SpecimenReceivingForm,
)

def laboratory_result_entry(request, order_item_id):

    order_item = get_object_or_404(
        LaboratoryOrderItem,
        id=order_item_id
    )

    active_assignment = (
        order_item.specimen_assignments
        .filter(is_active=True)
        .select_related("specimen")
        .first()
    )

    if (
        active_assignment is None
        or active_assignment.specimen.status != "received"
    ):
        return redirect(
            "specimen_assignment",
            order_item_id=order_item.id
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

            if order_item.entered_results == 0:

                order_item.status = "collected"

            elif order_item.entered_results < order_item.expected_results:

                order_item.status = "results_in_progress"

            else:

                order_item.status = "ready_for_verification"

            order_item.save(
                update_fields=["status"]
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

@login_required
def laboratory_result_verify(request, order_item_id):

    order_item = get_object_or_404(
        LaboratoryOrderItem,
        id=order_item_id
    )

    if request.method != "POST":
        return redirect(
            "laboratory_result_detail",
            order_item_id=order_item.id
        )

    if (
        order_item.status != "ready_for_verification"
        or order_item.expected_results == 0
        or order_item.entered_results != order_item.expected_results
    ):
        return redirect(
            "laboratory_result_detail",
            order_item_id=order_item.id
        )

    with transaction.atomic():

        order_item.status = "verified"
        order_item.verified_by = request.user
        order_item.verified_at = timezone.now()

        order_item.save(
            update_fields=[
                "status",
                "verified_by",
                "verified_at",
            ]
        )

    return redirect(
        "laboratory_result_detail",
        order_item_id=order_item.id
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

def specimen_receiving(request, specimen_id):

    specimen = get_object_or_404(
        Specimen,
        id=specimen_id
    )

    if request.method == "POST":

        form = SpecimenReceivingForm(
            request.POST,
            instance=specimen
        )

        if form.is_valid():

            action = form.cleaned_data["action"]

            with transaction.atomic():

                if action == "received":

                    specimen.status = "received"
                    specimen.received_at = timezone.now()
                    specimen.rejection_reason = ""

                elif action == "rejected":

                    specimen.status = "rejected"
                    specimen.received_at = None
                    specimen.rejection_reason = (
                        form.cleaned_data["rejection_reason"]
                    )

                specimen.save(
                    update_fields=[
                        "status",
                        "received_at",
                        "rejection_reason",
                        "updated_at",
                    ]
                )

            return redirect(
                "visit_detail",
                pk=specimen.visit.id
            )

    else:

        form = SpecimenReceivingForm(
            instance=specimen
        )

    return render(
        request,
        "laboratory/specimen_receiving.html",
        {
            "form": form,
            "specimen": specimen,
            "visit": specimen.visit,
        }
    )

def specimen_assignment(request, order_item_id):
    order_item = get_object_or_404(
        LaboratoryOrderItem,
        id=order_item_id
    )

    visit = order_item.order.visit

    active_assignment = (
        order_item.specimen_assignments
        .filter(is_active=True)
        .select_related(
            "specimen",
            "specimen__specimen_type",
            "specimen__container",
        )
        .first()
    )

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
            "active_assignment": active_assignment,

        }
    )