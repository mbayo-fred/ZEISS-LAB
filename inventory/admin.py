from django.contrib import admin
from .models import Supplier, StockItem, StockUsage

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone']

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity_in_stock', 'reorder_level', 'supplier']
    list_filter = ['category', 'supplier']
    search_fields = ['name']

@admin.register(StockUsage)
class StockUsageAdmin(admin.ModelAdmin):
    list_display = ['stock_item', 'quantity_used', 'used_by', 'date_used']
    readonly_fields = ['stock_item', 'quantity_used', 'used_by', 'reason', 'date_used']
