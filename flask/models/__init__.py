from .tables import init_tables
from .tables import db, tb_device_type, tb_factory, tb_data_aging

from .views import init_views
from .views import view, view_data_aging
from .views import create_view, delete_view

def init_models(app):
    init_tables(app)
    init_views(app)
