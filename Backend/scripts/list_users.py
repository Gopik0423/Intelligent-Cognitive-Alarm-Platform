from Backend.database.db import SessionLocal, Base, engine
from Backend.models.user import User


def list_users():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for u in users:
            print(f"id={u.id} email={u.email} name={u.name} password={u.password}")
        if not users:
            print("No users found")
    finally:
        db.close()


if __name__ == '__main__':
    list_users()
