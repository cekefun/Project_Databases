from django import forms

class UploadFileForm(forms.Form):
#    def __init__(self,name,filename):
#        self.title = name
#        self.file = filename
#    title = forms.CharField()
    Uplfile = forms.FileField()
    household = forms.IntegerField()

class UploadjsonForm(forms.Form):
    Uplfile = forms.FileField()
