from database.db import SessionLocal, Base, engine
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def ensure_hashed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            print("No test user found to update")
            return
        if user.password.startswith("$2"):
            print("Password already hashed for user id:", user.id)
            return
        hashed = pwd_context.hash(user.password)
        user.password = hashed
        db.add(user)
        db.commit()
        print("Updated password to hashed for user id:", user.id)
    finally:
        db.close()


if __name__ == '__main__':
    ensure_hashed()
