from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)

    content = db.relationship('Content', back_populates='category')

class CategorySchema(ma.Schema):
    content = fields.Nested('ContentSchema', many=True) 

    category = fields.String(required=True, validate=And(Length(min=10, error='Description must be at least 10 characters long'),
                                                            Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers are allowed')
                                                            ))
    class Meta:
        fields = ('id', 'category', 'content')
        ordered = True

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)