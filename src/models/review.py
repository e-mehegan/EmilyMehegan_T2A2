from init import db, ma
from marshmallow import fields

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created = db.Column(db.Date)


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    content = db.relationship('Content', back_populates='reviews')

class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name'])
    content = fields.Nested('ContentSchema', exclude=['description'])

    class Meta:
        fields = ('id', 'content', 'rating', 'comment', 'created', 'user')
        ordered = True


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

