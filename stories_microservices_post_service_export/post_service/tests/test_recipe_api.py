
from post_service.api.routers import recipe
from post_service.models import Recipe
import pytest



def test_get_recipes_status_code(app, client):
    response = client.get('/recipes/')
    assert response.status_code == 200


def test_get_recipe_id_status_code_OK(app, client):
    recipe = Recipe.query.filter_by(is_published=True)
    recipe_id = recipe[-1].id
    response = client.get(f'/recipes/{recipe_id}/')

    assert response.status_code == 200


def test_get_recipe_id(app, client):
    response = client.post('/recipes/')
    res_data = response.json
    
    assert res_data['category_id'] 
    assert res_data['title']
    assert res_data['description'] 
    assert res_data['short_description']
    assert res_data['slug']

    
def test_post_recipe_valid_data_status_code(app, client):
    post_data = {
        "category_id": 1,
        "description": "sdfnsdjfndsfjnsdlsflsdkfnsksldn",
        "short_description": "23423423789",
        "slug": "345345",
        "title": "345353534"
    }
    response = client.post('/recipes/', json=post_data)

    assert response.status_code == 201


def test_post_recipe_valid_data(app, client):
    post_data = {
        "category_id": 1,
        "description": "description",
        "short_description": "short_description",
        "slug": "slug",
        "title": "title"
    }
    response = client.post('/recipes/', json=post_data)
    res_data = response.json

    assert res_data['category_id'] == post_data['category_id']
    assert res_data['title'] == post_data['title']
    assert res_data['description'] == post_data['description']
    assert res_data['short_description'] == post_data['short_description']


def test_post_recipe_invalid_data_status_code(app, client):
    post_data = {
        "category_id": 1
    }
    response = client.post('/recipes/', json=post_data)

    assert response.status_code == 400


def test_post_recipe_invalid_data(app, client):
    post_data = {
        "category_id": 1
    }
    response = client.post('/recipes/', json=post_data)
    res_data = response.json

    assert "Missing data for required field." in res_data['description']
    assert "Missing data for required field." in res_data['short_description']
    assert "Missing data for required field." in res_data['slug']
    assert "Missing data for required field." in res_data['title']


def test_post_recipe_invalid_data_with_longer_title(app, client):
    post_data = {
        "title": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the "
                "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type "
                "and scrambled it to make a type specimen book. It has survived not only five centuries, "
                "but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised "
                "in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently "
                "with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. ",
        "slub": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the "
                "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type "
                "and scrambled it to make a type specimen book. It has survived not only five centuries, "
                "but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised "
                "in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently "
                "with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. ",
    }
    response = client.post('/recipes/', json=post_data)
    res_data = response.json

    assert "Longer than maximum length 80." in res_data['title']


def test_post_recipe_with_not_valid_type(app, client):
    post_data = {
        "category_id": "sasasasa",
        'title': 2525,
        'description': 2525,
        'short_description': 2525,
        'slug': 2525
    }
    response = client.post('/recipes/', json=post_data)
    res_data = response.json

    assert "Not a valid integer." in res_data['category_id']
    assert "Not a valid string." in res_data['title']
    assert "Not a valid string." in res_data['description']
    assert "Not a valid string." in res_data['short_description']
    assert "Not a valid string." in res_data['slug']


def test_get_recipe_with_wrong_id(app, client):
    recipe_id = 25259
    response = client.get(f'/recipes/{recipe_id}/')
    res_data = response.json

    print('res_data', res_data)

    assert "message" in res_data
    assert "Not found" in res_data['message']


def test_get_recipe_with_wrong_id_status_code(app, client):
    recipe_id = 25259

    response = client.get(f'/recipes/{recipe_id}/')
    assert response.status_code == 404


def test_delete_recipe_status_code_OK(app, client):
    recipe = Recipe.query.filter_by(is_published=True)
    recipe_id = recipe[-1].id

    response = client.delete(f'/recipes/{recipe_id}/')
    assert response.status_code == 204


def test_put_recipe_id_status_code_OK(app, client):
    recipe = Recipe.query.filter_by(is_published=True)
    recipe_id = recipe[-1].id

    post_data = {
        "category_id": 1,
        "description": "description",
        "short_description": "short_description",
        "slug": "slug",
        "title": "title"
    }
    response = client.put(f'/recipes/{recipe_id}/', json=post_data)
    assert response.status_code == 200


def test_put_recipe_id_valid_data(app, client):
    recipe = Recipe.query.filter_by(is_published=True)
    recipe_id = recipe[-1].id 

    post_data = {
        "category_id": 1,
        "description": "description",
        "short_description": "short_description",
        "slug": "slug",
        "title": "title"
    }
    response = client.put(f'/recipes/{recipe_id}/', json=post_data)
    res_data = response.json
    assert post_data['category_id'] == res_data['category_id']
    assert post_data['description'] == res_data['description']
    assert post_data['short_description'] == res_data['short_description']
    assert post_data['slug'] == res_data['slug']
    assert post_data['title'] == res_data['title']


def test_put_recipe_id_invalid_data(app, client):
    recipe = Recipe.query.filter_by(is_published=True)
    recipe_id = recipe[-1].id 

    post_data = {
        "category_id": 1,
    }

    response = client.put(f'/recipes/{recipe_id}/', json=post_data)
    res_data = response.json

    assert "Missing data for required field." in res_data['description']
    assert "Missing data for required field." in res_data['short_description']
    assert "Missing data for required field." in res_data['slug']
    assert "Missing data for required field." in res_data['title']


def test_patch_recipe_id_status_code_OK(app, client):
    recipe = Recipe.query.filter_by(is_published=True)
    recipe_id = recipe[-1].id 

    post_data = {
        "category_id": 1,
        "description": "description",
        "short_description": "short_description",
        "slug": "slug",
        "title": "title"
    }
    response = client.patch(f'/recipes/{recipe_id}/', json=post_data)
    assert response.status_code == 200

def test_patch_recipe_id_valid_data(app, client):
    recipe = Recipe.query.filter_by(is_published=True)
    recipe_id = recipe[-1].id
    print(recipe_id, 'sasasa')

    post_data = {
        "category_id": 1,
        "description": "description",
        "short_description": "short_description",
        "slug": "slug",
        "title": "title"
    }
    response = client.patch(f'/recipes/{recipe_id}/', json=post_data)
    res_data = response.json
    assert post_data['category_id'] == res_data['category_id']
    assert post_data['description'] == res_data['description']
    assert post_data['short_description'] == res_data['short_description']
    assert post_data['slug'] == res_data['slug']
    assert post_data['title'] == res_data['title']