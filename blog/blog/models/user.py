from flask_login import UserMixin

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from blog.models.database import db
from blog.security import flask_bcrypt


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    first_name = Column(
        String(120), unique=False, nullable=False, default="", server_default=""
    )
    last_name = Column(
        String(120), unique=False, nullable=False, default="", server_default=""
    )
    email = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    _password = Column(String(72), nullable=True)

    author = relationship("Author", uselist=False, back_populates="user")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value).decode("utf-8")

    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self._password, password)

    def __repr__(self):
        return f"<User #{self.first_name} {self.last_name!r}>"
