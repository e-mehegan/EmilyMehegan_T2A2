from flask import Blueprint, request
from init import db
from models.content import Content, content_schema, contents_schema

content_bp = Blueprint('content', __name__, url_prefix='/content')

@content_bp.route('/')
def get_all_content():
    stmt = db.select(Content).order_by(Content.id.desc())
    contents = db.session.scalars(stmt)
    return contents_schema.dump(contents)