from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from patients.models import Patient

from .forms import VisitForm

# Create your views here.
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