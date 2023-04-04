import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Parent_Child_Link(Base):
    url_id          = Column(Integer,   ForeignKey('crawler.url_id'), nullable=False, primary_key=True)
    child_url_id    = Column(Integer,   ForeignKey('crawler.url_id'), nullable=False)
    # created_at      = Column(DateTime,      default=datetime.datetime.now)
    # create_by       = Column(String(256),   nullable=True)
    # updated_at      = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # update_by       = Column(String(256),   nullable=True)

    crawler = relationship(
        "Cralwer",
        cascade="all,delete-orphan",
        back_populates="parent_child_link",
        uselist=True,
        # sqlalchemy.exc.ArgumentError: For many-to-one relationship Order.products, delete-orphan cascade is normally configured only on the "one" side of a one-to-many relationship, and not on the "many" side of a many-to-one or many-to-many relationship.  To force this relationship to allow a particular "Product" object to be referred towards by only a single "Order" object at a time via the Order.products relationship, which would allow delete-orphan cascade to take place in this direction, set the single_parent=True flag. (Background on this error at: https://sqlalche.me/e/14/bbf0)
        # single_parent=True,
    )


    def __repr__(self):
        _string = f"""Product(
            url_id={self.url_id!r}, 
            child_url_id={self.child_url_id!r})"""
        return _string