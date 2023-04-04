import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Order(Base):
    id                  = Column(Integer,   nullable=False, primary_key=True)
    order_at            = Column(DateTime,  nullable=True)
    pay_at              = Column(DateTime,  nullable=True)
    qty                 = Column(Integer,   nullable=True, default=0)
    total_price         = Column(Integer,   nullable=True, default=0)
    status              = Column(Integer,   nullable=True, default=0)
    created_at          = Column(DateTime,      default=datetime.datetime.now)
    create_by           = Column(String(256),   nullable=True)
    updated_at          = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_by           = Column(String(256),   nullable=True)

    product_id          = Column(Integer,   ForeignKey('product.id'), nullable=False)
    products = relationship(
        "Product",
        cascade="all,delete-orphan",
        back_populates="order",
        uselist=True,
        # sqlalchemy.exc.ArgumentError: For many-to-one relationship Order.products, delete-orphan cascade is normally configured only on the "one" side of a one-to-many relationship, and not on the "many" side of a many-to-one or many-to-many relationship.  To force this relationship to allow a particular "Product" object to be referred towards by only a single "Order" object at a time via the Order.products relationship, which would allow delete-orphan cascade to take place in this direction, set the single_parent=True flag. (Background on this error at: https://sqlalche.me/e/14/bbf0)
        single_parent=True,
    )


    def __repr__(self):
        _string = f"""Order(
            id={self.id!r}, 
            created_at={self.created_at!r}, 
            create_by={self.create_by!r}, 
            updated_at={self.updated_at!r}, 
            update_by={self.update_by!r})"""
        return _string