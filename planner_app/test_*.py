import pytest
from django.urls import reverse
from planner_app.models import Recipe, Plan

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
def test_AddPlan(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    client.login(username='testuser', password='testpass')

    data = {
        'name': 'Test Plan',
        'description': 'Test Plan Description',
        'recipes': []
    }

    response = client.post(reverse('add-plan'), data=data, follow=True)

    assert response.status_code == 200
    assert Plan.objects.count() == 1
    assert Plan.objects.first().name == 'Test Plan'
    assert Plan.objects.first().description == 'Test Plan Description'


