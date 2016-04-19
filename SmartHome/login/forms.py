from django import forms

class RegisterForm(forms.Form):
    Achternaam = forms.CharField()
    Voornaam = forms.CharField()
    Usernaam = forms.CharField()
    Wachtwoord = forms.CharField()
    Emailadres = forms.EmailField()

#class LoginForm(forms.Form):
