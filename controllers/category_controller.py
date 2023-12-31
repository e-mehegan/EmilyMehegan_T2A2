from flask import Blueprint, request
from init import db
from models.user import User
from models.category import Category, category_schema, categories_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.author_controller import authorise_admin


# Blueprint for category routes
category_bp = Blueprint('category', __name__, url_prefix='/category')


@category_bp.route('/')
def get_all_categories():
    """
    Route for retrieving all categories.

    This route retrieves a list of all categories from the database and returns it as JSON.

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
    

@category_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_admin
def create_category():
    """
    Route for creating a new category.

    This function allows adminis to create a new category by extracting the category data from the request JSON
    and adding it to the database.

    Returns:
        dict: Dictionary containing the details of the newly created category if successful.

    Raises:
        403 Forbidden: If the user making the request is not an admin, an error message occurs.
    """
    json_data = category_schema.load(request.get_json())

    # Extract category data from the request JSON
    category = json_data.get('category')

    # Create new category object with provided data
    categories = Category(
        category=category
    )

    # Add the category to the database and commit the changes
    db.session.add(categories)
    db.session.commit()
    return category_schema.dump(categories), 201


@category_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_admin
def delete_one_category(id):
    """
    Route for deleting a category by ID.

    This function allows adminis to delete a category from the database based on the provided ID.

    Args:
        id (int): The ID of the category to be deleted.

    Returns:
        dict: Dictionary containing the result of the operation.
              If the category is successfully deleted, it returns a message confirming the deletion.

    Raises:
        403 Forbidden: If the user making the request is not an admin, an error message occurs.
        404 Not Found: If the category with the given ID does not exist, an error message occurs.
    """
    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)

    if category:
        db.session.delete(category)
        db.session.commit()
        return {'Message': f'Category {category} has been deleted successfully.'}
    else: 
        # Return an error message if the input ID is not found
        return {'Error': f'Category with the id {id} does not exist.'}, 404
    

@category_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_admin
def update_one_category(id):
    """
    Route for updating a category by ID.

    This function allows adminis to update a category's information in the database based on the provided ID.

    Args:
        id (int): The ID of the category to be updated.

    Returns:
        dict: Dictionary containing updated information of the category if successful.

    Raises:
        403 Forbidden: If the user making the request is not an admin, an error message occurs.
        404 Not Found: If the category with the given ID does not exist, an error message occurs.
    """
    json_data = category_schema.load(request.get_json(), partial=True)
    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)

    if category:
        # Update category fields if provided, otherwise keep the existing values from database
        category.category = json_data.get('category', category.category)

        db.session.commit()
        # Return the updated category as JSON with HTTP status code 200 (OK), if id doesn't exist return error
        return category_schema.dump(category)
    else:
        return {'Error': f'Category with id {id} does not exist.'}, 404
