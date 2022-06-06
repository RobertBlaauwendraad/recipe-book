from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    # e.g. /recipes/
    path('', views.index, name='index'),
    # e.g. /recipes/5/
    path('<int:recipe_id>/', views.detail, name='detail'),
    # path('update/<int:recipe_id>', views.update),
    # e.g. /recipes/delete/5
    path('delete/<int:recipe_id>', views.delete, name='delete'),
    # e.g. /recipes/edit/5
    path('edit/<int:recipe_id>', views.edit, name='edit'),
    # e.g. /recipes/add
    path('create/', views.create, name='create'),
    path('search/', views.search, name='search')
]
