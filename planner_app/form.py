from django import forms
from planner_app.models import ProductInRecipe, Plan, Recipe
from django.forms import modelform_factory, modelformset_factory


class EditRecipeForm(forms.Form):
    """
    Form for editing the name, description and preparation of the recipe.
    """
    name = forms.CharField(label="Nazwa", max_length=64)
    description = forms.CharField(label="Opis", max_length=2000)
    preparation = forms.CharField(label="Przygotowanie", max_length=10000, widget=forms.Textarea())


#"""
# Form for ProductInRecipe model
# """

ProductInRecipeForm = modelform_factory(ProductInRecipe, fields=('product', 'quantity', 'quantity_categories'))


#"""
# Set of forms for ProductInRecipe model. Set is created include ProductInRecipeForm as base
#"""
ProductInRecipeFormSet = modelformset_factory(ProductInRecipe, form=ProductInRecipeForm, extra=0)


class AddPlanForm(forms.ModelForm):
    """
    Change recipes to quesryset and put it in form as multiple checkbox field
    """
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        """
        Form to add the name, description and recipes to plan
        """
        model = Plan
        fields = ("name", "description", "recipes")


class EditPlanForm(forms.ModelForm):
    """
    Change recipes to quesryset and put it in form as multiple checkbox field
    """
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        """
        Form to edit name, description and recipes in plan
        """
        model = Plan
        fields = ("name", "description", "recipes")
