from django.contrib import admin
from .models import TestCategory, LabTest, TestOrder, OrderItem, Sample, TestResult

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'sample_type', 'price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['code', 'name']

@admin.register(TestOrder)
class TestOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'patient', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['order_number', 'patient__first_name', 'patient__last_name']
    inlines = [OrderItemInline]

admin.site.register([Sample, TestResult])
