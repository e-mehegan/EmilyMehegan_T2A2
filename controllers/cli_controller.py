from flask import Blueprint
from init import db, bcrypt
from datetime import date, datetime
from models.user import User
from models.content import Content
from models.review import Review
from models.category import Category
from models.author import Author


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    """
    Command for creating the database.

    This command creates all the tables defined in the database models.
    Used for setting up the database for the first time.

    Usage:
        flask db create

    Returns:
        Prints "Tables Created" upon successful creation of the tables.
    """
    db.create_all()
    print("Tables Created")


@db_commands.cli.command('drop')
def drop_db():
    """
    Command for dropping the database.

    This command drops all the tables defined in the database models.
    It will delete all data in the database.

    Usage:
        flask db drop

    Returns:
        Prints "Tables dropped" upon successful dropping of the tables.
    """
    db.drop_all()
    print("Tables dropped")


# The command for seeding the objects
@db_commands.cli.command('seed')
def seed_db():
    """
    Command for dropping the database.

    This command adds data into the database, such as neccesary data and test data.
    Used for developing and testing the application.

    Usage:
        flask db seed

    Returns:
        Prints "Database seeded" upon successful seeding of the database.
    """
    categories = [
        Category(
        category='Novel'
        ),
        Category(
        category='Short Story'
        ),
        Category(
        category='Manga'
        ),
        Category(
        category='Thesis'
        ),
        Category(
        category='Poetry'
        ),
        Category(
        category='Essay'
        ),
        Category(
        category='Autobiography'
        ),
        Category(
        category='Article'
        ),
        Category(
        category='Biography'
        ),
        Category(
        category='Picture Book'
        ),
        Category(
        category='Comic'
        ),
    ]

    # Adding the categories to the session and committing to the database
    db.session.add_all(categories)
    db.session.commit()

# Seeding the authors
    authors = [
            Author(
            author='author 1'
            ),
            Author(
            author='author 2'
            ),
            Author(
            author='author 3'
            ),
            Author(
            author='author 4'
            ),
            Author(
            author='author 5'
            ),
            Author(
            author='author 6'
            ),
            Author(
            author='author 7'
            ),
            Author(
            author='author 8'
            ),
    ]

    # Adding the authors to the session and committing to the database
    db.session.add_all(authors)
    db.session.commit()

# Seeding the users
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

    # Adding the users to the session and committing to the database
    db.session.add_all(users)
    db.session.commit()

# Seeding the content
    content = [
        Content(
            title='Content 1',
            category=categories[0],
            author=authors[0], 
            genre='Genre 1',
            description='Content 1 description',
            published=date(2009, 1, 1),
            publisher='Publisher 1'
        ),
        Content(
            title='Content 2',
            category=categories[1],
            author=authors[1],
            genre='Genre 2',
            description='Content 2 description',
            published=date(2010, 1, 1),
            publisher='Publisher 2', 
        ),
        Content(
            title='Content 3',
            category=categories[2],
            author=authors[2],
            genre='Genre 3',
            description='Content 3 description',
            published=date(2011, 1, 1),
            publisher='Publisher 3', 
        ),
        Content(
            title='Content 4',
            category=categories[3],
            author=authors[3],
            genre='Genre 4',
            description='Content 4 description',
            published=date(2012, 1, 1),
            publisher='Publisher 4', 
        ),
    ]

    # Adding the content to the session and committing to the database
    db.session.add_all(content)
    db.session.commit()

    # Seeding the reviews
    reviews = [
        Review(
            content=content[0],
            rating='5',
            comment='Comment 1',
            created=date.today(),
            user=users[0],
        ),
        Review(
            content=content[1],
            rating='4',
            comment='Comment 2',
            created=date.today(),
            user=users[1], 
        ),
        Review(
            content=content[2],
            rating='2',
            comment='Comment 3',
            created=date.today(),
            user=users[0], 
        ),
        Review(
            content=content[3],
            rating='4',
            comment='Comment 4',
            created=date.today(),
            user=users[1], 
        ),
    ]

    # Adding the reviews to the session and committing to the database
    db.session.add_all(reviews)
    db.session.commit()

    print("Tables seeded")
