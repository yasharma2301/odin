from app.models.entity.metadata import Metadata
from app.core.setup_sql import get_db


class MetadataRepo:
    def __init__(self):
        self.db = next(get_db())

    def create_metadata(self, metadata: dict) -> Metadata:
        new_metadata = Metadata(**metadata)
        self.db.add(new_metadata)
        self.db.commit()
        return new_metadata