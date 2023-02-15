from django.contrib import admin
from planner_app.models import (Product, Recipe, ProductInRecipe)


admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(ProductInRecipe)


