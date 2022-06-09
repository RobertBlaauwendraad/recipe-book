from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Recipe, RecipeIngredients, RecipeInstructions

from .forms import RecipeForm, IngredientFormset, InstructionFormset
import datetime


def search(request):
    if request.method == "POST" and request.user.is_authenticated:
        searched = request.POST['searched']
        results = Recipe.objects.filter(author_id=request.user, recipe_name__contains=searched)
        return render(request, 'recipes/search.html',
                      {'searched': searched, 'results': results})
    else:
        return render(request, 'recipes/search.html', {})


def search_all(request):
    return search_helper(request, True)


def search_helper(request, search_all):
    if request.method == "POST" and request.user.is_authenticated:
        searched = request.POST['searched']
        if search_all:
            results = Recipe.objects.filter(recipe_name__contains=searched)
        else:
            results = Recipe.objects.filter(author_id=request.user, recipe_name__contains=searched)
        return render(request, 'recipes/search.html',
                      {'searched': searched, 'results': results, 'search_all': search_all})
    else:
        return render(request, 'recipes/search.html', {})


def edit(request, recipe_id):
    current_recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_form = RecipeForm(request.POST or None, instance=current_recipe)
    ingredient_formset = IngredientFormset(request.POST or None,
                                           queryset=RecipeIngredients.objects.filter(recipe_id=current_recipe.id),
                                           prefix='ingredient-form')
    instruction_formset = InstructionFormset(request.POST or None,
                                             queryset=RecipeInstructions.objects.filter(recipe_id=current_recipe.id),
                                             prefix='instruction-form')

    if recipe_form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
        recipe = recipe_form.save()
        for ingredient_form in ingredient_formset:
            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
        step = 1
        for instruction_form in instruction_formset:
            instruction = instruction_form.save(commit=False)
            instruction.recipe = recipe
            instruction.step = step
            instruction.save()
            step += 1
        return redirect('recipes:detail', current_recipe.id)

    context = {
        'recipe': current_recipe,
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset
    }
    return render(request, 'recipes/edit.html', context)


def index(request):
    return index_helper(request, False)


def index_all(request):
    return index_helper(request, True)


def index_helper(request, list_all):
    """Return recipes of all user when list_all is True. If list_all is False but the user logged
       in then return only the users recipes. And in any other case return no recipes."""
    if list_all:
        latest_recipes_list = Recipe.objects.all().order_by('-pub_date')[:30]
    elif request.user.is_authenticated:
        latest_recipes_list = Recipe.objects.filter(author_id=request.user).order_by('-pub_date')[:10]
    else:
        latest_recipes_list = {}
    context = {
        'latest_recipes_list': latest_recipes_list
    }
    if list_all:
        return render(request, 'recipes/index-all.html', context)
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
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        recipe_form = RecipeForm(request.GET or None)
        ingredient_formset = IngredientFormset(queryset=RecipeIngredients.objects.none(), prefix='ingredient-form')
        instruction_formset = InstructionFormset(queryset=RecipeInstructions.objects.none(), prefix='instruction-form')
    elif request.method == "POST":
        recipe_form = RecipeForm(request.POST)
        ingredient_formset = IngredientFormset(request.POST, prefix='ingredient-form')
        instruction_formset = InstructionFormset(request.POST, prefix='instruction-form')

        if recipe_form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.pub_date = str(datetime.datetime.today()).split('.')[0]
            recipe.author = request.user
            recipe.save()
            for ingredient_form in ingredient_formset:
                ingredient = ingredient_form.save(commit=False)
                ingredient.recipe = recipe
                ingredient.save()
            step = 1
            for instruction_form in instruction_formset:
                instruction = instruction_form.save(commit=False)
                instruction.recipe = recipe
                instruction.step = step
                instruction.save()
                step += 1
            return redirect('recipes:detail', recipe.id)
    context = {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset
    }
    return render(request, 'recipes/create.html', context)
