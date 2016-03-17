from django import forms

class UploadFileForm(forms.Form):
#    def __init__(self,name,filename):
#        self.title = name
#        self.file = filename
#    title = forms.CharField()
    file = forms.FileField()
