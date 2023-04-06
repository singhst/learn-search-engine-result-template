import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Doc_Info(Base):
    url_id                  = Column(Integer, nullable=False, primary_key=True)
    url                     = Column(String,  nullable=False)
    title                   = Column(String,  nullable=False)
    last_modification_date  = Column(DateTime,nullable=False)
    size_of_page            = Column(Integer, nullable=False)
    html_content            = Column(String,  nullable=False)
    # created_at      = Column(DateTime,      default=datetime.datetime.now)
    # create_by       = Column(String(256),   nullable=True)
    # updated_at      = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # update_by       = Column(String(256),   nullable=True)

    parent_child_link = relationship("Parent_Child_Link", back_populates="doc_info")


    def __repr__(self):
        _string = f"""Doc_Info(
            url_id={self.url_id!r}, 
            url={self.url!r}, 
            title={self.title!r}, 
            last_modification_date={self.last_modification_date!r}, 
            size_of_page={self.size_of_page!r},
            html_content={self.html_content!r})"""
        return _string
