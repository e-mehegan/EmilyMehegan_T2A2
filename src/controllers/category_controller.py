# Imports for this file
from flask import Blueprint, request
from init import db
from models.user import User
from models.category import Category, category_schema, categories_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

# Blueprint for category routes
category_bp = Blueprint('category', __name__, url_prefix='/category')

@category_bp.route('/')
def get_all_categories():
    """
    Route for retrieving all categories.

    This route retrieves a list of all categories from the database and returns it as JSON.

    Parameters:
        None

    Returns:
        A list of all categories as JSON objects with HTTP status code 200 (OK).
    """
    stmt = db.select(Category).order_by(Category.id.desc())
    categories = db.session.scalars(stmt)
    return categories_schema.dump(categories)

@category_bp.route('/<int:id>')
def get_one_category(id):
    """
    Route for retrieving a single category by the ID.

    This route retrieves a single category from the database based on the provided ID and returns it as JSON.

    Parameters:
        id (int): The ID of the category to retrieve.

    Returns:
        The category data as a JSON object with HTTP status code 200 (OK) if the category is found.
        An error message as a JSON object with HTTP status code 404 (Not Found) if the category is not found.
    """
    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)
    if category:
        return category_schema.dump(category)
    else:
        # Return an error message if the input ID is not found
        return {'Error': f'Category not found with the id {id}'}, 404
    

