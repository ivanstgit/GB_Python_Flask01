from werkzeug.security import generate_password_hash

from blog.app import create_app
from blog.models.database import db


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from blog.models import User

    admin = User(
        email="admin@blog.ru", is_staff=True, password=generate_password_hash("test")
    )
    user = User(email="user@blog.ru", password=generate_password_hash("test"))
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()
    print("done! created users:", admin, user)
