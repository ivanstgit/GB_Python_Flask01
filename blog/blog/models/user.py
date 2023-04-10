from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from blog.models.database import db


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    password = db.Column(db.String(255))

    def __repr__(self):
        return f"<User #{self.id} {self.email!r}>"
