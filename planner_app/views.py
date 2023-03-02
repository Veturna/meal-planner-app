import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse

from weasyprint import HTML

from planner_app.models import Recipe, ProductInRecipe, Plan
from planner_app.form import EditRecipeForm, ProductInRecipeFormSet, AddPlanForm, EditPlanForm


class Profile(LoginRequiredMixin, View):
    """Widok profilu użytkownika"""
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
        return render(request, "recipes_view.html", {"recipes": recipes})


class RecipeDetail(View):
    """Szczegóły przepisu"""
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        products = ProductInRecipe.objects.filter(recipe=recipe)
        return render(request, "recipe_details.html", {"recipe": recipe, "products": products})


class EditRecipe(LoginRequiredMixin, View):
    """Edycja przepisu"""
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        form = EditRecipeForm(initial= {"name": recipe.name, "description": recipe.description,
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
            return redirect('edit-products-in-recipe', id=recipe.id)
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
            url = reverse('recipe-detail', kwargs={'id': recipe.id})
            return redirect(url)
        return render(request, "edit_product.html", {"formset": formset, "recipe": recipe})


class PlansView(LoginRequiredMixin, View):
    """Widok planów"""
    def get(self, request):
        plans = Plan.objects.all()
        return render(request, "plans_view.html", {"plans": plans})


class PlanDetail(View):
    """Szczegóły planu"""
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        return render(request, "plan_details.html", {"plan": plan})


class AddPlan(View):
    """Dodawanie planów"""
    def get(self, request):
        form = AddPlanForm()
        return render(request, 'add_plan.html', {'form': form})

    def post(self, request):
        form = AddPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.date = datetime.datetime.now()
            plan.user = request.user
            plan.save()
            plan.recipes.set(form.cleaned_data['recipes'])

            return redirect('plans')
        return render(request, "add_plan.html")


class EditPlan(View):
    """Edycja planu"""
    def get(self, request, plan_pk):
        plan = Plan.objects.get(pk=plan_pk)
        form = EditPlanForm()
        return render(request, 'edit_plan.html', {'form': form})
    def post(self, request, plan_pk):
        plan = Plan.objects.get(pk=plan_pk)
        form = EditPlanForm()
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            preparation = form.cleaned_data["preparation"]

            recipe.name = name
            recipe.description = description
            recipe.preparation = preparation

            recipe.save()
            return redirect('edit-products-in-recipe', id=recipe.id)
        return render(request, "edit_recipe.html")

class DeletePlan(View):
    """Usuwanie planów"""
    def get(self, request, plan_pk):
        plan = Plan.objects.get(pk=plan_pk)
        plan.delete()
        return redirect("plans")


class GenerateShoppingList(LoginRequiredMixin, View):
    """Generowanie listy zakupów"""
    def get(self, request, plan_pk):
        plan = Plan.objects.get(pk=plan_pk)
        shopping_list = []

        for recipe in plan.recipes.all():
            for product_in_recipe in recipe.productinrecipe_set.all():
                product = product_in_recipe.product
                quantity = product_in_recipe.quantity
                quantity_categories = product_in_recipe.quantity_categories
                product_name = product.name

                shopping_list.append((product_name, quantity, quantity_categories,))

        return render(request, "shopping_list.html", {"shopping_list": shopping_list, "plan": plan})


class GeneratePDF(View):
    """Generowanie PDF"""
    def get(self, request, plan_pk):
        plan = Plan.objects.get(pk=plan_pk)
        shopping_list = []

        for recipe in plan.recipes.all():
            for product_in_recipe in recipe.productinrecipe_set.all():
                product = product_in_recipe.product
                quantity = product_in_recipe.quantity
                quantity_categories = product_in_recipe.quantity_categories
                product_name = product.name

                shopping_list.append((product_name, quantity, quantity_categories))

        template = get_template('shopping_list.html')
        context = {"shopping_list": shopping_list, "plan": plan}

        html_string = template.render(context)
        html = HTML(string=html_string)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="lista-zakupow.pdf"'

        html.write_pdf(response)
        return response
