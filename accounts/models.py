from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta

class Customer(models.Model):
    hp_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField()
    village = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=15)
    guarantor_name = models.CharField(max_length=200, blank=True, null=True)
    guarantor_mobile = models.CharField(max_length=15, blank=True, null=True)

    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.FloatField()
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.IntegerField()
    start_date = models.DateField()
    emi_day = models.PositiveSmallIntegerField(default=5, help_text="Fixed EMI day each month (1-28)")

    # Vehicle details
    vehicle_type = models.CharField(max_length=100, blank=True, null=True)
    vehicle_name = models.CharField(max_length=100, blank=True, null=True)
    vehicle_model = models.CharField(max_length=100, blank=True, null=True)
    engine_number = models.CharField(max_length=100, blank=True, null=True)
    chasis_number = models.CharField(max_length=100, blank=True, null=True)
    insurance = models.CharField(max_length=100, blank=True, null=True)

    @property
    def end_date(self):
        """Automatically calculate loan end date"""
        return self.start_date + relativedelta(months=self.duration_months)

    @property
    def first_emi_date(self):
        """First EMI due date aligned to emi_day"""
        return self.start_date.replace(day=self.emi_day)

    @property
    def emi_schedule(self):
        """Return EMI schedule dynamically without saving to DB"""
        schedule = []
        emi_date = self.start_date
        for i in range(self.duration_months):
            schedule.append({
                "installment_no": i + 1,
                "installment_date": emi_date,
                "amount": self.emi_amount
            })
            emi_date += relativedelta(months=1)
        return schedule
    
    def amortization_schedule(self):
        schedule = []
        P = float(self.loan_amount)
        r = self.interest_rate / 100 / 12   # monthly interest rate
        n = self.duration_months

        # EMI formula
        emi = (P * r * (1+r)**n) / ((1+r)**n - 1) if r > 0 else P/n

        balance = P
        total_paid = 0

        # Get EMI fixed day from loan details (e.g., 5 means 5th of each month)
        emi_day = self.emi_day   # add this field in your Loan/Customer model

        # First EMI date = start_date adjusted to emi_day
        start_date = self.start_date
        first_emi_date = start_date.replace(day=emi_day)

        # If start_date’s day is already past emi_day → take next month
        if start_date.day > emi_day:
            first_emi_date = (start_date + relativedelta(months=1)).replace(day=emi_day)

        for i in range(1, n+1):
            interest = balance * r
            principal = emi - interest
            balance -= principal
            total_paid += emi

            emi_date = first_emi_date + relativedelta(months=i-1)

            schedule.append({
                "installment_no": i,
                "date": emi_date,
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "total_payment": round(emi, 2),
                "balance": round(balance if balance > 0 else 0, 2),
                "loan_paid_to_date": round(total_paid, 2),
            })

        return schedule

    def __str__(self):
        return f"{self.name} ({self.hp_no})"


class Installment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="installments")
    
    # Scheduled and actual dates
    installment_date = models.DateField()  # Original due date
    paid_date = models.DateField(blank=True, null=True)  # Actual date paid
    
    # Amounts
    installment_due = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Optional remarks
    remarks = models.TextField(blank=True, null=True)

    def remaining_emi(self):
        """Calculate remaining EMI amount"""
        return self.installment_due - self.paid_amount

    def __str__(self):
        return f"Installment {self.installment_date} - {self.customer.name}"