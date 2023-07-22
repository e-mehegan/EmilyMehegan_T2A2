# Imports for this file
from flask import Blueprint, request
from init import db
from models.user import User
from models.content import Content, content_schema, contents_schema
from models.author import Author
from models.category import Category
from flask_jwt_extended import get_jwt_identity, jwt_required


def authorise_admin():
    """
    Check if the current user is an admin.

    This function checks if the current user, identified by the JWT token,
    is the admin. It retrieves the user from the database based on
    the user ID from the JWT token. It returns a boolean value
    indicating whether the user is an admin.

    Returns:
        bool: True if the current user is an admin, False otherwise.
    """
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin


# Blueprint for content routes
content_bp = Blueprint('content', __name__, url_prefix='/content')

@content_bp.route('/')
def get_all_content():
    """
    Route for retrieving all content.

    This route retrieves a list of all content from the database and returns it as JSON.

    Returns:
        A list of all content as JSON objects with HTTP status code 200 (OK).
    """
    stmt = db.select(Content).order_by(Content.id.desc())
    contents = db.session.scalars(stmt)
    return contents_schema.dump(contents)


@content_bp.route('/<int:id>')
def get_one_content(id):
    """
    Route for retrieving a single piece of content by the ID.

    This route retrieves a single piece of content from the database based on the provided ID and returns it as JSON.

    Parameters:
        id (int): The ID of the content to retrieve.

    Returns:
        The content data as a JSON object with HTTP status code 200 (OK) if the content is found.
        An error message as a JSON object with HTTP status code 404 (Not Found) if the content is not found.
    """
    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalar(stmt)
    if content:
        return content_schema.dump(content)
    else:
        # Return an error message if the input ID is not found
        return {'Error': f'Content not found with the id {id}'}, 404
    

@content_bp.route('/', methods=['POST'])
@jwt_required()
def create_content():
    """
    Route for creating new content.

    This route allows authorized admins to create new content by providing
    details such as title, genre, description, published date, publisher, 
    category ID, and author ID.

    Returns:
        The created content as a JSON object with HTTP status code 201 (Created) 
        if the current user is an admin and the content is successfully created.

        An error message as a JSON object with HTTP status code 403 (Forbidden) 
        if the current user is not an admin.

        An error message as a JSON object with HTTP status code 400 (Bad Request) 
        if the request JSON is missing required fields or contains invalid category or author IDs.
    """
    json_data = content_schema.load(request.get_json())
    is_admin = authorise_admin()
    if not is_admin:
        return {'Error': 'You must be an admin to create content.'}, 403

    # Extract content data from the request JSON
    title = json_data.get('title')
    genre = json_data.get('genre')
    description = json_data.get('description')
    published = json_data.get('published')
    publisher = json_data.get('publisher')

    category_id = json_data.get('category_id')
    author_id = json_data.get('author_id')
    # Check if both category_id and author_id are provided, if not return an error
    if not category_id or not author_id:
        return {'Error': 'Both category_id and author_id must be provided when creating content.'}, 400

    # Retrieve the category and author objects based on the provided IDs
    category = db.session.query(Category).get(category_id)
    author = db.session.query(Author).get(author_id)

    # Check if the category and author exist in the database, if not return an error
    if not category:
        return {'Error': f'Category with id {category_id} does not exist.'}, 400
    if not author:
        return {'Error': f'Author with id {author_id} does not exist.'}, 400

    # Create new Content object with provided data
    content = Content(
        title=title,
        category_id=category_id,
        author_id=author_id,
        genre=genre,
        description=description,
        published=published,
        publisher=publisher,
    )

    # Add the content to the database and commit the changes
    db.session.add(content)
    db.session.commit()
    return content_schema.dump(content), 201


@content_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_content(id):
    """
    Route for deleting a single content item by ID.

    This route allows authorized admins to delete a content item based on` ID.

    Parameters:
        id (int): The ID of the content item to be deleted.

    Returns:
        A success message as a JSON object with HTTP status code 200 (OK) if the 
        content item is found and successfully deleted.

        An error message as a JSON object with HTTP status code 403 (Forbidden) 
        if the current user is not an admin.

        An error message as a JSON object with HTTP status code 404 (Not Found) 
        if the content item with the specified ID does not exist.
    """
    # Check authorization, if not admin return an error
    admin_status = authorise_admin()
    if not admin_status:
        return {'Error': 'You must be an admin to delete content.'}

    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalar(stmt)

    # If content item exists, delete it from the database and commit the changes, if not return error message
    if content:
        db.session.delete(content)
        db.session.commit()
        return {'Message': f'Content {content.title} has been deleted successfully.'}
    else: 
        return {'Error': f'Content with the id {id} does not exist.'}, 404


@content_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_content(id):
    """
    Route for updating a single content item by its ID.

    This route allows authorized admins to update the details of a content item 
    based on ID. The content can be partially updated by providing only the 
    fields to be changed in the request JSON.

    Parameters:
        id (int): The ID of the content item to be updated.

    Returns:
        The updated content as a JSON object with HTTP status code 200 (OK) if the 
        content item is found and successfully updated.

        An error message as a JSON object with HTTP status code 403 (Forbidden) 
        if the current user is not an admin.

        An error message as a JSON object with HTTP status code 404 (Not Found) 
        if the content item with the specified ID does not exist.

        An error message as a JSON object with HTTP status code 400 (Bad Request) 
        if the provided category or author IDs are invalid.
    """
    json_data = content_schema.load(request.get_json(), partial=True)
    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalar(stmt)

    # Check authorization, if not admin return an error
    if content:
        is_admin = authorise_admin()
        if not is_admin:
            return {'Error': 'You must be an admin to edit any content.'}, 403

        # Update content fields if provided, otherwise keep the existing values from database
        content.title = json_data.get('title', content.title)
        content.genre = json_data.get('genre', content.genre)
        content.description = json_data.get('description', content.description)
        content.published = json_data.get('published', content.published)

        # Update category and author IDs if provided, and ensure they exist in the database, if not return error
        category_id = json_data.get('category_id', content.category_id)
        author_id = json_data.get('author_id', content.author_id)
        category = db.session.query(Category).get(category_id)
        author = db.session.query(Author).get(author_id)
        if not category:
            return {'Error': f'Category with id {category_id} does not exist.'}, 400
        if not author:
            return {'Error': f'Author with id {author_id} does not exist.'}, 400

        # Assign updated category and author objects to the content
        content.category = category
        content.author = author

        db.session.commit()
        # Return the updated content as JSON with HTTP status code 200 (OK), if id doesn't exist return error
        return content_schema.dump(content)
    else:
        return {'Error': f'Content with id {id} does not exist.'}, 404

