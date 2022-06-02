from django.contrib.messages.context_processors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect

from .models import Recipe
from .forms import RecipeForm

class RecipeEditView(UpdateView):
    model = Recipe
    form_class = RecipeEditMultiForm
    success_url = reverse_lazy('recipe:index')

    # def get_form_kwargs(self):
    #     kwargs = super(RecipeEditView, self).get_form_kwargs()
    #     kwargs.update(instance={
    #         'recipe': self.object,
    #         'instructions': self.object.profile,
    #     })
    #     return kwargs

def edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    form = RecipeEditMultiForm(request.POST or None, instance=recipe)
    context = {'recipe': recipe, 'form': form}
    if form.is_valid():
        form.save()
        return redirect('recipes:index')
    return render(request, 'recipes/edit.html', context)


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
