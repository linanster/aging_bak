from flask_restful import Api, Resource, marshal_with, fields, reqparse, abort
import json, copy, datetime, time
import subprocess as s

from app.lib.mydecorator import viewfunclog
from app.lib.mylogger import logger_app
from app.lib.execsql import set_eventdone_sql
from app.lib.cloudhandler import check_gecloud_connection
from app.lib.tools import set_gecloud_online, reset_gecloud_online

api_notice = Api(prefix='/api/notice/')

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

class ResourceNoticeEventdone(Resource):
    @viewfunclog
    def post(self):
        set_eventdone_sql()
        return {
            'notice': 'page received event done',
            'status': 'ok',
        }

class ResourceNoticeUpdateGEcloudOnline(Resource):
    @viewfunclog
    def post(self):
        if check_gecloud_connection():
            set_gecloud_online()
            msg = 'gecloud online and sqlite updated'
        else:
            reset_gecloud_online()
            msg = 'gecloud not online and sqlite updated'
        return {
            'msg': msg,
            'status': 'ok',
        }


##############################
### 4. Resourceful Routing ###
##############################


api_notice.add_resource(ResourceNoticeEventdone, '/eventdone', endpoint='api_notice_eventdone')
api_notice.add_resource(ResourceNoticeUpdateGEcloudOnline, '/updategecloudonline', endpoint='api_notice_updategecloudonline')

