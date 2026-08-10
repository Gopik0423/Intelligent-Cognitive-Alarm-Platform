"""
create_admin.py

Creates the platform's single Admin account. This is intentionally NOT
exposed through the public /register endpoint (Signup.jsx only ever
creates "user" role accounts) -- admin accounts should be created
deliberately, by someone who already has access to the machine/database,
not by anyone who visits the signup page.

Run from inside Backend/ (with your venv active):
    python -m scripts.create_admin
"""

from datetime import date
from database.db import SessionLocal, Base, engine
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

ADMIN_EMAIL = "admin@platform.com"
ADMIN_PASSWORD = "ChangeThisPassword123"  # change this before running in anything real
ADMIN_NAME = "Platform Admin"


def create_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.role == "admin").first()
        if existing:
            print(f"An admin already exists: {existing.email} (id={existing.id}). Refusing to create a second one.")
            return

        existing_email = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if existing_email:
            print(f"A user with email {ADMIN_EMAIL} already exists (id={existing_email.id}, role={existing_email.role}).")
            return

        hashed = pwd_context.hash(ADMIN_PASSWORD)
        admin = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password=hashed,
            role="admin",
            date_of_birth=date(1990, 1, 1),
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Admin created: id={admin.id}, email={admin.email}")
        print("Log in with this email and the password set in this script, then change it.")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
