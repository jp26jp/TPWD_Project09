from datetime import datetime

from django import forms

from .models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('created_date',)

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        try:
            datetime.strptime(str(expiration_date), '%Y-%m-%d').date()
        except ValueError:
            raise forms.ValidationError('Please enter date as yyyy-mm-dd')
        return expiration_date
