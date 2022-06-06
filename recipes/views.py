from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Recipe
from .forms import RecipeForm, IngredientFormset, InstructionFormset
import datetime


def index(request):
    if request.user.is_authenticated:
        latest_recipes_list = Recipe.objects.filter(author_id=request.user).order_by('-pub_date')[:10]
    else:
        latest_recipes_list = {}
    context = {
        'latest_recipes_list': latest_recipes_list
    }
    return render(request, 'recipes/index.html', context)


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ordered_instructions_list = recipe.instructions.order_by('step')
    context = {
        'recipe': recipe,
        'ordered_instructions_list': ordered_instructions_list
    }
    return render(request, 'recipes/detail.html', context)


def delete(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    return redirect('recipes:index')


def create(request):
    submitted = False
    if request.method == "POST":
        formA = RecipeForm(request.POST)
        formB = IngredientFormset(request.POST)
        formC = InstructionFormset(request.POST)
        if formA.is_valid() and formB.is_valid() and formC.is_valid():
            a = formA.save(commit=False)
            a.pub_date = str(datetime.datetime.today()).split('.')[0]
            a.author = request.user.id
            a.save()

            for b in formB:
                ingredient = b.save(commit=False)
                ingredient.recipe = a
                ingredient.save()

            i = 1
            for c in formC:
                Instruction = c.save(commit=False)
                Instruction.recipe = a
                Instruction.step = i
                i += 1
                Instruction.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        formA = RecipeForm
        formB = IngredientFormset
        formC = InstructionFormset
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'recipes/create.html',
                  {'formA': formA, 'formB': formB, 'formC': formC, 'submitted': submitted})
