from .tables import db
from .tables import RunningState, Systeminfo
from .tables import Device, Factory, Testdata

from .views import view, TestdataView

def init_models(app):
    db.init_app(app)
    view.init_app(app)
