from django import forms


class PDFFileForm(forms.Form):
    file = forms.FileField()
