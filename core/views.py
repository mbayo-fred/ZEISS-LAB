from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

from patients.models import Patient
from laboratory.models import LabTest, TestOrder, OrderItem
from .forms import CustomUserCreationForm

@login_required
def dashboard(request):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    def get_revenue(start_date, end_date=None):
        if end_date:
            orders = TestOrder.objects.filter(created_at__date__range=[start_date, end_date])
        else:
            orders = TestOrder.objects.filter(created_at__date=start_date)
        
        total = OrderItem.objects.filter(order__in=orders).aggregate(total=Sum('price'))['total']
        return total or 0

    # Calculate Revenue
    rev_today = get_revenue(today)
    rev_yesterday = get_revenue(yesterday)
    
    rev_week = OrderItem.objects.filter(order__created_at__date__gte=start_of_week).aggregate(total=Sum('price'))['total'] or 0
    rev_month = OrderItem.objects.filter(order__created_at__date__gte=start_of_month).aggregate(total=Sum('price'))['total'] or 0
    rev_year = OrderItem.objects.filter(order__created_at__date__gte=start_of_year).aggregate(total=Sum('price'))['total'] or 0

    context = {
        'total_patients': Patient.objects.count(),
        'total_tests': LabTest.objects.count(),
        'total_orders': TestOrder.objects.count(),
        'rev_today': rev_today,
        'rev_yesterday': rev_yesterday,
        'rev_week': rev_week,
        'rev_month': rev_month,
        'rev_year': rev_year,
    }
    return render(request, 'core/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = 'RECEP' 
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})
