import pytest
from django.urls import reverse
from django.test import Client
from planner_app.models import Recipe

@pytest.mark.django_db
def test_MainPage(client):
    response = client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
def test_AboutApp(client):
    response = client.get('/about/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_RecipesView(client):
    client.login(username='daria', password='Filofilo971211!')
    response = client.get('/recipes/')
    assert response.status_code == 200
    assert 'recipes' in response.context
    assert all(isinstance(recipe, Recipe) for recipe in response.context['recipes'])


@pytest.mark.django_db
def test_RecipeDetail(client):
    recipe = Recipe.objects.create(name='test', description='recipe', preparation='test')
    client.login(username='daria', password='Filofilo971211!')
    response = client.get(reverse('recipe-detail', args=[recipe.pk]))
    assert response.status_code == 200
    assert Recipe.objects.get(pk=recipe.pk).name == 'test'
    assert Recipe.objects.get(pk=recipe.pk).description == 'recipe'
    assert Recipe.objects.get(pk=recipe.pk).preparation == 'test'


@pytest.mark.django_db
def test_EditRecipe(client):
    recipe = Recipe.objects.create(name='test', description='recipe', preparation='test')
    client.login(username='daria', password='Filofilo971211!')
    response = client.get(reverse('edit-recipe', args=[recipe.pk]))
    assert response.status_code == 200

    data = {'name': 'new recipe name', 'description': 'new recipe description', 'preparation': 'new recipe preparation'}
    response = client.post(reverse('edit-recipe', args=[recipe.pk]), data)
    assert response.status_code == 302
    assert Recipe.objects.get(pk=recipe.pk).name == 'new recipe name'
    assert Recipe.objects.get(pk=recipe.pk).description == 'new recipe description'
    assert Recipe.objects.get(pk=recipe.pk).preparation == 'new recipe preparation'


@pytest.mark.django_db