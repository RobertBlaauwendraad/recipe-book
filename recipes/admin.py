from django.contrib import admin

from .models import Recipe, RecipeIngredients, RecipeInstructions



class RecipeIngredient(admin.TabularInline):
    model = RecipeIngredients
    extra = 0
    verbose_name_plural = "Ingredients"


class RecipeInstruction(admin.TabularInline):
    model = RecipeInstructions
    extra = 0
    verbose_name_plural = "Instructions"



class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['recipe_name']}),
        ('Information', {'fields': ['description', 'people', 'pub_date', ]}),
    ]
    inlines = [RecipeIngredient, RecipeInstruction]

    list_display = ('recipe_name', 'description', 'people', 'pub_date')
admin.site.register(Recipe, RecipeAdmin)
