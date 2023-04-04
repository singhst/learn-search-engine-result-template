import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Product(Base):
    id                  = Column(Integer,       nullable=False, primary_key=True)
    name                = Column(String(256),   nullable=True)
    shop_product_code   = Column(String(256),   nullable=True,  index=True)
    order_time_start    = Column(DateTime,      nullable=True)
    order_time_end      = Column(DateTime,      nullable=True)
    delivery_date       = Column(DateTime,      nullable=True)
    company             = Column(String(256),   nullable=True)
    original_website    = Column(String(256),   nullable=True)
    img_url             = Column(String(256),   nullable=True)
    order_status        = Column(String(256),   nullable=True)
    is_favourite        = Column(Boolean,       default=False)
    created_at          = Column(DateTime,      default=datetime.datetime.now)
    create_by           = Column(String(256),   nullable=True)
    updated_at          = Column(DateTime,      default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_by           = Column(String(256),   nullable=True)

    order = relationship("Order", back_populates="products")


    def __repr__(self):
        _string = f"""Product(
            id={self.id!r}, 
            name={self.name!r}, 
            shop_product_code={self.shop_product_code!r}, 
            order_time_start={self.order_time_start!r}, 
            order_time_end={self.order_time_end!r}, 
            delivery_date={self.delivery_date!r}, 
            company={self.company!r}, 
            original_website={self.original_website!r}, 
            img_url={self.img_url!r}, 
            order_status={self.order_status!r}, 
            is_favourite={self.is_favourite!r}, 
            created_at={self.created_at!r}, 
            create_by={self.create_by!r}, 
            updated_at={self.updated_at!r}, 
            update_by={self.update_by!r})"""
        return _string