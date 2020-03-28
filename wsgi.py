# coding:utf8
#
from app import create_app

application = create_app()

@application.template_global('totalcount')
def totalcount():
    from app.lib import get_totalcount
    return get_totalcount()

@application.template_global('progress')
def progress():
    from app.lib import get_progress
    return get_progress()
