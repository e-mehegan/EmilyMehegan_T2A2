from init import db, ma
from marshmallow import fields

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)

    content = db.relationship('Content', back_populates='category')

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'category', 'content')

category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)
    