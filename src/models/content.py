from init import db, ma
from marshmallow import fields

class Content(db.Model):
    __tablename__ = "content"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    description = db.Column(db.Text)
    published = db.Column(db.String)
    publisher = db.Column(db.String)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    reviews = db.relationship('Review', back_populates='content', cascade='all, delete')
    author = db.relationship('Author', back_populates='content')
    category = db.relationship('Category', back_populates='content')

class ContentSchema(ma.Schema):
    reviews = fields.Nested('ReviewSchema', exclude=['id'])
    author = fields.Nested('AuthorSchema')
    category = fields.Nested('CategorySchema')

    class Meta:
        fields = ('id', 'author', 'category,' 'title', 'genre', 'description', 'published', 'publisher', 'reviews')
        ordered = True

content_schema = ContentSchema()
contents_schema = ContentSchema(many=True)