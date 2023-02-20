from django.shortcuts import render
from django.views import View

from planner_app.models import Recipe, ProductInRecipe, Product
from planner_app.form import EditRecipeForm


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


class EditRecipe(View):
    """Edycja przepisu"""
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        form = EditRecipeForm(initial= {"name": recipe.name,
                                        "description": recipe.description,
                                        "preparation": recipe.preparation,
                                        }
                              )
        return render(request, 'edit_recipe.html', {'form': form, "recipe": recipe, "products": products})
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
            return render(request, "edit_recipe.html", {"name": name,
                                                        "description": description,
                                                        "preparation": preparation,
                                                         }
                          )


class AddRecipe(View):
    """Dodanie przepisu"""
    pass


class Login(View):
    """Widok logowania"""
    pass


class UserView(View):
    """Widok po zalogowaniu"""
    pass


class EditUser(View):
    """Edycja użytkownika"""
    pass


class PlansView(View):
    """Widok planów"""
    pass





