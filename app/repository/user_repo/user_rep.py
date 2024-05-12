from app.models.entity.user import User
from app.core.setup_sql import get_db


class UserRepo:
    def __init__(self):
        self.db = next(get_db())

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: dict) -> User:
        user = User(**user)
        self.db.add(user)
        self.db.commit()
        return user

    def update_user(self, user_id: int, user: dict) -> User:
        existing_user = self.get_user_by_id(user_id)
        if existing_user:
            for key, value in user.items():
                setattr(existing_user, key, value)
            self.db.commit()
        return existing_user

    def delete_user(self, user_id: int) -> bool:
        existing_user = self.get_user_by_id(user_id)
        if existing_user:
            self.db.delete(existing_user)
            self.db.commit()
            return True
        return False
