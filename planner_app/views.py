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
    """View showing the user's profile."""
    def get(self, request):
        """
        A method that serves a GET request and shows the user's profile.

        :param request: HttpRequest
        :return: HttpResponse
        """
        return render(request, "profile.html")


class MainPage(View):
    """View showing the main page of application"""
    def get(self, request):
        """
        A method that serves a GET request and shows the main page.

        :param request: HttpRequest
        :return: HttpResponse
        """
        return render(request, "main_page.html")


class AboutApp(View):
    """View showing additional information about application"""
    def get(self, request):
        """
        A method that serves a GET request and shows the additional information about application.

        :param request: HttpRequest
        :return: HttpResponse
        """
        return render(request, "about_app.html")


class RecipesView(View):
    """View showing all recipes from db"""
    def get(self, request):
        """
        A method that serves a GET request and shows all recipes.

        :param request: HttpRequest
        :return: HttpResponse
        """
        recipes = Recipe.objects.all()
        return render(request, "recipes_view.html", {"recipes": recipes})


class RecipeDetail(View):
    """View showing the details for recipe with a specific primary key"""
    def get(self, request, recipe_pk):
        """
        A method that serves a GET request and shows the additional information about recipe.

        :param request: HttpRequest
        :param recipe_pk: recipe primary key
        :return: HttpResponse
        """
        recipe = Recipe.objects.get(id=recipe_pk)
        products = ProductInRecipe.objects.filter(recipe=recipe)
        return render(request, "recipe_details.html", {"recipe": recipe, "products": products})


class EditRecipe(LoginRequiredMixin, View):
    """View showing form to edit recipe with a specific primary key"""
    def get(self, request, recipe_pk):
        """
        A method that serves a GET request and shows the form to edit the name, description and preparation of the recipe.

        :param request: HttpRequest
        :param recipe_pk: recipe primary_key
        :return: HttpResponse
        """
        recipe = Recipe.objects.get(id=recipe_pk)
        form = EditRecipeForm(initial= {"name": recipe.name, "description": recipe.description,
                                        "preparation": recipe.preparation,
                                        }
                              )
        return render(request, 'edit_recipe.html', {'form': form, "recipe": recipe})

    def post(self, request, recipe_pk):
        """
        A method that serves a POST request. Data transferred to the form: name, description and preparation of the recipe.

        :param request: HttpRequest
        :param recipe_pk: recipe primary key
        :return: HttpResponse
        """
        recipe = Recipe.objects.get(id=recipe_pk)
        form = EditRecipeForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            preparation = form.cleaned_data["preparation"]

            recipe.name = name
            recipe.description = description
            recipe.preparation = preparation

            recipe.save()

            url = reverse('edit-products-in-recipe', kwargs={"recipe_pk": recipe.id})
            return redirect(url)
        return render(request, "edit_recipe.html")


class EditProductsInRecipe(LoginRequiredMixin, View):
    """View showing form to edit products in recipe with a specific primary key"""
    def get(self, request, recipe_pk):
        """
        A  method that serves a GET request and shows the form to edit the products (product, quantity, quantity_categories) in recipe.

        :param request: HttpRequest
        :param recipe_pk: recipe primary key
        :return: HttpResponse
        """
        recipe = Recipe.objects.get(id=recipe_pk)
        products = ProductInRecipe.objects.filter(recipe=recipe)
        formset = ProductInRecipeFormSet(queryset=products)
        return render(request, 'edit_product.html', {"formset": formset, "recipe": recipe})

    def post(self, request, recipe_pk):
        """
        A method that serves a POST request. Data transferred to the form: product, quantity, quantity_categories of the recipe.

        :param request: HttpRequest
        :param recipe_pk: recipe primary key
        :return: HttpResponse
        """
        recipe = Recipe.objects.get(id=recipe_pk)
        formset = ProductInRecipeFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            url = reverse('recipe-detail', kwargs={'recipe_pk': recipe.id})
            return redirect(url)
        return render(request, "edit_product.html", {"formset": formset, "recipe": recipe})


class PlansView(LoginRequiredMixin, View):
    """View showing all plans from db"""
    def get(self, request):
        """
        A method that serves a GET request and shows all the plans

        :param request: HttpRequest
        :return: HttpResponse
        """
        plans = Plan.objects.all()
        return render(request, "plans_view.html", {"plans": plans})


class PlanDetail(View):
    """View showing the details for plan with a specific primary key"""
    def get(self, request, plan_pk):
        """
        A method that serves a GET request and shows the additional information about plan.

        :param request: HttpRequest
        :param recipe_pk: recipe primary key
        :return: HttpResponse
        """
        plan = Plan.objects.get(id=plan_pk)
        return render(request, "plan_details.html", {"plan": plan})


class AddPlan(View):
    """View showing the form to adding the plan to db"""
    def get(self, request):
        """
        A method that serves a GET request and shows the form to add the plan (name, description, recipes).

        :param request: HttpRequest
        :return: HttpResponse
        """
        form = AddPlanForm()
        return render(request, 'add_plan.html', {'form': form})

    def post(self, request):
        """
        A method that serves a POST request. Data transferred to the form: name, description, recipes. Data and user are add automatically

        :param request: HttpRequest
        :return: HttpResponse
        """
        form = AddPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.date = datetime.datetime.now()
            plan.user = request.user
            plan.save()
            plan.recipes.set(form.cleaned_data['recipes'])

            url = reverse('plans')
            return redirect(url)
        return render(request, "add_plan.html")


class EditPlan(View):
    """View showing the form to edit the plan with specific primary key"""
    def get(self, request, plan_pk):
        """
        A method that serves a GET request and shows the form to edit the plan (name, description, recipes)

        :param request: HttpRequest
        :param plan_pk: plan primary key
        :return: HttpResponse
        """
        plan = Plan.objects.get(pk=plan_pk)
        form = EditPlanForm(instance=plan)
        return render(request, 'edit_plan.html', {'form': form})

    def post(self, request, plan_pk):
        """
        A method that serves a POST request. Data transferred to the form: name, description, recipes.

        :param request: HttpRequest
        :param plan_pk: plan primary key
        :return: HttpResponse
        """
        plan = Plan.objects.get(pk=plan_pk)
        form = EditPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            plan.recipes.set(form.cleaned_data['recipes'])

            url = reverse('plan-detail', kwargs={'plan_pk': plan.id})
            return redirect(url)
        return render(request, "edit_plan.html", {"form": form})


class DeletePlan(View):
    """View deleting the plan with specific primary key from db"""
    def get(self, request, plan_pk):
        """
        A method that serves a GET request and deleting the plan

        :param request: HttpRequest
        :param plan_pk: plan primary key
        :return: HttpResponse
        """
        plan = Plan.objects.get(pk=plan_pk)
        plan.delete()

        url = reverse('plans')
        return redirect(url)


class GenerateShoppingList(LoginRequiredMixin, View):
    """View generating the shopping list base of plan detail view"""
    def get(self, request, plan_pk):
        """
        A method that serves a GET request and generate the view with list of the products form recipes in that plan

        :param request: HttpRequest
        :param plan_pk: plan primary key
        :return: HttpResponse
        """
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
    """View generating the GenerateShoppingList view in PDF"""
    def get(self, request, plan_pk):
        """
        A method that serves a GET request and generate the PDF base of GenerateShoppingList view

        :param request: HttpRequest
        :param plan_pk: plan primary key
        :return: HttpResponse
        """
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
