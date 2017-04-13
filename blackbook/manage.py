from flask_script import Command, Manager, prompt, prompt_pass, prompt_bool
from app import app, init_config
from database import User, Permission, db
from werkzeug import security

manager = Manager(app)


def initialize_db():
    init_config(app)
    db.init_app(app)
    db.create_all(app=app)

    if not len(Permission.query.all()):
        permissions = [
            'blackbook.admin.create',
            'blackbook.admin.read',
            'blackbook.admin.edit',
            'blackbook.user.edit',
            'blackbook.user.read',
            'blackbook.user.create',
            'blackbook.user.contact.create',
            'blackbook.user.contact.read',
            'blackbook.user.contact.edit',
            'blackbook.user.contact.delete'
        ]

        for p in permissions:
            permission = Permission(p)
            db.session.add(permission)

        db.session.commit()


class InitDB(Command):
    """Initializes the configured database."""

    def run(self):
        initialize_db()


class CreateRoot(Command):
    """Creates a user with all permissions."""

    def run(self):

        # Initialize DB if it hasn't been done yet
        initialize_db()

        # Check if users exist, prompt with warning
        users = User.query.all()
        if len(users):
            user_continue = prompt_bool('Users exist, there should be a root user already. Continue?')
            if not user_continue:
                exit('Not creating any users.')

        def prompt_password():
            passwd = prompt_pass('Password: ')
            passwd_again = prompt_pass('Verify Password: ')
            return passwd, passwd_again

        username = prompt('User Name: ', default='root')
        email = prompt('User Email: ')

        while not email:
            print('Email cannot be empty.')
            email = prompt('User Email: ')

        password, password_again = prompt_password()

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

        permissions = Permission.query.all()

        root_user = User(display_name=username, email=email, password_hash=password_hash, permissions=permissions)

        db.session.add(root_user)
        db.session.commit()

        print('User {0} added (ID: {1})'.format(username, root_user.id))

if __name__ == '__main__':
    manager.add_command('init-db', InitDB())
    manager.add_command('create-root', CreateRoot())
    manager.run()
