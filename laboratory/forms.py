from django import forms
from django.db.models import Q
from .models import (
    LaboratoryOrder,
    LaboratoryTest,
    LaboratoryResult,
    Specimen,
    SpecimenAssignment,
)

class LaboratoryOrderForm(forms.Form):

    tests = forms.ModelMultipleChoiceField(
        queryset=LaboratoryTest.objects.filter(active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

class LaboratoryResultForm(forms.Form):

    def __init__(self, *args, order_item=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.order_item = order_item

        if order_item is not None:

            parameters = order_item.test.parameters.all()

            existing_results = {
                result.parameter_id: result.value
                for result in order_item.results.all()
            }

            for parameter in parameters:

                self.fields[str(parameter.id)] = forms.CharField(
                    label=parameter.name,
                    required=False,
                    initial=existing_results.get(parameter.id, ""),
                )

class SpecimenCollectionForm(forms.ModelForm):

    class Meta:
        model = Specimen
        fields = [
            "specimen_type",
            "container",
            "volume",
            "volume_unit",
            "notes",
        ]

class SpecimenAssignmentForm(forms.ModelForm):

    def __init__(self, *args, order_item=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.order_item = order_item

        if order_item is not None:
            self.instance.order_item = order_item

            visit = order_item.order.visit
            requirements = order_item.test.specimen_requirements.all()

            specimen_filter = Q(pk__in=[])

            for requirement in requirements:
                specimen_filter |= Q(
                    visit=visit,
                    specimen_type=requirement.specimen_type,
                    container=requirement.container,
                )

            already_assigned_specimen_ids = (
                SpecimenAssignment.objects
                .filter(order_item=order_item)
                .values_list("specimen_id", flat=True)
            )

            self.fields["specimen"].queryset = (
                Specimen.objects
                .filter(specimen_filter)
                .exclude(id__in=already_assigned_specimen_ids)
                .distinct()
            )

            self.no_available_specimens = (
                not self.fields["specimen"].queryset.exists()
            )

            if self.no_available_specimens:
                self.fields["specimen"].help_text = (
                    "No compatible unassigned specimen is available. "
                    "Collect a new specimen before assigning one."
                )

            self.fields["requirement"].queryset = (
                order_item.test.specimen_requirements.all()
            )

    class Meta:

        model = SpecimenAssignment

        fields = [
            "specimen",
            "requirement",
        ]