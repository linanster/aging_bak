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

@application.template_global('running')
def running():
    from app.lib import get_running_state
    return get_running_state()

@application.template_global('phase')
def phase():
    from app.lib import get_phase
    return get_phase()

@application.template_global('errno')
def errno():
    from app.lib import get_errno
    return get_errno()
