# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
# from app.models.user import User  # noqa
# from app.models.recipe import Recipe  # noqa
from app.models.product import Product
from app.models.order import Order
