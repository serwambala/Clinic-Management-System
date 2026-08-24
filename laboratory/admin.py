from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    LaboratoryTest,
    LaboratoryOrder,
    LaboratoryOrderItem,
    LaboratoryTestParameter,
)


admin.site.register(LaboratoryTest)
admin.site.register(LaboratoryOrder)
admin.site.register(LaboratoryOrderItem)
admin.site.register(LaboratoryTestParameter)