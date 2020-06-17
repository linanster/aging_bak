from flask_restful import Api, Resource, marshal_with, fields, reqparse, abort
import json, copy, datetime, time

from app.lib.mydecorator import viewfunclog
from app.lib.mycmd import watch_to_finish, start, kickout_all, blink_single, blink_all, blink_stop, turn_on_all, turn_off_all
from app.lib.tools import get_errno, set_running_state
from app.lib.mylogger import logger_app

api_cmd = Api(prefix='/api/cmd/')

#####################################################################
### 1. fields definition, for marshal (custom object serializing) ###
#####################################################################



########################################
### 2. request parser initialization ###
########################################

parser = reqparse.RequestParser()
parser.add_argument('mac', type=str, location=['args'])



####################################
### 3. resource class definition ###
####################################


class ResourceCmdStarttest(Resource):
    @viewfunclog
    def post(self):
        time.sleep(1)
        logger_app.warn('trigger starttest api')
        set_running_state()
        start()
        watch_to_finish()

        response_obj = {
            'errno': get_errno(),
            'cmd': 'starttest',
            'msg': '',
        }
        return response_obj

class ResourceCmdBlinksingle(Resource):
    @viewfunclog
    def post(self):
        args = parser.parse_args()
        mac = args.get('mac')
        logger_app.warn('trigger blink single api')
        errno = blink_single(mac)

        response_obj = {
            'errno': errno,
            'cmd': 'blinksingle',
            'mac': mac,
            'msg': '',
        }
        return response_obj

class ResourceCmdBlinkall(Resource):
    @viewfunclog
    def post(self):
        logger_app.warn('trigger blink all api')
        errno = blink_all()

        response_obj = {
            'errno': errno,
            'cmd': 'blinkall',
            'msg': '',
        }
        return response_obj

class ResourceCmdBlinkstop(Resource):
    @viewfunclog
    def post(self):
        logger_app.warn('trigger blink stop api')
        errno = blink_stop()

        response_obj = {
            'errno': errno,
            'cmd': 'blinkstop',
            'msg': '',
        }
        return response_obj

class ResourceCmdAllon(Resource):
    @viewfunclog
    def post(self):
        logger_app.warn('trigger turn on all api')
        errno = turn_on_all()

        response_obj = {
            'errno': errno,
            'cmd': 'allon',
            'msg': '',
        }
        return response_obj

class ResourceCmdAlloff(Resource):
    @viewfunclog
    def post(self):
        logger_app.warn('trigger turn off all api')
        errno = turn_off_all()

        response_obj = {
            'errno': errno,
            'cmd': 'alloff',
            'msg': '',
        }
        return response_obj

class ResourceCmdAllkickout(Resource):
    @viewfunclog
    def post(self):
        logger_app.warn('trigger allkickout api')
        errno = kickout_all()

        response_obj = {
            'errno': errno,
            'cmd': 'allkickout',
            'msg': '',
        }
        return response_obj



##############################
### 4. Resourceful Routing ###
##############################


api_cmd.add_resource(ResourceCmdStarttest, '/starttest')
api_cmd.add_resource(ResourceCmdBlinksingle, '/blinksingle')
api_cmd.add_resource(ResourceCmdBlinkall, '/blinkall')
api_cmd.add_resource(ResourceCmdBlinkstop, '/blinkstop')
api_cmd.add_resource(ResourceCmdAllon, '/allon')
api_cmd.add_resource(ResourceCmdAlloff, '/alloff')
api_cmd.add_resource(ResourceCmdAllkickout, '/allkickout')



