from .tables import db, db_stage, db_archive
from .tables import tb_device_type, tb_factory, tb_data_aging, tb_data_aging_stage, tb_data_aging_archive
from .tables import tb_state

from .views import view, view_data_aging

def init_models(app):
    db.init_app(app)
    view.init_app(app)
