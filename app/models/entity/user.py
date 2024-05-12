from sqlalchemy import Column, Integer, String
from app.core.setup_sql import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(25), unique=True, nullable=False)
    name = Column(String(50))
    uid = Column(String(50), unique=True, nullable=False)

    repositories = relationship('Repository', back_populates='user')

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'uid': self.uid,
        }

