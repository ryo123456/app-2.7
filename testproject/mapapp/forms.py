from django import forms


class MyForm(forms.Form):
    search = forms.CharField(max_length=100)
