from init import db, bcrypt
from flask import Blueprint, request
from models.user import User
from models.review import Review, review_schema, reviews_schema

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')