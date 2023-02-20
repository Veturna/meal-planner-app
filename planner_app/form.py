from django import forms
from planner_app.models import QUANTITY_CATEGORIES


class EditRecipeForm(forms.Form):
    name = forms.CharField(label="Nazwa", max_length=64)
    description = forms.CharField(label="Opis", max_length=2000)
    preparation = forms.CharField(label="Przygotowanie", max_length=10000, widget=forms.Textarea())


class EditProductInRecipeForm(forms.Form):
    product = forms.CharField(label="Produkt", max_length=255)
    quantity = forms.IntegerField(label="Ilość")
    quantity_categories = forms.ChoiceField(label="Kategoria", choices=QUANTITY_CATEGORIES)