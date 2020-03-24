from .tables import db
from .tables import tb_device_type, tb_factory, tb_data_aging
from .tables import tb_state

from .views import view, view_data_aging

def init_models(app):
    db.init_app(app)
    view.init_app(app)
