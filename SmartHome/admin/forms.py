from django import forms

CHOICESTIME = (('minute', 'minute',),('hour', 'hour',),('day', 'day',), ('month', 'month',),('year','year',))
CHOICES=(('streetnamecity','streetnamecity',),('postalcode','postalcode',),('country','country',))

class LoginForm(forms.Form):
	Usernaam = forms.CharField()
	Wachtwoord = forms.CharField()

class UserForm(forms.Form):
	UserName = forms.CharField()

class RequestForm(forms.Form):
	start = forms.DateField()
	to = forms.DateField()	
	selecttime = forms.ChoiceField(widget=forms.RadioSelect,choices=CHOICESTIME)
	selectregion = forms.ChoiceField(widget=forms.RadioSelect,choices=CHOICES)
	city = forms.CharField(required=False)
	streetname = forms.CharField(required=False)
	postalcode = forms.CharField(required=False)
	country = forms.CharField(required=False)
