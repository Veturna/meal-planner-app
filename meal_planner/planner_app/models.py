from django.db import models
from django.contrib.auth.models import User


class Product:
    name = models.CharField(max_length=64, unique=True)
    category = models.CharField(null=False)


class Recipe(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True)
    products = models.ManyToManyField(Product, through='ProductInRecipe')
    preparation = models.TextField(null=False)


class ProductInRecipe(models.Model):
    product = models.ForeignKey(Product)
    recipe = models.ForeignKey(Recipe)
    quantity = models.IntegerField()


class Plan(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True)
    date = models.DateTimeField()
    recipes = models.ManyToManyField(Recipe)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ShoppingList(models.Model):
    name = models.CharField(max_length=64, unique=True)
    date = models.DateTimeField()
    products = models.ManyToManyField(Product)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

