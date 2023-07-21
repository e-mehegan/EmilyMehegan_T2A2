from init import db, ma
from marshmallow import fields

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)

    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)

    content = db.relationship('Content', back_populates='category')

class CategorySchema(ma.Schema):
    content = fields.Nested('ContentSchema', many=True) 
    class Meta:
        fields = ('id', 'category', 'content')
        ordered = True

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

