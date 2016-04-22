from django import forms

class LoginForm(forms.Form):
	Usernaam = forms.CharField()
	Wachtwoord = forms.CharField()
