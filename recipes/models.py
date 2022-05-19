from django.db import models


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=50)
    description = models.CharField(max_length=65535, blank=True, default='')
    people = models.IntegerField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.recipe_name

    pass


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=65535)
    quantity = models.DecimalField(decimal_places=2, max_digits=6)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.ingredient_name

    pass


class RecipeInstructions(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.IntegerField()
    instruction = models.CharField(max_length=65535)

    def __str__(self):
        return str(self.step) + ": " + self.instruction

    pass
