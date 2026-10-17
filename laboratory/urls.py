from django.urls import path
from . import views

app_name = 'laboratory'

urlpatterns = [
    path('tests/', views.test_list, name='tests'),
    path('order/create/<int:patient_id>/', views.create_order, name='create_order'),
    path('revenue/', views.daily_revenue, name='revenue'),
]
