from flask import Blueprint, request
from init import db, bcrypt
from models.review import Review, review_schema, reviews_schema

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/')
def get_all_reviews():
    stmt = db.select(Review).order_by(Review.id.desc())
    reviews = db.session.scalars(stmt)
    return reviews_schema.dump(reviews)

