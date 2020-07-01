from flask_restful import Api, Resource, marshal_with, fields, reqparse, abort
import json, copy, datetime, time
import subprocess as s

from app.lib.mydecorator import viewfunclog
from app.lib.mycmd import watch_to_finish, watch_timeout, watch_to_blink, start, kickout_all, blink_single, blink_all, blink_stop, turn_on_all, turn_off_all
from app.lib.tools import get_errno, set_running_state
from app.lib.tools import reset_running_state, reset_errno
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
parser.add_argument('cmd', type=str, location=['args', 'form'])



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
        watch_timeout()
        watch_to_blink()
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

def my_check_output_legacy(cmd):
    try:
        # output = s.check_output([cmd, ])
        cmd_list = cmd.split(' ')
        output = s.check_output(cmd_list)
    except s.CalledProcessError as e:
        return str(e)
    except Exception as e:
        return str(e)
    else:
        # return output.decode('utf-8')
        return output.decode()

def my_check_output(cmd):
    try:
        cmd_list = cmd.split(' ')
        # print('==cmd_list==', cmd_list)
        output = s.check_output(cmd_list, stderr=s.STDOUT)
    except s.CalledProcessError as e:
        # print('==CalledProcessError==')
        return e.output.decode()
    except Exception as e:
        # print('==Exception==')
        # print(type(e))
        try:
            return e.output.decode()
        except:
            return str(e)
    else:
        return output.decode()

class ResourceCmdOnlinecmd(Resource):
    @viewfunclog
    def post(self):
        # cmd = request.form.get('cmd')
        args = parser.parse_args()
        cmd = args.get('cmd')
        output = my_check_output(cmd)
        # print('==cmd==', cmd)
        # print('==output==', output)
        return {
            'msg': 'ok',
            'method': 'post',
            'output': output,
        }


class ResourceCmdReset(Resource):
    @viewfunclog
    def post(self):
        reset_errno()
        reset_running_state()
        return {
            'msg': 'ok',
            'method': 'post',
        }


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
api_cmd.add_resource(ResourceCmdOnlinecmd, '/onlinecmd', endpoint='api_cmd_onlinecmd')
api_cmd.add_resource(ResourceCmdReset, '/reset', endpoint='api_cmd_reset')

