from django import forms
from planner_app.models import ProductInRecipe, Plan, Recipe
from django.forms import modelform_factory, modelformset_factory


class EditRecipeForm(forms.Form):
    name = forms.CharField(label="Nazwa", max_length=64)
    description = forms.CharField(label="Opis", max_length=2000)
    preparation = forms.CharField(label="Przygotowanie", max_length=10000, widget=forms.Textarea())


ProductInRecipeForm = modelform_factory(ProductInRecipe, fields=('product', 'quantity', 'quantity_categories'))
ProductInRecipeFormSet = modelformset_factory(ProductInRecipe, form=ProductInRecipeForm, extra=0)


class AddPlanForm(forms.ModelForm):
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Plan
        fields = ("name", "description", "recipes")
