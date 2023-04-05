# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
# from app.models.user import User  # noqa
# from app.models.recipe import Recipe  # noqa

### crawler
from app.models.crawler import Crawler
from app.models.parent_child_link import Parent_Child_Link
from app.models.doc_total_number import Doc_Total_Number
from app.models.doc_info import Doc_Info

### indexer
from app.models.doc_term_1_gram import Doc_Term_1_Gram
from app.models.term_1_gram import Term_1_Gram
