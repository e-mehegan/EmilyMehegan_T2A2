# Imports for this file
from flask import Blueprint, request
from init import db
from models.user import User
from models.category import Category, category_schema, categories_schema
from flask_jwt_extended import get_jwt_identity, jwt_required


def authorise_admin():
    """
    Check if the current user is an admin.

    This function checks if the current user, identified by the JWT token,
    is the admin. It retrieves the user from the database based on
    the user ID from the JWT token. It returns a boolean value
    indicating whether the user is an admin.

    Parameters:
        None.

    Returns:
        bool: True if the current user is an admin, False otherwise.
    """
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin


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
    

@category_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    """
    Route for creating a new category.

    This function allows adminis to create a new category by extracting the category data from the request JSON
    and adding it to the database.

    Returns:
        dict: A dictionary containing the details of the newly created category if successful.

    Raises:
        403 Forbidden: If the user making the request is not an admin, an error message is returned.
    """
    json_data = category_schema.load(request.get_json())
    is_admin = authorise_admin()
    if not is_admin:
        return {'Error': 'You must be an admin to create a new category.'}, 403

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
def delete_one_category(id):
    """
    Route for deleting a category by ID.

    This function allows adminis to delete a category from the database based on the provided ID.

    Args:
        id (int): The ID of the category to be deleted.

    Returns:
        dict: A dictionary containing the result of the operation.
              If the category is successfully deleted, it returns a message confirming the deletion.

    Raises:
        403 Forbidden: If the user making the request is not an admin, an error message is returned.
        404 Not Found: If the category with the given ID does not exist, an error message is returned.
    """
    # Check authorization, if not admin return an error
    admin_status = authorise_admin()
    if not admin_status:
        return {'Error': 'You must be an admin to delete a category.'}

    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)

    if category:
        db.session.delete(category)
        db.session.commit()
        return {'Message': f'Category {category} has been deleted successfully.'}
    else: 
        return {'Error': f'Category with the id {id} does not exist.'}, 404
    

@category_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_category(id):
    """
    Route for updating a category by ID.

    This function allows adminis to update a category's information in the database based on the provided ID.

    Args:
        id (int): The ID of the category to be updated.

    Returns:
        dict: A dictionary containing the updated information of the category if successful.

    Raises:
        403 Forbidden: If the user making the request is not an admin, an error message is returned.
        404 Not Found: If the category with the given ID does not exist, an error message is returned.

    Note:
        The function expects the updated category information in the request JSON, and it performs a partial update.
        If a field is not provided in the request JSON, the existing value in the database for that field will be retained.
    """
    json_data = category_schema.load(request.get_json(), partial=True)
    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)

    # Check authorization, if not admin return an error
    if category:
        is_admin = authorise_admin()
        if not is_admin:
            return {'Error': 'You must be an admin to edit any categories.'}, 403

        # Update category fields if provided, otherwise keep the existing values from database
        category.category = json_data.get('category', category.category)

        db.session.commit()
        # Return the updated category as JSON with HTTP status code 200 (OK), if id doesn't exist return error
        return category_schema.dump(category)
    else:
        return {'Error': f'Category with id {id} does not exist.'}, 404
