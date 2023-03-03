from django.db import models
from django.contrib.auth.models import User


CATEGORIES = (
    (1, "Fruit"),
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
    (1, "Szklanka"),
    (2, "Łyżeczka"),
    (3, "Łyżka"),
    (4, "Sztuka"),
)


class Product(models.Model):
    """
    Model representing a product
    """
    name = models.CharField(max_length=64, unique=True)
    category = models.IntegerField(choices=CATEGORIES)

    def __str__(self):
        """
        Return a string representation of the product
        :return: str
        """
        return self.name


class Recipe(models.Model):
    """
    Model representing a recipe
    """
    name = models.CharField(max_length=64, unique=True, help_text='Wprowadź nazwę przepisu')
    description = models.TextField(null=True, help_text="Wprowadź opis przepisu")
    products = models.ManyToManyField(Product, through='ProductInRecipe', help_text='Wybierz produkty używane w przepisie')
    preparation = models.TextField(null=False, help_text='Wprowadź instrukcję przygotowania produktu')

    def __str__(self):
        """
        Return a string representation of the recipe
        :return: str
        """
        return self.name


class ProductInRecipe(models.Model):
    """
    Model representing a connection between a product and a recipe
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text='Wybierz produkt')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, help_text='Wybierz przepis')
    quantity = models.IntegerField(help_text='Wprowadź ilość produktu')
    quantity_categories = models.IntegerField(choices=QUANTITY_CATEGORIES, default=None, help_text='Wybierz jednostkę miary dla ilości produktu')

    def __str__(self):
        """
        Return a string representation product in recipe
        :return: str
        """
        return f"{self.product} w {self.recipe}"

class Plan(models.Model):
    """
    Model representing a plan
    """
    name = models.CharField(max_length=64, unique=True, help_text='Wprowadź nazwę planu')
    description = models.TextField(null=True, help_text='Wprowadź opis planu')
    date = models.DateTimeField(null=True, help_text='Data utworzenia planu')
    recipes = models.ManyToManyField(Recipe, help_text='Wybierz przepisy używane w planie')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Użytkownik, który utworzył plan')

    def __str__(self):
        """
        Return a string representation product in recipe
        :return: str
        """
        return self.name


class ShoppingList(models.Model):
    """
    Model representing a shopping list
    """
    name = models.CharField(max_length=64, unique=True, help_text='Wprowadź nazwę listy')
    date = models.DateTimeField(help_text='Data utworzenia listy')
    products = models.ManyToManyField(Product, help_text='Produkty dostępne w liście')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Użytkownik, który utworzył listę')

    def __str__(self):
        """
        Return a string representation product in recipe
        :return: str
        """
        return self.name
