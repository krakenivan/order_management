from django import forms


class DateFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        label="С",
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    end_date = forms.DateField(
        required=False,
        label="По",
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
