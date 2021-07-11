from .base import Base
from sqlalchemy import Column, DateTime, String, Integer, func


class User(Base):
    __tablename__ = 'bug'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    email_address = Column(String, unique=True)
    password_hash = Column(String)
    password_salt = Column(String)

    def __repr__(self):
        return f'{self.last_name}, {self.first_name} - {self.email_address} - @{self.username}'
