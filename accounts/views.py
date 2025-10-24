from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Installment
from .forms import CustomerForm, InstallmentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

@login_required
def accounts(request):
    return render(request,"accounts/accounts.html")

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'accounts/customers.html', {'customers': customers})

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)

    personal_fields = ['hp_no','customer_name','father_name','mobile','address','village','guarantor_name','guarantor_mobile']
    loan_fields = ['loan_amount','interest_rate','emi_amount','duration_months','start_date','emi_day']
    vehicle_fields = ['vehicle_type','vehicle_name','vehicle_model','engine_number','chasis_number','insurance']

    context = {
        'form': form,
        'personal_fields': personal_fields,
        'loan_fields': loan_fields,
        'vehicle_fields': vehicle_fields,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('customers:customers')
        else:
            # Print form errors for debugging
            print("Form is invalid:", form.errors)

    return render(request, 'accounts/customer_form.html', context)




@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    emi_schedule = customer.amortization_schedule()
    
    return render(request, 'accounts/customer_detail.html', {
        'customer': customer,
        'emi_schedule': emi_schedule
    })


@login_required
def installment_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    form = InstallmentForm(request.POST or None, initial={'customer_name': customer.name})
    
    if form.is_valid():
        inst = form.save(commit=False)
        inst.customer = customer  # set the customer automatically
        inst.save()
        return redirect('customers:customer_detail', pk=customer_id)
    
    return render(request, 'accounts/installment_form.html', {'form': form, 'customer': customer})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('customers:customers')
    return render(request, 'accounts/customer_form.html', {'form': form})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customers:customers')
    return render(request, 'accounts/customer_confirm_delete.html', {'customer': customer})



def login_view(request):
    if request.user.is_authenticated:
        return redirect('customers:customers')  # Redirect logged-in users

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('customers:customers')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect('customers:login')