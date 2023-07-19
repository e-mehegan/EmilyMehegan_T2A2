from init import db, ma
from marshmallow import fields

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)

    content = db.relationship('Content', back_populates=('author'))

class AuthorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'content')

author_schema = AuthorSchema()
authors_schema =AuthorSchema(many=True)