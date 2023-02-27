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
    (11, "Cereals"),
    (12, "Fish"),
    (13, "Oil"),
    (14, "Flour"),
    (15, "Other"),
)


QUANTITY_CATEGORIES = (
    (1, "Glass"),
    (2, "Tea Spoon"),
    (3, "Table Spoon"),
    (4, "Piece"),
)


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.IntegerField(choices=CATEGORIES)
    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True)
    products = models.ManyToManyField(Product, through='ProductInRecipe')
    preparation = models.TextField(null=False)
    def __str__(self):
        return self.name


class ProductInRecipe(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    quantity_categories = models.IntegerField(choices=QUANTITY_CATEGORIES, default=None)


class Plan(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True)
    date = models.DateTimeField(null = True)
    recipes = models.ManyToManyField(Recipe)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    name = models.CharField(max_length=64, unique=True)
    date = models.DateTimeField()
    products = models.ManyToManyField(Product)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

