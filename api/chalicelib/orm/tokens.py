from .base import Base
from sqlalchemy import Column, DateTime, Integer, func, Boolean
import time


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    sid = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user_sid = Column(Integer)
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
