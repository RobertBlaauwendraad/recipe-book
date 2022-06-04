from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Recipe
import datetime


def index(request):
    latest_recipes_list = Recipe.objects.order_by('-pub_date')[:10]
    context = {
        'latest_recipes_list': latest_recipes_list
    }
    return render(request, 'recipes/index.html', context)


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/detail.html', {'recipe': recipe})


## voeg dit toe

from . forms import RecipeForm, IngredientFormset, InstructionFormset

def add_recipe(request):

    submitted = False
    if request.method == "POST":
        formA = RecipeForm(request.POST)
        formB = IngredientFormset(request.POST)
        formC = InstructionFormset(request.POST)
        if formA.is_valid() and formB.is_valid() and formC.is_valid():
            a =formA.save(commit=False)
            a.pub_date = str(datetime.datetime.today()).split('.')[0]
            a.save()

            for b in formB:
                ingredient = b.save(commit=False)
                ingredient.recipe = a
                ingredient.save()

            i=1
            for c in formC:
                Instruction = c.save(commit=False)
                Instruction.recipe = a
                Instruction.step = i
                i+=1
                Instruction.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        formA = RecipeForm
        formB = IngredientFormset
        formC = InstructionFormset
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'recipes/add_recipe.html',{'formA':formA, 'formB':formB, 'formC':formC, 'submitted':submitted})