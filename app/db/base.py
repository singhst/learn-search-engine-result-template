# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
# from app.models.user import User  # noqa
# from app.models.recipe import Recipe  # noqa
from app.models.crawler import Crawler
from app.models.parent_child_link import Parent_Child_Link
