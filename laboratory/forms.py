from django import forms
from .models import LaboratoryOrder, LaboratoryTest, LaboratoryResult


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

            for parameter in parameters:

                self.fields[str(parameter.id)] = forms.CharField(
                    label=parameter.name,
                    required=False,
                )