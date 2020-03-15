from .tables import init_tables
from .tables import db, db_stage, db_archive, tb_device_type, tb_factory, tb_data_aging, tb_data_aging_stage, tb_data_aging_archive

from .views import init_views
from .views import view, view_data_aging

def init_models(app):
    init_tables(app)
    init_views(app)
