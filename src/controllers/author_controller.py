# Imports for the file
from flask import Blueprint, request
from init import db
from models.user import User
from models.author import Author, authors_schema, author_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

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
    