from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from laboratory.models import LabTest, TestOrder

@login_required
def dashboard(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_tests': LabTest.objects.count(),
        'total_orders': TestOrder.objects.count(),
    }
    return render(request, 'core/dashboard.html', context)
