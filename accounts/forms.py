from django import forms
from .models import Customer, Installment
from datetime import date

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'hp_no': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'guarantor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guarantor_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'emi_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                     # 'max': date.today().isoformat()  # restrict to today or earlier
                }
            ),

            'vehicle_type': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control'}),
            'engine_number': forms.TextInput(attrs={'class': 'form-control'}),
            'chasis_number': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InstallmentForm(forms.ModelForm):
    customer_name = forms.CharField(
        label='Customer',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Installment
        fields = ['installment_date', 'paid_date', 'installment_due', 'paid_amount', 'balance_amount', 'remarks']  # remove customer from here
        widgets = {
            'installment_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'max': date.today().isoformat()}
            ),
            'paid_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'max': date.today().isoformat()}
            ),
            'installment_due': forms.NumberInput(attrs={'class': 'form-control'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

