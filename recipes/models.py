from django.db import models


class Unit(models.Model):
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code

    pass


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient_name

    pass


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=50)
    instructions = models.CharField(max_length=65535)

    def __str__(self):
        return self.recipe_name

    pass


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=6)
    people = models.IntegerField()

    def __str__(self):
        return self.recipe + " " + self.ingredient

    pass
