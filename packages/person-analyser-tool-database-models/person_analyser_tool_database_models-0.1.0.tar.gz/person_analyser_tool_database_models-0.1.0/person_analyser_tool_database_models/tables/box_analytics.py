from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import DOUBLE

from .base import Base


class BoxAnalytics(Base):
    __tablename__ = 'box_analytics'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    saved = Column(DateTime, nullable=False, server_default=func.now())
    box_id = Column(Integer, nullable=False)
    time_spent_in = Column(DOUBLE, nullable=False)
