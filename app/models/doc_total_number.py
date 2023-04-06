import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Doc_Total_Number(Base):
    id              = Column(Integer, nullable=False, primary_key=True)
    n               = Column(Integer, nullable=False)
    # created_at      = Column(DateTime,      default=datetime.datetime.now)
    # create_by       = Column(String(256),   nullable=True)
    # updated_at      = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # update_by       = Column(String(256),   nullable=True)


    def __repr__(self):
        _string = f"""Doc_Total_Number(
            n={self.n!r})"""
        return _string