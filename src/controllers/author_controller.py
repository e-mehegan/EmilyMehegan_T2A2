from flask import Blueprint, request
from init import db
from models.user import User
from models.author import Author, authors_schema, author_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

author_bp = Blueprint('author', __name__, url_prefix='/author')

@author_bp.route('/')
def get_all_authors():
    stmt = db.select(Author).order_by(Author.id.desc())
    authors = db.session.scalars(stmt)
    return authors_schema.dump(authors)

@author_bp.route('/<int:id>')
def get_one_author(id):
    stmt = db.select(Author).filter_by(id=id)
    author = db.session.scalar(stmt)
    if author:
        return author_schema.dump(author)
    else:
        return {'Error': f'Author not found with the id {id}'}, 404
    