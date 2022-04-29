from django.db import models


class Unit(models.Model):
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    pass


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    pass


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=50)
    instructions = models.CharField(max_length=65535)
    pass


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=6)
    people = models.IntegerField()
    pass
