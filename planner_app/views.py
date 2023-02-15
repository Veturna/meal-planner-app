from django.shortcuts import render
from django.views import View

from planner_app.models import Recipe


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




class AddRecipe(View):
    """Dodanie przepisu"""
    pass


class EditRecipe(View):
    """Edycja przepisu"""
    pass

