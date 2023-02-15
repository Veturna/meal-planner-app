from django.shortcuts import render
from django.views import View


class MainPage(View):
    def get(self, request):
        return render(request, "main_page.html")


class AboutApp(View):
    def get(self, request):
        return render(request, "about_app.html")

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


class RecipesView(View):
    """Widok przepisów"""
    pass


class AddRecipe(View):
    """Dodanie przepisu"""
    pass


class EditRecipe(View):
    """Edycja przepisu"""
    pass

