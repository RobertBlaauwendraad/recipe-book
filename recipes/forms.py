from django import forms
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm
from .models import Recipe, RecipeIngredients, RecipeInstructions

class RecipeEditMultiForm(MultiModelForm):
    form_classes = {
        'recipe': RecipeForm,
        'ingredients': RecipeIngredientsForm,
        'instructions': RecipeInstructionsForm,
    }

class RecipeIngredientsForm(ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = '__all__'

class RecipeInstructionsForm(ModelForm):
    class Meta:
        model = RecipeInstructions
        fields = '__all__'

class RecipeForm(ModelForm, RecipeIngredientsForm, RecipeInstructionsForm):
    class Meta:
        model = Recipe
        fields = '__all__'