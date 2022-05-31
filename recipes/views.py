from django.contrib.messages.context_processors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect

from .models import Recipe


def index(request):
    latest_recipes_list = Recipe.objects.filter(author_id=request.user).order_by('-pub_date')[:10]
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
