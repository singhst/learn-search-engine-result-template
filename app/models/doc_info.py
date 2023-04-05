import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Doc_Info(Base):
    url_id          = Column(Integer, nullable=False, primary_key=True)
    size_of_page    = Column(Integer, nullable=False)
    # created_at      = Column(DateTime,      default=datetime.datetime.now)
    # create_by       = Column(String(256),   nullable=True)
    # updated_at      = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # update_by       = Column(String(256),   nullable=True)


    def __repr__(self):
        _string = f"""Doc_Info(
            url_id={self.url_id!r}, 
            size_of_page={self.size_of_page!r})"""
        return _string
