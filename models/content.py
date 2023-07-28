from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


class Content(db.Model):
    __tablename__ = "content"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    description = db.Column(db.Text)
    published = db.Column(db.Date)
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

    description = fields.String(required=True, validate=And(Length(min=10, error='Description must be at least 10 characters long'),
                                                            Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers are allowed')
                                                            ))   

    class Meta:
        fields = ('id', 'title', 'author_id', 'category_id', 'genre', 'description', 'published', 'publisher')
        ordered = True

content_schema = ContentSchema()
contents_schema = ContentSchema(many=True)