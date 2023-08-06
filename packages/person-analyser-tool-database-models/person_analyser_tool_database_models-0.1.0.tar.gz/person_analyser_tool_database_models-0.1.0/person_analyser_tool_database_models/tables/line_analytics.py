from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer

from .base import Base


class LineAnalytics(Base):
    __tablename__ = 'line_analytics'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    saved = Column(DateTime, nullable=False, server_default=func.now())
    line_id = Column(Integer, nullable=False)
    up = Column(Integer, nullable=False)
    down = Column(Integer, nullable=False)
