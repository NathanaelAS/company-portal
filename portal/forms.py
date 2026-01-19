from django import forms
from .models import Request
from datetime import date, timedelta

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'start_date', 'end_date']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # This "init" function runs when the form is created
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = date.today().strftime('%Y-%m-%d')

        # We loop through all fields and add the Bootstrap class
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name == 'start_date' or field_name == 'end_date':
                field.widget.attrs['min'] = today

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        category = cleaned_data.get("category")

        # We only care about this logic for Vacations
        if category == 'VACATION':

            if not start_date:
                self.add_error('start_date', "The Start Date cannot be empty for Vacation/Leave Requests")
            if not end_date:
                self.add_error('end_date', "The End Date cannot be empty for Vacation/Leave Requests")
            
            if start_date and end_date:
                # 1. Check if End is before Start
                if end_date < start_date:
                    self.add_error('end_date', "The End Date cannot be earlier than the Start Date.")
                    return cleaned_data # Stop here if dates are swapped

                # 2. Count business days (Monday-Friday)
                business_days = 0
                current_date = start_date
                while current_date <= end_date:
                    if current_date.weekday() < 5: # 0-4 are Mon-Fri, 5-6 are Sat-Sun
                        business_days += 1
                    current_date += timedelta(days=1)

                # 3. If zero business days, the request is invalid
                if business_days == 0:
                    raise forms.ValidationError(
                        "Your request only covers weekend days. Please select at least one working day."
                    )

        return cleaned_data