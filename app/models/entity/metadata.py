from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.core.setup_sql import Base
from sqlalchemy.orm import relationship


class Metadata(Base):
    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('file.id'), nullable=False)
    function_name = Column(String(255))
    function_code = Column(Text)
    function_type = Column(String(100))
    class_name = Column(String(100))

    file = relationship('File', back_populates='metadata_list')

    def to_json(self):
        return {
            'id': self.id,
            'file_id': self.file_id,
            'function_name': self.function_name,
            'function_code': self.function_code,
            'function_type': self.function_type,
            'class_name': self.class_name,
        }
