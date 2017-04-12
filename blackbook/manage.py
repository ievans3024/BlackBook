from flask_script import Manager, prompt, prompt_pass
from blackbook.app import app
from blackbook.database import User, db, init_db
from werkzeug import security

manager = Manager(app)


@manager.command
def init_db():
    init_db(db, app)


@manager.command
def create_root_user():

    # TODO: check that db is initialized
    # TODO: check that user table is empty

    password = None
    password_again = None

    def prompt_password():
        global password
        global password_again
        password = prompt('Password: ')
        password_again = prompt('Verify Password: ')

    username = prompt('User Name: ', default='root')
    email = prompt('User Email: ')

    while not email:
        print('Email cannot be empty.')
        email = prompt('User Email: ')

    prompt_password()

    while not password:
        print('Password cannot be empty.')
        prompt_password()

    while password != password_again:
        print('Passwords do not match. Please try again.')
        prompt_password()

    password_hash = security.generate_password_hash(
        password,
        method=app.config.get('BLACKBOOK_PASSWORD_HASH_METHOD'),
        salt_length=app.config.get('BLACKBOOK_PASSWORD_SALT_LENGTH')
    )

    # TODO: get all permissions from db

    permissions = []

    root_user = User(display_name=username, email=email, password_hash=password_hash, permissions=permissions)

    db.session.add(root_user)
    db.session.commit()

    print('User {0} added (ID: {1})'.format(username, root_user.id))


if __name__ == '__main__':
    manager.run()
