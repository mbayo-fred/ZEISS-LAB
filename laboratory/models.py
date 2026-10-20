from django.db import models
from core.models import User
from patients.models import Patient
from inventory.models import StockItem

class TestCategory(models.Model):
    name = models.CharField(max_length=100)  # Hematology, Chemistry, Microbiology
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Test Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class LabTest(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(TestCategory, on_delete=models.PROTECT, related_name='tests')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sample_type = models.CharField(max_length=50)  # Blood, Urine, Stool
    turnaround_hours = models.PositiveIntegerField(default=24)
    reference_range = models.CharField(max_length=200, blank=True)
    unit = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    required_stock = models.ManyToManyField(StockItem, blank=True, help_text="Select strips/reagents used for this test")

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class TestOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COLLECTED = 'COLLECTED', 'Sample Collected'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class Priority(models.TextChoices):
        ROUTINE = 'ROUTINE', 'Routine'
        URGENT = 'URGENT', 'Urgent'
        STAT = 'STAT', 'STAT'

    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Cash'
        MOBILE = 'MOBILE', 'Mobile Money'
        INSURANCE = 'INSURANCE', 'Insurance'
        CARD = 'CARD', 'Credit/Debit Card'

    order_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='orders')
    ordered_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='orders_created'
    )
    tests = models.ManyToManyField(LabTest, through='OrderItem', related_name='orders')
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.ROUTINE)
    payment_method = models.CharField(max_length=15, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    clinical_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # First, save the object to get an ID from the database
        super().save(*args, **kwargs)
        # If it's a new order (no order_number yet), generate one using the ID
        if not self.order_number:
            self.order_number = f"ORD-{self.id:05d}" # e.g., ORD-00001
            # Call save again to update the order_number field
            super().save(update_fields=['order_number'])

    def __str__(self):
        return f"{self.order_number} - {self.patient.full_name}"

    @property
    def total_amount(self):
        return sum(item.price for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(TestOrder, on_delete=models.CASCADE)
    test = models.ForeignKey(LabTest, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.test.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.order_number} - {self.test.name}"


class Sample(models.Model):
    order = models.ForeignKey(TestOrder, on_delete=models.CASCADE, related_name='samples')
    barcode = models.CharField(max_length=30, unique=True)
    sample_type = models.CharField(max_length=50)
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True)
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"{self.barcode} ({self.sample_type})"


class TestResult(models.Model):
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='result')
    value = models.CharField(max_length=200)
    unit = models.CharField(max_length=30, blank=True)
    reference_range = models.CharField(max_length=200, blank=True)
    is_abnormal = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='results_entered')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='results_verified')
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_item.order.order_number} - {self.order_item.test.name}: {self.value}"
