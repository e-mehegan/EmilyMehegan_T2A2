from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.content_controllers import content_bp
from controllers.review_controllers import reviews_bp
from controllers.category_controller import category_bp
from controllers.author_controller import author_bp
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'Error': err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {'Error': str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {'Error': str(err)}, 404

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(author_bp)

    return app