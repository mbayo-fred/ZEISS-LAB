from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

from .models import LabTest, TestOrder, OrderItem
from patients.models import Patient
from .forms import OrderForm, LabTestForm

@login_required
def test_list(request):
    tests = LabTest.objects.all().order_by('category__name', 'name')
    edit_id = request.GET.get('edit_id')
    
    # If editing, load the existing test into the form
    if edit_id:
        test_to_edit = get_object_or_404(LabTest, id=edit_id)
        form = LabTestForm(instance=test_to_edit)
    else:
        test_to_edit = None
        form = LabTestForm()

    if request.method == 'POST':
        edit_id_post = request.POST.get('edit_id')
        
        if edit_id_post:
            # Update existing test (e.g. if price changed)
            test_to_edit = get_object_or_404(LabTest, id=edit_id_post)
            form = LabTestForm(request.POST, instance=test_to_edit)
        else:
            # Create new test
            form = LabTestForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('laboratory:tests')

    return render(request, 'laboratory/tests.html', {
        'tests': tests, 
        'form': form, 
        'test_to_edit': test_to_edit
    })


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
