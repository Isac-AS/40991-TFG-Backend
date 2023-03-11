from flask.cli import FlaskGroup
from src.accounts.models import User
import getpass

from src import app, db

cli = FlaskGroup(app)

@cli.command("create_admin")
def create_admin():
    """Creates an admin user
    """
    username = input("Enter admin username: ")
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    check_password = getpass.getpass("Confirm password: ")

    if password != check_password:
        print("Passwords don't match!")
        return 1

    try:
        user = User(
            username=username,
            email=email,
            password=password,
            role=10,
            is_admin=True,
            created_by="CLI"
        )
        db.session.add(user)
        db.session.commit()
    except Exception:
        print("Couldn't create admin user")


if __name__ == "__main__":
    cli()
