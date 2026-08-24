from django.shortcuts import get_object_or_404, render, redirect

from .models import LaboratoryOrderItem, LaboratoryResult
from .forms import LaboratoryResultForm


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

                    LaboratoryResult.objects.create(
                        order_item=order_item,
                        parameter=parameter,
                        value=value,
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