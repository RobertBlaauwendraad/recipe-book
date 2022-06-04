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
            'recipe_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Recipe Name'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}),
            'people': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Servings'}),
            }

class IngredientsForm(ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ('ingredient_name', 'quantity', 'unit')
        labels = {
            'ingredient_name': '',
            'quantity': '',
            'unit': '',
            }
        widgets = {
            'ingredient_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingredient Name'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Quantity'}),
            'unit': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Unit'})
            }

IngredientFormset = modelformset_factory(
    RecipeIngredients,
    form=IngredientsForm,
    extra=-3,
    )



class InstructionForm(ModelForm):
    class Meta:
        model = RecipeInstructions
        fields = ('instruction',)
        labels = {
            'instruction': '',
            }
        widgets = {
            'instruction': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instruction'}),
            }


InstructionFormset = modelformset_factory(
    RecipeInstructions,
    form=InstructionForm,
    extra=-5,
    )

