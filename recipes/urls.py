from django.urls import path
from . import views


urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/add/', views.recipe_add, name='recipe_add'),
    path('recipe/<int:id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
]