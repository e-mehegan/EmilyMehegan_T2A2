from flask import Blueprint, request
from init import db
from models.content import Content, content_schema, contents_schema
from models.user import User

content_bp = Blueprint('content', __name__, url_prefix='/content')

