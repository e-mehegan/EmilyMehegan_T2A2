from flask import Blueprint, request
from init import db
from models.content import Content, content_schema, contents_schema
from models.user import User

content_bp = Blueprint('content', __name__, url_prefix='/content')

@content_bp.route('/')
def get_all_content():
    stmt = db.select(Content).order_by(Content.id.desc())
    content = db.session.scalars(stmt)
    return contents_schema.dump(content)

@content_bp.route('/<int:id>')
def get_one_content(id):
    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalar(stmt)
    if content:
        return content_schema.dump(content)
    else:
        return {'error': f'Content with id {id} does not exist.'}, 404