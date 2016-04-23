from django import forms

class HouseForm(forms.Form):
    Streetname = forms.CharField()
    Streetnumber = forms.DecimalField()
    City = forms.CharField()
    Postalcode = forms.DecimalField()
    Country = forms.CharField()
    Price = forms.DecimalField()
