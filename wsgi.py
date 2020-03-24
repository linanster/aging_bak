# coding:utf8
#
from app import create_app

application = create_app()

@application.template_global('running')
def running():
    from app.lib import get_running_state
    return get_running_state()

@application.template_global('paused')
def paused():
    from app.lib import get_paused_state
    return get_paused_state()

