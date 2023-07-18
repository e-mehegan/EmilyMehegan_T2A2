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


    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    category_id_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

# enter relationships

# enter contentschema
class ContentSchema(ma.Schema):
    pass 

    class Meta:
        fields = ('id', 'title', 'genre', 'description', 'published', 'publisher')
        ordered = True

content_schema = ContentSchema()
contents_schema = ContentSchema(many=True)