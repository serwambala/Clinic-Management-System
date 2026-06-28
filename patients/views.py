from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from django.contrib import messages
from django.db.models import Q


def patient_detail(request, id):

    patient = get_object_or_404(
        Patient,
        id=id
    )

    context = {
        "patient": patient
    }

    return render(
        request,
        "patients/patient_detail.html",
        context
    )

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
            Q(mrn__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(phone_number__icontains=search)
    )

        

    context = {
        "patients" : patients
    }

    return render(
        request,
        "patients/patient_list.html",
        context
    )