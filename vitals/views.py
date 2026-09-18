
from django.shortcuts import get_object_or_404, redirect, render

from visits.models import Visit

from .forms import VitalSignForm
from .models import VitalSign

# Create your views here.
def vital_sign_create(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if request.method == "POST":
        form = VitalSignForm(request.POST)

        if form.is_valid():
            vital_sign = form.save(commit=False)
            vital_sign.visit = visit
 
            return redirect("visit_detail", pk=visit.id)

    else:
        form = VitalSignForm()

    return render(
        request,
        "vitals/vital_sign_form.html",
        {
            "form": form,
            "visit": visit,
        },
    )