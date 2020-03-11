from .command import blue_command
from .database import blue_database
from .index import blue_index

def init_views(app):
    app.register_blueprint(blue_command)
    app.register_blueprint(blue_database)
    app.register_blueprint(blue_index)

