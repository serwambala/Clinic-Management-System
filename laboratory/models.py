from django.db import models
from visits.models import Visit


class LaboratoryTest(models.Model):

    name = models.CharField(
        max_length=255
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    specimen_type = models.CharField(
        max_length=100,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

class LaboratoryTestParameter(models.Model):

    test = models.ForeignKey(
        LaboratoryTest,
        on_delete=models.PROTECT,
        related_name="parameters",
    )

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=50
    )

    unit = models.CharField(
        max_length=50,
        blank=True
    )

    data_type = models.CharField(
        max_length=20,
        default="text"
    )

    def __str__(self):
        return f"{self.test.name} - {self.name}"
    
class LaboratoryOrder(models.Model):

    visit = models.ForeignKey(
        Visit,
        on_delete=models.PROTECT,
        related_name="laboratory_orders",
    )

    ordered_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Lab Order #{self.pk} - {self.visit}"


class LaboratoryOrderItem(models.Model):

    STATUS_CHOICES = [
        ("ordered", "Ordered"),
        ("collected", "Sample Collected"),
        ("completed", "Completed"),
    ]

    order = models.ForeignKey(
        LaboratoryOrder,
        on_delete=models.PROTECT,
        related_name="items",
    )

    test = models.ForeignKey(
        LaboratoryTest,
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ordered",
    )

    result = models.TextField(
        blank=True
    )

    recorded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.order} - {self.test.name}"

class LaboratoryResult(models.Model):

    order_item = models.ForeignKey(
        LaboratoryOrderItem,
        on_delete=models.PROTECT,
        related_name="results",
    )

    parameter = models.ForeignKey(
        LaboratoryTestParameter,
        on_delete=models.PROTECT,
        related_name="results",
    )

    value = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.order_item.test.name} - {self.parameter.name}"