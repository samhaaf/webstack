from .base import Base
from sqlalchemy import Column, DateTime, String, Integer, func, LargeBinary


class User(Base):
    __tablename__ = 'user'
    sid = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    email_address = Column(String, unique=True)
    password_hash = Column(LargeBinary)
    password_salt = Column(LargeBinary)

    def __repr__(self):
        return f'{self.last_name}, {self.first_name} - {self.email_address} - @{self.username}'
