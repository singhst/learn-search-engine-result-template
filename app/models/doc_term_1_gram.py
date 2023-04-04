import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Doc_Term_1_Gram(Base):
    url_id          = Column(Integer,   ForeignKey('crawler.url_id'),           nullable=False, primary_key=True)
    term_id         = Column(Integer,   ForeignKey('term_1_gram.term_id'),   nullable=False, primary_key=True)
    term_freq       = Column(Integer,   nullable=False)
    # created_at      = Column(DateTime,      default=datetime.datetime.now)
    # create_by       = Column(String(256),   nullable=True)
    # updated_at      = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # update_by       = Column(String(256),   nullable=True)

    crawler = relationship(
        "Cralwer",
        cascade="all,delete-orphan",
        back_populates="doc_term_1_gram",
        uselist=True,
        # sqlalchemy.exc.ArgumentError: For many-to-one relationship Order.products, delete-orphan cascade is normally configured only on the "one" side of a one-to-many relationship, and not on the "many" side of a many-to-one or many-to-many relationship.  To force this relationship to allow a particular "Product" object to be referred towards by only a single "Order" object at a time via the Order.products relationship, which would allow delete-orphan cascade to take place in this direction, set the single_parent=True flag. (Background on this error at: https://sqlalche.me/e/14/bbf0)
        # single_parent=True,
    )

    term_1gram = relationship(
        "Term_1_Gram",
        cascade="all,delete-orphan",
        back_populates="doc_term_1_gram",
        uselist=True,
        # sqlalchemy.exc.ArgumentError: For many-to-one relationship Order.products, delete-orphan cascade is normally configured only on the "one" side of a one-to-many relationship, and not on the "many" side of a many-to-one or many-to-many relationship.  To force this relationship to allow a particular "Product" object to be referred towards by only a single "Order" object at a time via the Order.products relationship, which would allow delete-orphan cascade to take place in this direction, set the single_parent=True flag. (Background on this error at: https://sqlalche.me/e/14/bbf0)
        # single_parent=True,
    )


    def __repr__(self):
        _string = f"""Product(
            url_id={self.url_id!r}, 
            term_id={self.term_id!r}, 
            term_freq={self.term_freq!r})"""
        return _string