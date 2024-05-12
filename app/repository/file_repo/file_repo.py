from app.models.entity.file import File
from app.core.setup_sql import get_db
from app.models.entity.metadata import Metadata

class FileRepo:
    def __init__(self):
        self.db = self.db = next(get_db())

    def get_file_by_id(self, file_id: int) -> File:
        return self.db.query(File).filter(File.id == file_id).first()

    def create_file(self, file_data: dict) -> File:
        metadata_list_data = file_data.pop('metadata', [])
        new_file = File(**file_data)

        metadata_list = [Metadata(**metadata_data) for metadata_data in metadata_list_data]
        new_file.metadata_list.extend(metadata_list)

        self.db.add(new_file)
        self.db.commit()
        return new_file

    def create_files(self, files: list) -> bool:
        if files:
            files_to_add = []
            for file_data in files:
                metadata_list_data = file_data.pop('metadata', [])
                new_file = File(**file_data)

                metadata_list = [Metadata(**metadata_data) for metadata_data in metadata_list_data]
                new_file.metadata_list.extend(metadata_list)

                files_to_add.append(new_file)

            self.db.add_all(files_to_add)
            self.db.commit()
            return True
        return False

    def update_file(self, file_id: int, file: dict) -> File:
        existing_file = self.get_file_by_id(file_id)
        if existing_file:
            for key, value in file.items():
                setattr(existing_file, key, value)
            self.db.commit()
        return existing_file

    def delete_file(self, file_id: int) -> bool:
        existing_file = self.get_file_by_id(file_id)
        if existing_file:
            self.db.delete(existing_file)
            self.db.commit()
            return True
        return False
