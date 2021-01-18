from flask import request, jsonify, send_from_directory
from flasgger import swag_from
from http import HTTPStatus
from post_service.app import app
from marshmallow.exceptions import ValidationError

from post_service.schemas.schmas import (
    RecipeSchema, 
    StorySchema,
    CategorySchema,
    TagSchema,
)

from post_service.config.base import MEDIA_ROOT
from post_service.utils.common import save_file

from post_service.models import (
    Recipe, 
    Story,
    Category,
    Tag,
)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(MEDIA_ROOT, filename)

# gettiing and post recipes
@app.route('/recipes/', methods=['GET', 'POST'])
@swag_from('docs/recipes/get_all_recipes.yml', methods=['GET',])
@swag_from('docs/recipes/post_recipe.yml', methods=['POST',])
def recipes():
    if request.method == 'POST':
        try:
            data = request.json or request.form
            # print(data)
            image = request.files.get('image')
            serializer = RecipeSchema()
            recipe = serializer.load(data)
            recipe.owner_id = 1
            recipe.image = save_file(image)
            recipe.save()
            return RecipeSchema().jsonify(recipe), HTTPStatus.CREATED
        except ValidationError as err:
            return jsonify(err.messages), HTTPStatus.BAD_REQUEST
    # else
    recipes = Recipe.query.filter_by(is_published=True)
    return RecipeSchema(many=True).jsonify(recipes), HTTPStatus.OK


