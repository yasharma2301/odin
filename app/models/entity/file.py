from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.core.setup_sql import Base
from sqlalchemy.orm import relationship


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    repository_id = Column(Integer, ForeignKey('repository.id'))
    file_extension = Column(String(25), nullable=False)
    file_name = Column(String(255), nullable=False)
    parent_folder_path = Column(String(400), nullable=False)
    status = Column(Enum('COMPLETED', 'FAILED'), nullable=False)
    error = Column(String(255))

    metadata_list = relationship('Metadata', back_populates='file')
    repository = relationship('Repository', back_populates='files')

    def to_json(self):
        return {
            'id': self.id,
            'repository_id': self.repository_id,
            'file_extension': self.file_extension,
            'file_name': self.file_name,
            'parent_folder_path': self.parent_folder_path,
            'status': self.status,
        }
