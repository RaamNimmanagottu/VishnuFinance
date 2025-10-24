
from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.urls import reverse_lazy

app_name="customers"

urlpatterns = [
    
    path('', RedirectView.as_view(url=reverse_lazy('customers:login'), permanent=False)),
    path('customers/',views.customer_list, name="customers"),
    path('customer_create/',views.customer_create, name="customer_create"),
    path('customer_edit/<int:pk>/', views.customer_edit, name="customer_edit"),
    path('customer_delete/<int:pk>/', views.customer_delete, name="customer_delete"),
    path('customer_detail/<int:pk>/',views.customer_detail, name="customer_detail"),
    path('customer/<int:customer_id>/installment/add/', views.installment_create, name='installment_create'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
