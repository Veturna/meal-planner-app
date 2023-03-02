from django.test import TestCase, Client
import pytest

@pytest.fixture
def client():
    client = Client()
    return client


def test_main_page(client):
    response = client.get('')
    assert response.status_code == 200


def test_about_app(client):
    response = client.get('about/')
    assert response.status_code == response

