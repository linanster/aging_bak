from flask_restful import Api, Resource, marshal_with, fields, reqparse, abort
import json, copy, datetime, time
import subprocess as s

from app.lib.mydecorator import viewfunclog
from app.lib.mylogger import logger_app
from app.lib.execsql import set_eventdone_sql

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


##############################
### 4. Resourceful Routing ###
##############################


api_notice.add_resource(ResourceNoticeEventdone, '/eventdone', endpoint='api_notice_eventdone')

