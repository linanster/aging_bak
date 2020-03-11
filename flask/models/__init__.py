from .tables import init_tables
from .tables import db, tb_device_type, tb_factory, tb_data_aging

from .views import query_aging_all_from_view
from .views import init_views

def init_models(app):
    init_tables(app)
    init_views(app)
