from sqlalchemy import Column, Integer, String, Enum, ForeignKey, UniqueConstraint, Text
from app.core.setup_sql import Base
from sqlalchemy.orm import relationship


class Repository(Base):
    __tablename__ = 'repository'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey('user.uid'))
    url = Column(String(500))
    status = Column(Enum('QUEUED', 'IN_PROGRESS', 'COMPLETED', 'FAILED'), nullable=False)
    error = Column(String(255))

    user = relationship('User', back_populates='repositories')
    files = relationship('File', back_populates='repository')

    __table_args__ = (
        UniqueConstraint('url', 'user_id'),
    )

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'url': self.url,
            'status': self.status,
            'error': self.error,
        }

