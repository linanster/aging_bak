def init_ext(app):
    from .bootstrap import bootstrap
    bootstrap.init_app(app)
