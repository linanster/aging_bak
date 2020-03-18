def init_views(app):
    from .command import blue_command
    from .database import blue_database
    from .nav import blue_nav
    app.register_blueprint(blue_command)
    app.register_blueprint(blue_database)
    app.register_blueprint(blue_nav)

