from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category']

        # This "init" function runs when the form is created
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # We loop through all fields and add the Bootstrap class
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'