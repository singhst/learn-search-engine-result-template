import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Term_1_Gram(Base):
    term_id         = Column(Integer,   nullable=False, primary_key=True)
    term            = Column(String,    nullable=False)
    # created_at          = Column(DateTime,      default=datetime.datetime.now)
    # create_by           = Column(String(256),   nullable=True)
    # updated_at          = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # update_by           = Column(String(256),   nullable=True)

    doc_term_1_gram = relationship("Doc_Term_1_Gram", back_populates="term_1_gram")


    def __repr__(self):
        _string = f"""Term_1_Gram(
            term_id={self.term_id!r}, 
            term={self.term!r})"""
        return _string