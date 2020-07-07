def init_apis(app):
    from app.apis.api_db import api_db
    from app.apis.api_cmd import api_cmd
    from app.apis.api_notice import api_notice
    api_db.init_app(app)
    api_cmd.init_app(app)
    api_notice.init_app(app)
