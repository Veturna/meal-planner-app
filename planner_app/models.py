from django.db import models
from django.contrib.auth.models import User


CATEGORIES = (
    (1,"Fruit"),
    (2, "Vegetable"),
    (3, "Pasta"),
    (4, "Sauce"),
    (5, "Bakery"),
    (6, "Cheese"),
    (7, "Meat"),
    (8, "Sweeteners"),
    (9, "Dairy"),
    (10, "Seasoning"),
    (11, "Other"),
)


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.IntegerField(choices=CATEGORIES)


class Recipe(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True)
    products = models.ManyToManyField(Product, through='ProductInRecipe')
    preparation = models.TextField(null=False)


class ProductInRecipe(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
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

