from flask import Blueprint, request
from init import db
from models.user import User
from models.content import Content, content_schema, contents_schema
from models.author import Author
from models.category import Category
from flask_jwt_extended import get_jwt_identity, jwt_required

def authorise_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin

content_bp = Blueprint('content', __name__, url_prefix='/content')

@content_bp.route('/')
def get_all_content():
    stmt = db.select(Content).order_by(Content.id.desc())
    contents = db.session.scalars(stmt)
    return contents_schema.dump(contents)

@content_bp.route('/<int:id>')
def get_one_content(id):
    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalar(stmt)
    if content:
        return content_schema.dump(content)
    else:
        return {'Error': f'Content not found with the id {id}'}, 404
    
@content_bp.route('/', methods=['POST'])
@jwt_required()
def create_content():
    json_data = request.get_json()
    is_admin = authorise_admin()
    if not is_admin:
        return {'Error': 'You must be an admin to create content.'}, 403

    title = json_data.get('title')
    genre = json_data.get('genre')
    description = json_data.get('description')
    published = json_data.get('published')
    publisher = json_data.get('publisher')

    category_id = json_data.get('category_id')
    author_id = json_data.get('author_id')
    if not category_id or not author_id:
        return {'Error': 'Both category_id and author_id must be provided when creating content.'}, 400

    category = db.session.query(Category).get(category_id)
    author = db.session.query(Author).get(author_id)

    if not category:
        return {'Error': f'Category with id {category_id} does not exist.'}, 400
    if not author:
        return {'Error': f'Author with id {author_id} does not exist.'}, 400

    content = Content(
        title=title,
        category_id=category_id,
        author_id=author_id,
        genre=genre,
        description=description,
        published=published,
        publisher=publisher,
    )

    db.session.add(content)
    db.session.commit()
    return content_schema.dump(content), 201


@content_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_content(id):
    admin_status = authorise_admin()
    if not admin_status:
        return {'Error': 'You must be an admin to delete content.'}

    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalar(stmt)
    if content:
        db.session.delete(content)
        db.session.commit()
        return {'Message': f'Content {content.title} has been deleted successfully.'}
    else: 
        return {'Error': f'Content with the id {id} does not exist.'}, 404

@content_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_content(id):
    json_data = content_schema.load(request.get_json(), partial=True)
    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalar(stmt)
    if content:
        is_admin = authorise_admin()
        if not is_admin:
            return {'Error': 'You must be an admin to edit any content.'}, 403

        content.title = json_data.get('title', content.title)
        content.genre = json_data.get('genre', content.genre)
        content.description = json_data.get('description', content.description)
        content.published = json_data.get('published', content.published)

        category_id = json_data.get('category_id', content.category_id)
        author_id = json_data.get('author_id', content.author_id)

        category = db.session.query(Category).get(category_id)
        author = db.session.query(Author).get(author_id)
        if not category:
            return {'Error': f'Category with id {category_id} does not exist.'}, 400
        if not author:
            return {'Error': f'Author with id {author_id} does not exist.'}, 400

        content.category = category
        content.author = author

        db.session.commit()
        return content_schema.dump(content)
    else:
        return {'Error': f'Content with id {id} does not exist.'}, 404

