"""
project/models.py

The User model for the exam_registration database. It maps onto the users
table that setup_exam_db.py creates, so Flask reads and writes that table
rather than creating its own.
"""

from flask_login import UserMixin
from sqlalchemy.dialects.mysql import INTEGER

from . import db


class User(UserMixin, db.Model):
    """One row in the users table from exam_registration_final.sql."""

    __tablename__ = "users"

    user_id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    role = db.Column(db.Enum("Student", "Faculty"), nullable=False, server_default="Student")
    created_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))

    # Matches CONSTRAINT uq_user in the SQL file. If you change that to
    # UNIQUE (email), change this to db.UniqueConstraint("email", name="uq_user").
    __table_args__ = (db.UniqueConstraint("password", "email", name="uq_user"),)

    def get_id(self):
        # Flask-Login looks for a column called "id" by default. This table
        # calls it user_id, so this tells Flask-Login where to find it.
        return str(self.user_id)

    def __repr__(self):
        return f"<User {self.email}>"