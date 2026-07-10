from Backend.database.db import SessionLocal, Base, engine
from Backend.models.user import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def create_user():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "test@example.com").first()
        if existing:
            print("Test user already exists with id:", existing.id)
            return

        hashed = pwd_context.hash("secret")
        user = User(name="test", email="test@example.com", password=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Created test user id:", user.id)
    finally:
        db.close()


if __name__ == '__main__':
    create_user()
