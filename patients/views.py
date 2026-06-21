from django.shortcuts import render, redirect
from .models import Patient
from django.contrib import messages


def register_patient(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")

        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone_number=phone_number,
        )

        messages.success(
            request,
            f"Patient {patient.mrn} registered succesfully."
        )

        return redirect("register_patient")

    return render(
        request,
        "patients/register_patient.html"
    )

def patient_list(request):

    search = request.GET.get("search")

    patients = Patient.objects.order_by("-created_at")

    if search:
        patients = patients.filter(
            first_name__icontains=search
        )

    context = {
        "patients" : patients
    }

    return render(
        request,
        "patients/patient_list.html",
        context
    )