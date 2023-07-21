from init import db, ma
from marshmallow import fields

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)

    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)

    content = db.relationship('Content', back_populates=('author'))

class AuthorSchema(ma.Schema):
    content = fields.Nested('ContentSchema', many=True) 
    class Meta:
        fields = ('id', 'author', 'content')
        ordered = True

author_schema = AuthorSchema()
authors_schema =AuthorSchema(many=True)