import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpass123')

@pytest.mark.django_db
def test_login_success(client, test_user):  # successfull login redirects to home page
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.url == '/'

@pytest.mark.django_db
def test_protected_view_redirects_for_unauthenticated_user(client): # unauthenticated user recipe_add redirects to log in request
    url = reverse('recipe_add')
    response = client.get(url)
    login_url = reverse('login')
    assert response.url.startswith(f"{login_url}?next={url}")

@pytest.mark.django_db
def test_protected_view_access_for_authenticated_user(client, test_user): # request for recipe_add is successfull for authenticated user
    client.login(username='testuser', password='testpass123')
    response = client.get(reverse('recipe_add'))
    assert response.status_code == 200