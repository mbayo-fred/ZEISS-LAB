from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientRegistrationForm
from laboratory.models import TestOrder, OrderItem, TestResult
from inventory.models import StockUsage  # Import the stock usage model

@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    edit_id = request.GET.get('edit_id')

    if edit_id:
        patient = get_object_or_404(Patient, id=edit_id)
        form = PatientRegistrationForm(instance=patient)
    else:
        patient = None
        form = PatientRegistrationForm()

    if request.method == 'POST':
        edit_id_post = request.POST.get('edit_id')
        if edit_id_post:
            patient = get_object_or_404(Patient, id=edit_id_post)
            form = PatientRegistrationForm(request.POST, instance=patient)
        else:
            patient = None
            form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            # 1. Save Patient
            patient = form.save(commit=False)
            if not edit_id_post:
                patient.created_by = request.user
            patient.save()

            # 2. Handle Tests & Results
            selected_tests = form.cleaned_data['tests']

            if selected_tests:
                existing_order = TestOrder.objects.filter(patient=patient).order_by('-created_at').first()

                if not existing_order:
                    existing_order = TestOrder.objects.create(
                        patient=patient,
                        ordered_by=request.user,
                        priority='ROUTINE',
                        payment_method=form.cleaned_data.get('payment_method', 'CASH')
                    )
                else:
                    if form.cleaned_data.get('payment_method'):
                        existing_order.payment_method = form.cleaned_data.get('payment_method')
                        existing_order.save()

                for test in selected_tests:
                    existing_item = OrderItem.objects.filter(order=existing_order, test=test).first()

                    if not existing_item:
                        item = OrderItem.objects.create(
                            order=existing_order,
                            test=test,
                            price=test.price
                        )
                        
                        # --- NEW: DEDUCT STOCK & LOG USAGE ---
                        for stock in test.required_stock.all():
                            if stock.quantity_in_stock > 0:
                                stock.quantity_in_stock -= 1
                                stock.save()
                                
                                # Create an audit log of this stock usage
                                StockUsage.objects.create(
                                    stock_item=stock,
                                    used_by=request.user,
                                    quantity_used=1,
                                    reason=f"Used for {test.name} (Patient: {patient.full_name}, Order: {existing_order.order_number})"
                                )
                        # -------------------------------------

                    else:
                        item = existing_item

                    # Get Result Value and Custom Reference Range
                    result_key = f'result_{test.id}'
                    ref_range_key = f'ref_range_{test.id}'

                    result_value = request.POST.get(result_key)
                    custom_ref_range = request.POST.get(ref_range_key)

                    if result_value:
                        TestResult.objects.update_or_create(
                            order_item=item,
                            defaults={
                                'value': result_value,
                                'reference_range': custom_ref_range,
                                'performed_by': request.user,
                                'is_abnormal': False
                            }
                        )

            return redirect('patients:list')

    return render(request, 'patients/list.html', {'patients': patients, 'form': form, 'patient': patient})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    orders = TestOrder.objects.filter(patient=patient).order_by('-created_at')

    return render(request, 'patients/detail.html', {
        'patient': patient,
        'orders': orders
    })
