from django.contrib import admin

from .models import Recipe, RecipeIngredients, RecipeInstructions


class RecipeIngredient(admin.TabularInline):
    model = RecipeIngredients
    extra = 1
    verbose_name_plural = "Ingredients"


class RecipeInstruction(admin.TabularInline):
    model = RecipeInstructions
    extra = 1
    verbose_name_plural = "Instructions"
    # exclude = ['step']


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['recipe_name']}),
        ('Information', {'fields': ['description', 'people', 'pub_date', 'author']}),
    ]
    inlines = [RecipeIngredient, RecipeInstruction]


admin.site.register(Recipe, RecipeAdmin)
