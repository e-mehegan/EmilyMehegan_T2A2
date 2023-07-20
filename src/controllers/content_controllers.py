from flask import Blueprint, request
from init import db
from models.content import Content, content_schema, contents_schema

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
    
# make this so only admin can create content
@content_bp.route('/', methods=['POST'])
def create_content():
    pass