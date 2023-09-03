from django import forms

class UserForm(forms.Form):
    origin_city = forms.CharField(widget=forms.TextInput(), required=True)
    arrival_city = forms.CharField(widget=forms.TextInput(), required=True)
    search_start_date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose year", "Choose month", "Choose day")))
    search_end_date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose year", "Choose month", "Choose day")))