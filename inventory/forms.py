from django import forms
from .models import StockItem, Invoice, Supplier
from laboratory.models import LabTest

class StockItemForm(forms.ModelForm):
    # Optional field to link tests
    required_stock = forms.ModelMultipleChoiceField(
        queryset=LabTest.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '6'}),
        required=False,
        label="Link to Lab Tests (Optional)"
    )

    class Meta:
        model = StockItem
        fields = ['name', 'category', 'invoice', 'batch_number', 'expiry_date', 'quantity_in_stock', 'reorder_level', 'unit_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., HIV Strip'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'invoice': forms.Select(attrs={'class': 'form-select'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Batch No.'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RestockForm(forms.Form):
    item = forms.ModelChoiceField(queryset=StockItem.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    quantity_added = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    unit_price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'supplier', 'date_received']
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INV-001'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'date_received': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
