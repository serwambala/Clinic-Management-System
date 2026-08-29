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