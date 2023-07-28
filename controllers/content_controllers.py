from flask import Blueprint, request, jsonify
from init import db, ma
from models.content import Content, content_schema, contents_schema
from models.author import Author
from models.category import Category
from flask_jwt_extended import jwt_required
from controllers.author_controller import authorise_admin
from datetime import datetime


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
@authorise_admin
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

        An error message as a JSON object with HTTP status code 400 (Bad Request)
        if the request JSON has an invalid format for published date.
    """
    body_data = request.get_json()
    category_id = body_data.get('category_id')
    author_id = body_data.get('author_id')

    # Extract content data from the request JSON
    title = body_data.get('title')
    genre = body_data.get('genre')
    description = body_data.get('description')
    publisher = body_data.get('publisher')

    # Check if both category_id and author_id are provided, if not return an error
    if not category_id or not author_id:
        return {'Error': 'Both category_id and author_id must be provided when creating content.'}, 400

    # Retrieve the category and author objects based on the provided IDs
    category = Category.query.get(category_id)
    author = Author.query.get(author_id)

    if not category:
        return {'Error': f'Category with id {category_id} does not exist.'}, 400
    if not author:
        return {'Error': f'Author with id {author_id} does not exist.'}, 400

    # Extract and validate the 'published' date from the request JSON
    published_date_str = body_data.get('published')
    try:
        published_date = datetime.strptime(published_date_str, '%Y-%m-%d').date()
    except ValueError:
        return {'Error': 'Invalid date format for: published. Please provide the date in this format: YYYY-MM-DD.'}, 400

    # Create new Content object with provided data
    content = Content(
        title=title,
        category_id=category_id,
        author_id=author_id,
        genre=genre,
        description=description,
        published=published_date,
        publisher=publisher,
    )

    # Add the content to the database and commit the changes
    db.session.add(content)
    db.session.commit()
    return content_schema.dump(content), 201


@content_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_admin
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
@authorise_admin
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

        An error message as a JSON object with HTTP status code 400 (Bad Request)
        if no data is inputed by the admin.

        An error message as a JSON object with HTTP status code 403 (Forbidden) 
        if the current user is not an admin.

        An error message as a JSON object with HTTP status code 404 (Not Found) 
        if the content item with the specified ID does not exist.

        An error message as a JSON object with HTTP status code 400 (Bad Request) 
        if the provided category or author IDs are invalid.
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({'Error': 'No data provided in the request, please input data to update content!.'}), 400

    content_data = content_schema.load(json_data, partial=True)
    
    content = Content.query.get(id)
    if not content:
        return jsonify({'Error': f'Content with id {id} does not exist.'}), 404

    # Update content fields if provided, otherwise keep the existing values from the database
    content.title = content_data.get('title', content.title)
    content.genre = content_data.get('genre', content.genre)
    content.description = content_data.get('description', content.description)
    content.published = content_data.get('published', content.published)

    # Update category and author IDs if provided, and ensure they exist in the database, if not return an error
    category_id = content_data.get('category_id', content.category_id)
    author_id = content_data.get('author_id', content.author_id)

    category = Category.query.get(category_id)
    author = Author.query.get(author_id)

    if not category:
        return jsonify({'Error': f'Category with id {category_id} does not exist.'}), 400
    if not author:
        return jsonify({'Error': f'Author with id {author_id} does not exist.'}), 400

    # Assign updated category and author objects to the content
    content.category = category
    content.author = author

    db.session.commit()
    return content_schema.jsonify(content)

