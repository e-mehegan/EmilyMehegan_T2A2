# Imports for the file
from flask import Blueprint, request
from init import db
from models.user import User
from models.author import Author, authors_schema, author_schema
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

# Blueprint for author routes
author_bp = Blueprint('author', __name__, url_prefix='/author')

@author_bp.route('/')
def get_all_authors():
    """
    Route for retrieving all authors.

    This route retrieves a list of all authors from the database and returns it as JSON.

    Parameters:
        None

    Returns:
        A list of all authors as JSON objects with HTTP status code 200 (OK).
    """
    stmt = db.select(Author).order_by(Author.id.desc())
    authors = db.session.scalars(stmt)
    return authors_schema.dump(authors)


@author_bp.route('/<int:id>')
def get_one_author(id):
    """
    Route for retrieving a single author by their ID.

    This route retrieves a single author from the database based on the provided ID and returns it as JSON.

    Parameters:
        id (int): The ID of the author to retrieve.

    Returns:
        The author data as a JSON object with HTTP status code 200 (OK) if the author is found.
        An error message as a JSON object with HTTP status code 404 (Not Found) if the author is not found.
    """
    stmt = db.select(Author).filter_by(id=id)
    author = db.session.scalar(stmt)
    if author:
        return author_schema.dump(author)
    else:
        # Return an error message if the input ID is not found
        return {'Error': f'Author not found with the id {id}'}, 404
    

@author_bp.route('/', methods=['POST'])
@jwt_required()
def create_author():
    """
    Route for creating a new author.

    This function creates a new author by extracting the author data from the request JSON
    and adding it to the database. Only adminis can create a new author.

    Returns:
        dict: A dictionary containing the details of the newly created author if successful.

    Raises:
        403 Forbidden: If the user making the request is not an admin, an error message is returned.
    """
    # Check authorization, if not admin return an error
    json_data = request.get_json()
    is_admin = authorise_admin()
    if not is_admin:
        return {'Error': 'You must be an admin to create a new author.'}, 403

    # Extract author data from the request JSON
    author = json_data.get('author')

    # Create new author object with provided data
    authors = Author(
        author=author
    )
    # Add the author to the database and commit the changes
    db.session.add(authors)
    db.session.commit()
    return author_schema.dump(authors), 201


@author_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_author(id):
    """
    Route for deleting one author by ID.

    This function allows adminis to delete an author from the database based on the provided ID.

    Args:
        id (int): The ID of the author to be deleted.

    Returns:
        dict: A dictionary containing the result of the operation.
              If the author is successfully deleted, it returns a message confirming the deletion.
              If the author with the given ID does not exist, it returns an error message with status 404.

    Raises:
        403 Forbidden: If the user making the request is not an admin, it raises an exception.
    """
    # Check authorization, if not admin return an error
    admin_status = authorise_admin()
    if not admin_status:
        return {'Error': 'You must be an admin to delete a author.'}

    stmt = db.select(Author).filter_by(id=id)
    author = db.session.scalar(stmt)

    if author:
        db.session.delete(author)
        db.session.commit()
        return {'Message': f'Author has been deleted successfully.'}
    else: 
        return {'Error': f'Author with the id {id} does not exist.'}, 404 
    

@author_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_author(id):
    """
    Route for updating an author by ID.

    This function allows adminis to update an author's information in the database based on the provided ID.

    Args:
        id (int): The ID of the author to be updated.

    Returns:
        dict: A dictionary containing the updated information of the author if successful.

    Raises:
        403 Forbidden: If the user making the request is not an admin, an error message is returned.
        404 Not Found: If the author with the given ID does not exist, an error message is returned.

    Note:
        The function expects the updated author information in the request JSON, and it performs a partial update.
        If a field is not provided in the request JSON, the existing value in the database for that field will be retained.
    """
    json_data = author_schema.load(request.get_json(), partial=True)
    stmt = db.select(Author).filter_by(id=id)
    author = db.session.scalar(stmt)

    # Check authorization, if not admin return an error
    if author:
        is_admin = authorise_admin()
        if not is_admin:
            return {'Error': 'You must be an admin to edit any authors.'}, 403

        # Update author fields if provided, otherwise keep the existing values from database
        author.author = json_data.get('author', author.author)

        db.session.commit()
        # Return the updated author as JSON with HTTP status code 200 (OK), if id doesn't exist return error
        return author_schema.dump(author)
    else:
        return {'Error': f'Author with id {id} does not exist.'}, 404