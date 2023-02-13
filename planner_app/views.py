from django.shortcuts import render
from django.views import View


class MainPage(View):
    def get(self, request):
        return render(request, "main_page.html")


class AboutApp(View):
    def get(self, request):
        return render(request, "about_app.html")