@app.route('/recipes/<int:recipe_id>/', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@swag_from('docs/recipes/get_recipe_id.yml', methods=['GET',])
@swag_from('docs/recipes/put_recipe_id.yml', methods=['PUT'])
@swag_from('docs/recipes/delete_recipe_id.yml', methods=['DELETE'])
@swag_from('docs/recipes/patch_recipe_id.yml', methods=['PATCH'])
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({'message': 'Not found'}), HTTPStatus.NOT_FOUND
    if request.method == 'DELETE':
        recipe.delete()
        return jsonify({}), HTTPStatus.NO_CONTENT
    if request.method == 'GET':
        return RecipeSchema().jsonify(recipe), HTTPStatus.OK
    try:
        data = request.json or request.form
        image = request.files.get('image')
        serializer = RecipeSchema()
        if request.method == 'PUT':
            recipe_serializer = serializer.load(data, instance=recipe)
        elif request.method == 'PATCH':
            recipe_serializer = serializer.load(data, instance=recipe, partial=True)
        recipe.owner_id = 1
        if image:
            recipe.image = save_file(image)
        recipe_serializer.save()
        return RecipeSchema().jsonify(recipe), HTTPStatus.OK
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST


# gettiing and post stories
@app.route('/stories/', methods=['GET', 'POST'])
@swag_from('docs/stories/get_all_stories.yml', methods=['GET'])
@swag_from('docs/stories/post_story.yml', methods=['POST'])
def stories():
    if request.method == 'POST':
        try:
            data = request.json or request.form
            # print(data)
            image = request.files.get('image')
            serializer = StorySchema()
            story = serializer.load(data)
            story.owner_id = 1
            story.image = save_file(image)
            story.save()
            return StorySchema().jsonify(story), HTTPStatus.CREATED
        except ValidationError as err:
            return jsonify(err.messages), HTTPStatus.BAD_REQUEST
    # else
    stories = Story.query.filter_by(is_published=True)
    return StorySchema(many=True).jsonify(stories), HTTPStatus.OK

# getting story [id] 
@app.route('/stories/<int:story_id>/', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@swag_from('docs/stories/get_story_id.yml', methods=['GET'])
@swag_from('docs/stories/put_story_id.yml', methods=['PUT'])
@swag_from('docs/stories/patch_story_id.yml', methods=['PATCH'])
@swag_from('docs/stories/delete_story_id.yml', methods=['DELETE'])
def story(story_id):
    story = Story.query.filter_by(id=story_id).first()
    if not story:
        return jsonify({'message': 'Not found'}), HTTPStatus.NOT_FOUND
    if request.method == 'DELETE':
        story.delete()
        return jsonify({}), HTTPStatus.NO_CONTENT
    if request.method == 'GET':
        return StorySchema().jsonify(story), HTTPStatus.OK
    try:
        data = request.json or request.form
        image = request.files.get('image')
        serializer = StorySchema()
        if request.method == 'PUT':
            story_serializer = serializer.load(data, instance=story)
        elif request.method == 'PATCH':
            story_serializer = serializer.load(data, instance=story, partial=True)
        story.owner_id = 1
        if image:
            story.image = save_file(image)
        story_serializer.save()
        return StorySchema().jsonify(story), HTTPStatus.OK
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST



# getting and post categories
@app.route('/categories/', methods=["GET", "POST"])
@swag_from('docs/categories/get_all_categories.yml', methods=['GET'])
@swag_from('docs/categories/post_category.yml', methods=['POST'])
def categories():
    if request.method == 'POST':
        try:
            data = request.json or request.form
            serializer = CategorySchema()
            category = serializer.load(data)
            category.save()
            return CategorySchema().jsonify(category), HTTPStatus.CREATED
        except ValidationError as err:
            return jsonify(err.messages), HTTPStatus.BAD_REQUEST
    # else
    categories = Category.query.filter_by(is_published=True)
    return CategorySchema(many=True).jsonify(categories), HTTPStatus.OK


# getting category [id] 
@app.route('/categories/<int:category_id>/', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@swag_from('docs/categories/get_category_id.yml', methods=['GET'])
@swag_from('docs/categories/patch_category_id.yml', methods=['PATCH'])
@swag_from('docs/categories/put_category_id.yml', methods=['PUT'])
@swag_from('docs/categories/delete_category_id.yml', methods=['DELETE'])
def category(category_id):
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return jsonify({'message': 'Not found'}), HTTPStatus.NOT_FOUND
    if request.method == 'DELETE':
        category.delete()
        return jsonify({}), HTTPStatus.NO_CONTENT
    if request.method == 'GET':
        return CategorySchema().jsonify(category), HTTPStatus.OK
    try:
        data = request.json or request.form
        serializer = CategorySchema()
        if request.method == 'PUT':
            category_serializer = serializer.load(data, instance=category)
        elif request.method == 'PATCH':
            category_serializer = serializer.load(data, instance=category, partial=True)
        category_serializer.save()
        return CategorySchema().jsonify(category), HTTPStatus.OK
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST


# getting and post tags
@app.route('/tags/', methods=["GET", "POST"])
@swag_from('docs/tags/get_all_tags.yml', methods=['GET'])
@swag_from('docs/tags/post_tags.yml', methods=['POST'])
def tags():
    if request.method == "POST":
        try:
            data = request.json or request.form
            serializer = TagSchema()
            tag = serializer.load(data)
            tag.save()
            return TagSchema().jsonify(tag), HTTPStatus.CREATED
        except ValidationError as err:
            return jsonify(err.messages), HTTPStatus.BAD_REQUEST
    # else
    tags = Tag.query.all()
    return TagSchema(many=True).jsonify(tags), HTTPStatus.OK


# getting category [id] 
@app.route('/tags/<int:tag_id>/', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@swag_from('docs/tags/get_tag_id.yml', methods=['GET'])
@swag_from('docs/tags/patch_tag_id.yml', methods=['PATCH'])
@swag_from('docs/tags/put_tag_id.yml', methods=['PUT'])
@swag_from('docs/tags/delete_tag_id.yml', methods=['DELETE'])
def tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    if not tag:
        return jsonify({'message': 'Not found'}), HTTPStatus.NOT_FOUND
    if request.method == 'DELETE':
        tag.delete()
        return jsonify({}), HTTPStatus.NO_CONTENT
    if request.method == 'GET':
        return TagSchema().jsonify(tag), HTTPStatus.OK
    try:
        data = request.json or request.form
        serializer = TagSchema()
        if request.method == 'PUT':
            tag_serializer = serializer.load(data, instance=tag)
        elif request.method == 'PATCH':
            tag_serializer = serializer.load(data, instance=tag, partial=True)
        tag_serializer.save()
        return TagSchema().jsonify(tag), HTTPStatus.OK
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST
