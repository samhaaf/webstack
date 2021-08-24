from .base import Base
from sqlalchemy import Column, DateTime, String, Integer, func, LargeBinary, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
import time


Base.hidden = ['created_at', 'updated_at', 'deleted_at']


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
    banned = Column(Boolean)

    hidden = Base.hidden + ['password_hash', 'password_salt']

    def __repr__(self):
        return f'User({self.uid})'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    uid = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime, server_default=FetchedValue())
    deleted_at = Column(DateTime)
    user_uid = Column(Integer, ForeignKey('user.uid'))
    ttl = Column(Integer, default=7*24*60*60)
    invalidated = Column(Boolean)

    user = relationship('User', backref='refresh_tokens', foreign_keys=[user_uid])

    def __repr__(self):
        return f'RefreshToken({self.uid})'

    @property
    def time_left(self):
        return self.ttl - (time.time() - self.created_at.timestamp())

    @property
    def expired(self):
        return self.time_left < 0
