from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    # e.g. /recipes/
    path('', views.index, name='index'),
    # e.g. /recipes/5/
    path('<int:recipe_id>/', views.detail, name='detail'),
    path('add_recipe/', views.add_recipe, name='add-recipe') #deze is nieuw
]
