from django import forms
from django.forms import ModelForm
from django.forms import modelformset_factory

from .models import Recipe, RecipeIngredients, RecipeInstructions


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_name', 'description', 'people')
        labels = {
            'recipe_name': '',
            'description': '',
            'people': '',
        }
        widgets = {
            'recipe_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'people': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Servings'}),
        }


IngredientFormset = modelformset_factory(
    RecipeIngredients,
    fields=('ingredient_name', 'quantity', 'unit'),
    labels={
        'ingredient_name': '',
        'quantity': '',
        'unit': '',
    },
    widgets={
        'ingredient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient Name'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit'})
    }
)

InstructionFormset = modelformset_factory(
    RecipeInstructions,
    fields=('instruction',),
    labels={
        'instruction': '',
    },
    widgets={
        'instruction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instruction'}),
    },
)
