from django import forms
from .models import TestOrder, LabTest
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
