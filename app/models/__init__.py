# from .tables import db
# from .tables import RunningState, Systeminfo
# from .tables import Device, Factory, Testdata, TestdataArchive
# from .views import view, TestdataView, TestdataArchiveView
from .sqlite import db_sqlite, RunningState, Systeminfo
from .mysql import db_mysql, Device, Factory, Testdata, TestdataStage, TestdataArchive

def init_models(app):
    db_sqlite.init_app(app)
    db_mysql.init_app(app)
    db_sqlite.reflect(app=app)
    db_mysql.reflect(app=app)
