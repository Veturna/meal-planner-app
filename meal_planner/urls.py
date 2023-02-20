"""meal_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from planner_app.views import MainPage, AboutApp, RecipesView, RecipeDetail, EditRecipe, EditProductsInRecipe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name='main-page'),
    path('about/', AboutApp.as_view(), name='about-app'),
    path('recipes/', RecipesView.as_view(), name='recipes'),
    re_path(r'^detail/(?P<id>\d+)/$', RecipeDetail.as_view(), name='recipe-detail'),
    re_path(r'^edit/(?P<id>\d+)/$', EditRecipe.as_view(), name='edit-recipe'),
    re_path(r'^edit/product/(?P<id>\d+)/$', EditProductsInRecipe.as_view(), name='edit-product'),

]

