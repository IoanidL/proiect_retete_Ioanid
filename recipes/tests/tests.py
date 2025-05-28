import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from recipes.models import Recipe
from django.utils import timezone

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")

@pytest.fixture
def client_logged_in(client, user):
    client.login(username="testuser", password="testpass123")
    return client

@pytest.mark.django_db
def test_create_recipe(client_logged_in, user): # creates 1 item in recipe list, recipe has asserted title and user
    response = client_logged_in.post(reverse('recipe_add'), {
        'title': 'Titlu',
        'description': 'Reteta test',
        'prep_time': 10,
        'cooking_time': 30
    })
    assert Recipe.objects.count() == 1
    recipe = Recipe.objects.first()
    assert recipe.title == 'Titlu'
    assert recipe.user == user

@pytest.mark.django_db
def test_edit_recipe(client_logged_in, user): # edited recipe has asserted title and description
    recipe = Recipe.objects.create(
        title='Titlu',
        description='Reteta',
        prep_time='5',
        cooking_time='20',
        user=user
    )
    response = client_logged_in.post(reverse('recipe_edit', args=[recipe.id]), {
        'title': 'Titlu1',
        'description': 'Reteta1',
        'prep_time': '5',
        'cooking_time': '25'
    })
    recipe.refresh_from_db()
    assert recipe.title == 'Titlu1'
    assert recipe.description == 'Reteta1'

@pytest.mark.django_db
def test_delete_recipe(client_logged_in, user): # after deletion of created recipe, the recipe list has no items
    recipe = Recipe.objects.create(
        title='Titlu',
        description='Reteta',
        prep_time='5',
        cooking_time='10',
        user=user
    )
    response = client_logged_in.post(reverse('recipe_delete', args=[recipe.id]))
    assert Recipe.objects.count() == 0

@pytest.mark.django_db
def test_view_recipe_detail(client_logged_in, user): # request for recipe detail is successfull, recipe has asserted description
    recipe = Recipe.objects.create(
        title='Titlu',
        description='Reteta',
        prep_time='10',
        cooking_time='40',
        user=user
    )
    response = client_logged_in.get(reverse('recipe_detail', args=[recipe.id]))
    assert response.status_code == 200
    assert 'Reteta' in response.content.decode()

@pytest.mark.django_db
def test_recipe_list_sorting(client_logged_in, user): # first title's sorted first letter is alphabetically before second one's
    Recipe.objects.create(title='Paine', description='Calda', prep_time= '10', cooking_time='45', user=user)
    Recipe.objects.create(title='Branza', description='Rece', prep_time= '5', cooking_time='30', user=user)
    response = client_logged_in.get(reverse('recipe_list') + '?sort=alpha')
    content = response.content.decode()
    assert content.index('Branza') < content.index('Paine')

@pytest.mark.django_db
def test_recipe_model_fields(client_logged_in, user): # model fields are filled correctly
    recipe = Recipe.objects.create(
        title="Titlu",
        description="Description",
        prep_time=20,
        cooking_time=40,
        user=user,
        addition_date=timezone.now()
    )
    assert recipe.user == user
    assert recipe.title == "Titlu"
    assert recipe.description == "Description"
    assert recipe.prep_time == 20
    assert recipe.cooking_time == 40
    assert recipe.total_time() == 60
    assert isinstance(recipe.addition_date, timezone.datetime)
