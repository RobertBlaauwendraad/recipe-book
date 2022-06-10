from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Recipe, RecipeIngredients, RecipeInstructions

from .forms import RecipeForm, IngredientFormset, InstructionFormset
import datetime


# Search only the user's recipes.
def search(request):
    return search_helper(request, False)


# Search the entire recipe database.
def search_all(request):
    return search_helper(request, True)


# Render a list of recipes based on a search query and whether the user is logged in or not.
def search_helper(request, search_all):
    if request.method == "POST":
        searched = request.POST['searched']
        if search_all:
            # Return the results based on whether the recipe name contains the searched string
            results = Recipe.objects.filter(recipe_name__contains=searched)
            return render(request, 'recipes/search-all.html',
                          {'searched': searched, 'results': results, 'search_all': search_all})
        elif request.user.is_authenticated:
            # If user is authenticated, return only for the current user and the searched string
            results = Recipe.objects.filter(author_id=request.user, recipe_name__contains=searched)
            return render(request, 'recipes/search.html',
                          {'searched': searched, 'results': results, 'search_all': search_all})
    if search_all:
        # Render the page in which you can search the entire recipe database
        return render(request, 'recipes/search-all.html', {})
    return render(request, 'recipes/search.html', {})


# Edit recipe with recipe_id
def edit(request, recipe_id):
    # Get current recipe or render 404 if it doesn't exist
    current_recipe = get_object_or_404(Recipe, pk=recipe_id)
    # Create forms initiated with the current recipe
    recipe_form = RecipeForm(request.POST or None, instance=current_recipe)
    ingredient_formset = IngredientFormset(request.POST or None,
                                           queryset=RecipeIngredients.objects.filter(recipe_id=current_recipe.id),
                                           prefix='ingredient-form')
    instruction_formset = InstructionFormset(request.POST or None,
                                             queryset=RecipeInstructions.objects.filter(recipe_id=current_recipe.id),
                                             prefix='instruction-form')

    # Check whether all forms are filled in valid
    if recipe_form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
        # Save recipe with ingredients and instructions related
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


# Render only recipes which are authored by the requesting user
def index(request):
    return index_helper(request, False)


# Render all recipes in the database
def index_all(request):
    return index_helper(request, True)


# Return recipes of all users when list_all is True.
# If list_all is False but the user logged in then return only the users recipes.
# In any other case return no recipes
def index_helper(request, list_all):
    max_size = 30  # Determines the maximum number of recipes to be returned
    # Either return the recipes for current user or for all users.
    if list_all:
        latest_recipes_list = Recipe.objects.all().order_by('-pub_date')[:max_size]
    elif request.user.is_authenticated:
        latest_recipes_list = Recipe.objects.filter(author_id=request.user).order_by('-pub_date')[:max_size]
    else:
        latest_recipes_list = {}
    context = {
        'latest_recipes_list': latest_recipes_list
    }
    if list_all:
        # Render the page in which you can search the entire recipe database
        return render(request, 'recipes/index-all.html', context)
    return render(request, 'recipes/index.html', context)


# Render all the details of the recipe with recipe_id
def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ordered_instructions_list = recipe.instructions.order_by('step')
    context = {
        'recipe': recipe,
        'ordered_instructions_list': ordered_instructions_list
    }
    return render(request, 'recipes/detail.html', context)


# Delete the recipe with recipe_id
def delete(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    return redirect('recipes:index')


# Render the page that allows a user to create a new recipe
def create(request):
    if request.method == 'GET':
        # We don't want to display the already saved model instances
        recipe_form = RecipeForm(request.GET or None)
        ingredient_formset = IngredientFormset(queryset=RecipeIngredients.objects.none(), prefix='ingredient-form')
        instruction_formset = InstructionFormset(queryset=RecipeInstructions.objects.none(), prefix='instruction-form')
    elif request.method == "POST":
        # Initiate new forms
        recipe_form = RecipeForm(request.POST)
        ingredient_formset = IngredientFormset(request.POST, prefix='ingredient-form')
        instruction_formset = InstructionFormset(request.POST, prefix='instruction-form')

        # If forms are valid save them
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
