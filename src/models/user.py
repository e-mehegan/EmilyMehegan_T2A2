from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    year_born = db.Column(db.Integer)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    reviews = db.relationship('Review', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'year_born', 'email', 'password', 'is_admin', 'reviews')
        ordered = True

# this is for one user
user_schema = UserSchema(exclude=['password'])
# this is for list of users
users_schema = UserSchema(many=True, exclude=['password'])