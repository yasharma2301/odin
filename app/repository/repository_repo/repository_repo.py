from sqlalchemy.orm import Session
from app.models.entity.repository import Repository

class RepositoryRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_repository_by_id(self, repository_id: int) -> Repository:
        return self.db.query(Repository).filter(Repository.id == repository_id).first()

    def create_repository(self, repository: dict) -> Repository:
        new_repository = Repository(**repository)
        self.db.add(new_repository)
        self.db.commit()
        return new_repository

    def update_repository(self, repository_id: int, repository: dict) -> Repository:
        existing_repository = self.get_repository_by_id(repository_id)
        if existing_repository:
            for key, value in repository.items():
                setattr(existing_repository, key, value)
            self.db.commit()
        return existing_repository

    def delete_repository(self, repository_id: int) -> bool:
        existing_repository = self.get_repository_by_id(repository_id)
        if existing_repository:
            self.db.delete(existing_repository)
            self.db.commit()
            return True
        return False


