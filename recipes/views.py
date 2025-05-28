from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def recipe_list(request):
    sort_by = request.GET.get('sort', 'title')
    if sort_by == 'added':
        recipes = Recipe.objects.order_by('-addition_date')
    else:
        recipes = Recipe.objects.order_by('title')

    paginator = Paginator(recipes, 4 )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipe_list.html', {
        'page_obj': page_obj,
        'sort_by': sort_by
    })

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('my_recipes')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})

@login_required
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.user != request.user:
        return redirect('my_recipes')
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form})

@login_required
def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.user != recipe.user:
        return redirect('recipe_list')

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')

    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

@login_required
def my_recipes(request):
    sort_by = request.GET.get('sort', 'title')

    if sort_by == 'added':
        recipes = Recipe.objects.filter(user=request.user).order_by('-addition_date')
    else:
        recipes = Recipe.objects.filter(user=request.user).order_by('title')

    paginator = Paginator(recipes, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/my_recipes.html', {
        'page_obj': page_obj,
        'sort_by': sort_by
    })