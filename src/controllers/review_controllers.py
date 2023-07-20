from flask import Blueprint, request
from init import db, bcrypt
from datetime import date
from models.review import Review, review_schema, reviews_schema
from models.content import Content
from flask_jwt_extended import get_jwt_identity, jwt_required

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/')
def get_all_reviews():
    stmt = db.select(Review).order_by(Review.id.desc())
    reviews = db.session.scalars(stmt)
    return reviews_schema.dump(reviews)

@reviews_bp.route('/<int:id>')
def get_one_review(id):
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
    if review:
        return review_schema.dump(review)
    else:
        return {'Error': f'Review not found with the id {id}'}, 404


@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    body_data = request.get_json()
    content_id = body_data.get('content_id')
    if not content_id:
        return {'Error': 'content_id must be provided when creating a review.'}, 400

    content = Content.query.get(content_id)
    if not content:
        return {'Error': f'Content with id {content_id} does not exist.'}, 404

    review = Review(
        content_id=content_id,
        rating=body_data.get('rating'),
        comment=body_data.get('comment'),
        created=date.today(),
        user_id=get_jwt_identity()
    )

    db.session.add(review)
    db.session.commit()
    return review_schema.dump(review), 201


@reviews_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_review(id):
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'Message': f'Review has been deleted successfully'}
    else:
        return {'Error': f'Review not found with id {id}'}, 404
    
@reviews_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_review(id):
    body_data = request.get_json()
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
    if review:
        if str(review.user_id) != get_jwt_identity():
            return {'Error': 'You must be the owner of this review to edit.'}, 403
        review.rating = body_data.get('rating') or review.rating
        review.comment = body_data.get('comment') or review.comment
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {'Error': f'Review not found with {id}'}, 404
            

