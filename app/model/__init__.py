from .tables import init_tables
# from .tables import init_views
from .views import init_views

from .tables import create_tables
from .tables import delete_tables
from .tables import query_aging_all
from .tables import query_device_all
from .tables import query_factory_all
from .views import query_aging_all_from_view
from .tables import gen_testdata

def init_model(app):
    init_tables(app)
    init_views(app)
