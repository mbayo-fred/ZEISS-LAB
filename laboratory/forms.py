from django import forms
from .models import TestOrder, LabTest, TestCategory
from patients.models import Patient

class OrderForm(forms.ModelForm):
    class Meta:
        model = TestOrder
        fields = ['patient', 'tests', 'priority']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'tests': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), # Using checkboxes is easier to select multiple tests
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active tests
        self.fields['tests'].queryset = LabTest.objects.filter(is_active=True)


class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        # ADDED 'required_stock' to the fields list
        fields = ['code', 'name', 'category', 'sample_type', 'price', 'reference_range', 'required_stock']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., HEM04'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Blood Group'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'sample_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Blood'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 15000'}),
            'reference_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 70-100 or Negative'}),
            # ADDED the widget for the stock dropdown
            'required_stock': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }
