from django.db import models
from visits.models import Visit
from django.core.exceptions import ValidationError

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

class SpecimenType(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Container(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class SpecimenRequirement(models.Model):

    test = models.ForeignKey(
        LaboratoryTest,
        on_delete=models.PROTECT,
        related_name="specimen_requirements",
    )

    specimen_type = models.ForeignKey(
        SpecimenType,
        on_delete=models.PROTECT,
        related_name="test_requirements",
    )

    container = models.ForeignKey(
        Container,
        on_delete=models.PROTECT,
        related_name="test_requirements",
    )

    is_preferred = models.BooleanField(
        default=False
    )

    collection_instructions = models.TextField(
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["test", "specimen_type", "container"],
                name="unique_test_specimen_type_container_requirement",
            ),

            models.UniqueConstraint(
                fields=["test"],
                condition=models.Q(is_preferred=True),
                name="unique_preferred_specimen_requirement_per_test",
        ),
    ]
       

    def __str__(self):
        return (
            f"{self.test.name} - "
            f"{self.specimen_type.name} - "
            f"{self.container.name}"
        )
class Specimen(models.Model):

    visit = models.ForeignKey(
        "visits.Visit",
        on_delete=models.PROTECT,
        related_name="specimens",
    )

    specimen_type = models.ForeignKey(
        SpecimenType,
        on_delete=models.PROTECT,
        related_name="specimens",
    )

    container = models.ForeignKey(
        Container,
        on_delete=models.PROTECT,
        related_name="specimens",
    )

    specimen_number = models.CharField(
        max_length=50,
        unique=True,
    )

    status = models.CharField(
        max_length=30,
        default="collected",
    )

    collected_at = models.DateTimeField()

    received_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    rejection_reason = models.TextField(
        blank=True,
    )

    volume = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    volume_unit = models.CharField(
        max_length=20,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.specimen_number


class SpecimenAssignment(models.Model):

    specimen = models.ForeignKey(
        Specimen,
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    order_item = models.ForeignKey(
        "LaboratoryOrderItem",
        on_delete=models.PROTECT,
        related_name="specimen_assignments",
    )

    requirement = models.ForeignKey(
        SpecimenRequirement,
        on_delete=models.PROTECT,
        related_name="assignments",
       
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
    )

    def clean(self):
        if self.specimen.visit != self.order_item.order.visit:
            raise ValidationError(
                "Specimen and laboratory order item must belong to the same visit."
            )

        if self.requirement.test != self.order_item.test:
            raise ValidationError(
                "Specimen requirement must belong to the same laboratory test."
            )

        if self.specimen.specimen_type != self.requirement.specimen_type:
            raise ValidationError(
                "Specimen type does not match the specimen requirement."
            )

        if self.specimen.container != self.requirement.container:
            raise ValidationError(
                "Specimen container does not match the specimen requirement."
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["specimen", "order_item"],
                name="unique_specimen_order_item_assignment",
            ),
        ]

    def __str__(self):
        return (
            f"{self.specimen.specimen_number} → "
            f"{self.order_item.test.name}"
        )

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
        ("verified", "Verified"),
        ("released", "Released"),
        ("cancelled", "Cancelled"),
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

    @property

    def expected_results(self):
        return self.test.parameters.count()


    @property
    def entered_results(self):
        return self.results.count()


    @property
    def result_state(self):

        if self.entered_results == 0:
            return "No results"

        elif self.entered_results < self.expected_results:
            return "Partial results"

        else:
            return "Results complete"

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