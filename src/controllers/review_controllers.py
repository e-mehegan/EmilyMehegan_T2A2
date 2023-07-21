# Imports for this file
from flask import Blueprint, request
from init import db, bcrypt
from datetime import date
from models.review import Review, review_schema, reviews_schema
from models.content import Content
from flask_jwt_extended import get_jwt_identity, jwt_required


# Blueprint for reviews routes
reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@reviews_bp.route('/')
def get_all_reviews():
    """
    Route for retrieving all reviews.

    This route retrieves a list of all reviews from the database and returns it as JSON.

    Parameters:
        None

    Returns:
        A list of all reviews as JSON objects with HTTP status code 200 (OK).
    """
    stmt = db.select(Review).order_by(Review.id.desc())
    reviews = db.session.scalars(stmt)
    return reviews_schema.dump(reviews)


@reviews_bp.route('/<int:id>')
def get_one_review(id):
    """
    Route for retrieving a single review by the ID.

    This route retrieves a single review from the database based on the provided ID and returns it as JSON.

    Parameters:
        id (int): The ID of the review to retrieve.

    Returns:
        The review data as a JSON object with HTTP status code 200 (OK) if the review is found.
        An error message as a JSON object with HTTP status code 404 (Not Found) if the review is not found.
    """
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
    if review:
        return review_schema.dump(review)
    else:
        # Return an error message if the input ID is not found
        return {'Error': f'Review not found with the id {id}'}, 404


@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    """
    Route for creating new review.

    This route allows users to create a new review by providing
    details such as content_id, rating and comment.

    Parameters:
        None.

    Returns:
        The created review as a JSON object with HTTP status code 201 (Created) 
        if review is successfully created.

        An error message as a JSON object with HTTP status code 404 (Forbidden) 
        if the content_id doesn't exist. 

        An error message as a JSON object with HTTP status code 400 (Bad Request) 
        if the request JSON is missing required content_id.
    """
    body_data = request.get_json()
    content_id = body_data.get('content_id')
    # Return an error message if content_id is not provided.
    if not content_id:
        return {'Error': 'content_id must be provided when creating a review.'}, 400

    content = Content.query.get(content_id)
    # Return an error message if the content with the specified content_id does not exist
    if not content:
        return {'Error': f'Content with id {content_id} does not exist.'}, 404

    # Create a new review and add it to the database
    review = Review(
        content_id=content_id,
        rating=body_data.get('rating'),
        comment=body_data.get('comment'),
        created=date.today(),
        user_id=get_jwt_identity()
    )

    db.session.add(review)
    db.session.commit()
    # Return the created review as JSON with HTTP status code 201 (Created)
    return review_schema.dump(review), 201


# EDIT THIS ROUTE SO ADMIN AND USER CAN ONLY DELETE REVIEW
@reviews_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_review(id):
    """
    Route for deleting a single review by ID.

    This route allows authorized users to delete a review based on its ID.

    Parameters:
        id (int): The ID of the review to be deleted.

    Returns:
        A success message as a JSON object with HTTP status code 200 (OK) if the 
        review is found and successfully deleted.

        An error message as a JSON object with HTTP status code 404 (Not Found) 
        if the review with the specified ID does not exist.
    """
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
 # If the review exists, delete it from the database and commit the changes, if not retuen error 
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'Message': f'Review has been deleted successfully'}
    else:
        return {'Error': f'Review not found with id {id}'}, 404
    

@reviews_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_review(id):
    """
    Route for updating a single review by its ID.

    This route allows authorized users (the owners of the review) to update the 
    rating or comment of their review based on its ID.

    Parameters:
        id (int): The ID of the review to be updated.

    Returns:
        The updated review as a JSON object with HTTP status code 200 (OK) if the 
        review is found and successfully updated.

        An error message as a JSON object with HTTP status code 403 (Forbidden) 
        if the current user is not the owner of the review.

        An error message as a JSON object with HTTP status code 404 (Not Found) 
        if the review with the specified ID does not exist.
    """
    body_data = request.get_json()
    # Retrieve the review from the database based on the provided ID
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)

    # If the review exists, check if the current user is the owner of the review
    if review:
        if str(review.user_id) != get_jwt_identity():
            return {'Error': 'You must be the owner of this review to edit.'}, 403
        # Update rating and comment if provided in the request JSON, if not provided draw from database
        review.rating = body_data.get('rating') or review.rating
        review.comment = body_data.get('comment') or review.comment

        db.session.commit()
        return review_schema.dump(review)
    else:
        # Return an error message if the review with the specified ID does not exist
        return {'Error': f'Review not found with {id}'}, 404
            

