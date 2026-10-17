from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime

from .models import LabTest, TestOrder, OrderItem
from patients.models import Patient
from .forms import OrderForm

@login_required
def test_list(request):
    tests = LabTest.objects.all().order_by('category__name', 'name')
    return render(request, 'laboratory/tests.html', {'tests': tests})

@login_required
def create_order(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.ordered_by = request.user
            order.save()
            
            # Save the selected tests and their prices
            for test in form.cleaned_data['tests']:
                OrderItem.objects.create(order=order, test=test, price=test.price)
                
            return redirect('dashboard') # Redirect back to dashboard after saving
    else:
        # Pre-select the patient in the form
        form = OrderForm(initial={'patient': patient})
        
    return render(request, 'laboratory/create_order.html', {'form': form, 'patient': patient})

@login_required
def daily_revenue(request):
    today = timezone.now().date()
    # Calculate total money made today from all orders
    today_orders = TestOrder.objects.filter(created_at__date=today)
    
    total = 0
    for order in today_orders:
        total += sum(item.price for item in order.orderitem_set.all())
        
    return render(request, 'laboratory/revenue.html', {'orders': today_orders, 'total': total})
