import click
import os

from flask import Flask

from blog.models.database import db


def register_commands(app: Flask):
    @app.cli.command("create-tags")
    @click.command
    def create_tags():
        """
        Run in your terminal:
        ➜ flask create-tags
        """
        from blog.models import Tag

        for name in [
            "flask",
            "django",
            "python",
            "sqlalchemy",
            "news",
        ]:
            tag = Tag(name=name)
            db.session.add(tag)
        db.session.commit()
        print("created tags")

    @app.cli.command("create-users")
    def create_users():
        """
        Run in your terminal:
        flask create-users
        > done! created users: <User #1 'admin'> <User #2 'james'>
        """
        from blog.models import User

        admin_email = os.environ.get("ADMIN_EMAIL") or "admin@blog.ru"
        admin_password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
        admin = User.query.filter(User.email == admin_email).first()
        if not admin:
            admin = User(email=admin_email, is_staff=True, first_name="Admin")
            db.session.add(admin)
        admin.password = admin_password

        user_email = "user@blog.ru"
        user = User.query.filter(User.email == user_email).first()
        if not user:
            user = User(email=user_email, first_name="User")
            db.session.add(user)
        user.password = "test"

        db.session.commit()
        print("done! created/updated users:", admin, user)
