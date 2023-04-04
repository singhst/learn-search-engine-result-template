import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Crawler(Base):
    url_id                  = Column(Integer,       nullable=False, primary_key=True)
    url                 = Column(String,        nullable=False)
    html_content        = Column(String,        nullable=False)
    # created_at          = Column(DateTime,      default=datetime.datetime.now)
    # create_by           = Column(String(256),   nullable=True)
    # updated_at          = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # update_by           = Column(String(256),   nullable=True)

    parent_child_link = relationship("Parent_Child_Link", back_populates="crawler")


    def __repr__(self):
        _string = f"""Order(
            id={self.url_id!r}, 
            url={self.url!r}, 
            html_content={self.html_content!r})"""
        return _string