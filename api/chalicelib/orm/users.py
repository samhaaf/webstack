from .base import Base
from sqlalchemy import Column, DateTime, String, Integer, func, LargeBinary, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import FetchedValue



class User(Base):
    __tablename__ = 'user'
    uid = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime, server_default=FetchedValue())
    deleted_at = Column(DateTime)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    email_address = Column(String, unique=True)
    password_hash = Column(LargeBinary)
    password_salt = Column(LargeBinary)
    # banned = Column(Boolean)

    def __repr__(self):
        return f'{self.last_name}, {self.first_name} - {self.email_address} - @{self.username}'
