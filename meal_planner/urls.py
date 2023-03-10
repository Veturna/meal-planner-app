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
from django.urls import path, re_path, include
from planner_app.views import MainPage, AboutApp, RecipesView, RecipeDetail, EditRecipe, EditProductsInRecipe, \
    PlansView, PlanDetail, Profile, GenerateShoppingList, AddPlan, DeletePlan, GeneratePDF, EditPlan

urlpatterns = [
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('accounts/profile/', Profile.as_view()),
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name='main'),
    path('about/', AboutApp.as_view(), name='about'),
    path('recipes/', RecipesView.as_view(), name='recipe-view'),
    re_path(r'^detail/(?P<recipe_pk>\d+)/$', RecipeDetail.as_view(), name='recipe-detail'),
    re_path(r'^edit/(?P<recipe_pk>\d+)/$', EditRecipe.as_view(), name='edit-recipe'),
    re_path(r'^edit/product/(?P<recipe_pk>\d+)/$', EditProductsInRecipe.as_view(), name='edit-products-in-recipe'),
    path('plans/', PlansView.as_view(), name='plans'),
    re_path(r'^plan/detail/(?P<plan_pk>\d+)/$', PlanDetail.as_view(), name='plan-detail'),
    re_path(r'^shopping-list/(?P<plan_pk>\d+)/$', GenerateShoppingList.as_view(), name='generate-shopping-list'),
    re_path(r'^shopping-list-pdf/(?P<plan_pk>\d+)/$', GeneratePDF.as_view(), name='generate-shopping-list-pdf'),
    path('add/plan/', AddPlan.as_view(), name='add-plan'),
    re_path(r'^delete/plan/(?P<plan_pk>\d+)/$', DeletePlan.as_view(), name='delete-plan'),
    re_path(r'^edit/plan/(?P<plan_pk>\d+)/$', EditPlan.as_view(), name='edit-plan'),
]

