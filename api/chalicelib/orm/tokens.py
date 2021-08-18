from .base import Base
from sqlalchemy import Column, DateTime, Integer, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import FetchedValue
import time


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    uid = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime, server_default=FetchedValue())
    deleted_at = Column(DateTime)
    user_uid = Column(Integer)
    time_to_live = Column(Integer)
    invalidated = Column(Boolean)

    def __repr__(self):
        return f'sid: {self.sid}, user_sid: {self.user_sid}'

    @property
    def time_left(self):
        return self.time_to_live - (time.time() - self.created_at.timestamp())

    @property
    def expired(self):
        return self.time_left < 0
