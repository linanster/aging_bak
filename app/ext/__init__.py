from .mysocketio import socketio

def init_ext(app):
    from .bootstrap import bootstrap
    bootstrap.init_app(app)
    socketio.init_app(app)
