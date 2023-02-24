from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from planner_app.models import Recipe, ProductInRecipe, Plan
from planner_app.form import EditRecipeForm, ProductInRecipeFormSet, AddRecipe


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "profile.html")


class MainPage(View):
    """Strona główna aplikacji"""
    def get(self, request):
        return render(request, "main_page.html")


class AboutApp(View):
    """Strona "o aplikacji"""
    def get(self, request):
        return render(request, "about_app.html")


class RecipesView(View):
    """Widok przepisów"""
    def get(self, request):
        recipes = Recipe.objects.all()
        return render(request, "recipes_view.html", {"recipes":recipes})


class RecipeDetail(View):
    """Szczegóły przepisu"""
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        products = ProductInRecipe.objects.filter(recipe=recipe)
        return render(request, "recipe_details.html", {"recipe":recipe, "products":products})


class EditRecipe(LoginRequiredMixin, View):
    """Edycja przepisu"""
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        form = EditRecipeForm(initial= {"name": recipe.name,
                                        "description": recipe.description,
                                        "preparation": recipe.preparation,
                                        }
                              )
        return render(request, 'edit_recipe.html', {'form': form, "recipe": recipe})
    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        form = EditRecipeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            preparation = form.cleaned_data["preparation"]

            recipe.name = name
            recipe.description = description
            recipe.preparation = preparation

            recipe.save()
            return render(request, "edit_recipe.html")


class EditProductsInRecipe(LoginRequiredMixin, View):
    """Edycja produktów w przepisie"""
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        products = ProductInRecipe.objects.filter(recipe=recipe)
        formset = ProductInRecipeFormSet(queryset=products)
        return render(request, 'edit_product.html', {"formset": formset, "recipe": recipe})
    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        formset = ProductInRecipeFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('recipe-details', id=recipe.id)
        return render(request, "edit_product.html", {"formset": formset, "recipe": recipe})

class AddRecipe(LoginRequiredMixin, View):
    def get(self, request):
        form = AddRecipe()
        return render(request, 'add_recipe.html', {'form': form})

class PlansView(LoginRequiredMixin, View):
    """Widok planów"""
    def get(self, request):
        plans = Plan.objects.all()
        return render(request, "plans_view.html", {"plans": plans})


class PlanDetail(LoginRequiredMixin, View):
    """Szczegóły planu"""
    def get(self, request,id):
        plan = Plan.objects.get(id=id)
        return render(request, "plan_details.html", {"plan": plan})





