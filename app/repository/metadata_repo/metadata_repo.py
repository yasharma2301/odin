from sqlalchemy.orm import Session
from app.models.entity.metadata import Metadata


class MetadataRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_metadata(self, metadata: dict) -> Metadata:
        new_metadata = Metadata(**metadata)
        self.db.add(new_metadata)
        self.db.commit()
        return new_metadata