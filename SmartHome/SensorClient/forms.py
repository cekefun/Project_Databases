from django import forms

class UploadFileForm(forms.Form):
    Uplfile = forms.FileField()
    household = forms.IntegerField()

class UploadjsonForm(forms.Form):
    Uplfile = forms.FileField()
