def init_ext(app):
    from .bootstrap import bootstrap
    from .nav import nav
    bootstrap.init_app(app)
    nav.init_app(app)
