def init_ext(app):
    from .bootstrap import bootstrap
    from .socketio import socketio
    bootstrap.init_app(app)
    socketio.init_app(app)
