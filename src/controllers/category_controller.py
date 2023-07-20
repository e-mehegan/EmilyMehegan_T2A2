from flask import Blueprint, request
from init import db
from models.user import User
from models.category import Category, category_schema, categories_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

category_bp = Blueprint('category', __name__, url_prefix='/category')

@category_bp.route('/')
def get_all_categories():
    stmt = db.select(Category).order_by(Category.id.desc())
    categories = db.session.scalars(stmt)
    return categories_schema.dump(categories)

@category_bp.route('/<int:id>')
def get_one_category(id):
    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)
    if category:
        return category_schema.dump(category)
    else:
        return {'Error': f'Category not found with the id {id}'}, 404
    

