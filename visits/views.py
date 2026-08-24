from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from patients.models import Patient

from .forms import VisitForm

from .models import Visit

from laboratory.forms import LaboratoryOrderForm
from laboratory.models import LaboratoryOrder, LaboratoryOrderItem


def visit_detail(request, pk):

    visit = get_object_or_404(
        Visit,
        pk=pk
    )

    if request.method == "POST":

        laboratory_form = LaboratoryOrderForm(
            request.POST
        )

        if laboratory_form.is_valid():

            selected_tests = laboratory_form.cleaned_data["tests"]

            laboratory_order = LaboratoryOrder.objects.create(
                visit=visit
            )

            for test in selected_tests:

                LaboratoryOrderItem.objects.create(
                    order=laboratory_order,
                    test=test
                )

            return redirect(
                "visit_detail",
                pk=visit.pk
            )

    else:

        laboratory_form = LaboratoryOrderForm()

    return render(
        request,
        "visits/visit_detail.html",
        {
            "visit": visit,
            "laboratory_form": laboratory_form,
        },
    )

def create_visit(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id,
    )

    if request.method == "POST":

        form = VisitForm(request.POST)

        if form.is_valid():

            visit = form.save(commit=False)

            visit.patient = patient

            visit.save()

            return redirect(
                "patient_detail",
                id=patient.id,
            )

    else:

        form = VisitForm()

    context = {
        "patient": patient,
        "form": form,
    }

    return render(
        request,
        "visits/create_visit.html",
        context,
    )