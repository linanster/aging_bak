from .tables import db
from .tables import Device, Factory, Testdata
from .tables import RunningState

from .views import view, TestdataView

def init_models(app):
    db.init_app(app)
    view.init_app(app)
