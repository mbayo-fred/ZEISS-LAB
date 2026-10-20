from django.db import models
from core.models import User
from django.utils import timezone

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='invoices')
    date_received = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.invoice_number} - {self.supplier.name}"

class StockItem(models.Model):
    CATEGORY_CHOICES = [
        ('STRIP', 'Test Strip'),
        ('REAGENT', 'Reagent'),
        ('CONSUMABLE', 'Consumable'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    
    batch_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Sort so the closest expiry date is at the top
        ordering = ['expiry_date']

    def __str__(self):
        return f"{self.name} (Batch: {self.batch_number})"

class StockUsage(models.Model):
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='usage_logs')
    quantity_used = models.PositiveIntegerField()
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=255)
    date_used = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_item.name} - {self.quantity_used} used"
