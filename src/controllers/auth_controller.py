from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta


# Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def auth_register():
    """
    Route for user registration.

    This route allows users to create a new account by providing their
    details such as first name, last name, email, and password.

    Parameters:
        None

    Returns:
        Serialized user object upon successful registration with HTTP status code 201 (Created).
        Error message with HTTP status code 409 (Conflict) if the email is already in use.
        Error message with HTTP status code 409 (Conflict) if any required fields are missing.
    """
    try:
        body_data = request.get_json()
        # Create user and get required information
        user = User() 
        user.first_name = body_data.get('first_name')
        user.last_name = body_data.get('last_name')
        user.email = body_data.get('email')
        # Hash password before storing in database
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        
        # Add user and commit to database
        db.session.add(user)
        db.session.commit()
        # Return the serialized user data and HTTP status code 201 (Created)
        return user_schema.dump(user), 201
    
    # Handle unique constraint violation (email must be unique)
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'Error': 'Email is already in use' }, 409
        # Handle NOT NULL constraint violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'Error': f'{err.orig.diag.column_name} is required' }, 409
        
        
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    """
    Route for user login.

    This route allows users to log in to their existing account by providing
    their email and password.

    Parameters:
        None

    Returns:
        User email, JWT access token, and admin status when login successful with HTTP status code 200 (OK).
        Error message with HTTP status code 401 (Unauthorized) if the provided email or password is invalid.
    """
    body_data = request.get_json()
    
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    
    # Check if the user exists and the password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        # Generate a JWT access token for the user with a 1-day expiration
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # Return the user's email, JWT token, and if the user is an admin
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin }
    else:
        # Return an error message if login details are invalid
        return { 'Error': 'Invalid email or password, please try again' }, 401