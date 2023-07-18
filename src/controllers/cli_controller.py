from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.content import Content

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            first_name='Admin',
            last_name='Main',
            email='admin@main.com',
            password=bcrypt.generate_password_hash('admin1').decode('utf-8'),
            is_admin=True
        ),
        User(
            first_name='User1',
            last_name='One',
            email='user1@email.com',
            password=bcrypt.generate_password_hash('user1').decode('utf-8')
        ),
    ]

    db.session.add_all(users)

# TO DO: input for author and category
    content = [
        Content(
            title='Content 1',
            genre='Genre 1',
            description='Content 1 description',
            published='2009',
            publisher='Publisher 1', 
        ),
         Content(
            title='Content 2',
            genre='Genre 2',
            description='Content 2 description',
            published='2010',
            publisher='Publisher 2', 
        ),
         Content(
            title='Content 3',
            genre='Genre 3',
            description='Content 3 description',
            published='2011',
            publisher='Publisher 3', 
        ),
         Content(
            title='Content 4',
            genre='Genre 4',
            description='Content 4 description',
            published='2012',
            publisher='Publisher 4', 
        ),
    ]

    db.session.add_all(content)
    db.session.commit()

    # insert others

    print("Tables seeded")

