def init_views(app):
    from .blue_index import blue_index
    from .blue_test import blue_test
    from .blue_manage import blue_manage
    from .blue_about import blue_about
    from .blue_admin import blue_admin
    app.register_blueprint(blue_index)
    app.register_blueprint(blue_test)
    app.register_blueprint(blue_manage)
    app.register_blueprint(blue_about)
    app.register_blueprint(blue_admin)
