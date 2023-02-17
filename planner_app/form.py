from django import forms


class EditRecipeForm(forms.Form):
    name = forms.CharField(label="Nazwa", max_length=64)
    description = forms.CharField(max_length=2000)
    preparation = forms.CharField(max_length=10000, widget=forms.Textarea())