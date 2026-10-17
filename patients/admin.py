from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'gender', 'age', 'phone', 'created_at']
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone', 'national_id']
    list_filter = ['gender', 'created_at']
    readonly_fields = ['patient_id', 'created_at']
