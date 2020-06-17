def init_apis(app):
    from app.apis.api_db import api_db
    from app.apis.api_cmd import api_cmd
    api_db.init_app(app)
    api_cmd.init_app(app)
