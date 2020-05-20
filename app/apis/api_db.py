from flask_restful import Api, Resource, marshal_with, fields, reqparse, abort
import json, copy, datetime

from app.models.mysql import Factory, Device, Testdata
from app.lib.mydecorator import viewfunclog

api_db = Api(prefix='/api/db/')

#####################################################################
### 1. fields definition, for marshal (custom object serializing) ###
#####################################################################

fields_factory_db = {
    'code': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

fields_device_db = {
    'code_dec': fields.Integer(attribute='code'),
    'name': fields.String,
    'code_hex': fields.String,
    'factorycode': fields.Integer,
    'description': fields.String
}

fields_testdatacloud_db = {
    'id': fields.Integer,
    'devicecode': fields.Integer,
    'factorycode': fields.Integer,
    'fw_version': fields.String,
    'rssi_ble1': fields.Integer,
    'rssi_ble2': fields.Integer,
    'rssi_wifi1': fields.Integer,
    'rssi_wifi2': fields.Integer,
    'mac_ble': fields.String,
    'mac_wifi': fields.String,
    'status_cmd_check1': fields.Integer,
    'status_cmd_check2': fields.Integer,
    'bool_uploaded': fields.Boolean,
    'bool_qualified_signal': fields.Boolean,
    'bool_qualified_check': fields.Boolean,
    'bool_qualified_scan': fields.Boolean,
    'bool_qualified_deviceid': fields.Boolean,
    'bool_qualified_scan': fields.Boolean,
    # todo format datetime string
    'datetime': fields.DateTime(dt_format='iso8601'),
    'reserve_int_1': fields.Integer,
    'reserve_str_1': fields.String,
    'reserve_bool_1': fields.Boolean
}

fields_factory_list_response = {
    'status': fields.Integer,
    'msg': fields.String,
    # 'data': fields.Nested(fields_factory_db)
    'data': fields.List(fields.Nested(fields_factory_db))
}

fields_device_list_response = {
    'status': fields.Integer,
    'msg': fields.String,
    # 'data': fields.Nested(fields_device_db)
    'data': fields.List(fields.Nested(fields_device_db))
}

fields_testdatacloud_response = {
    'status': fields.Integer,
    'msg': fields.String,
    # 'data': fields.Nested(fields_testdatacloud_db)
    'data': fields.List(fields.Nested(fields_testdatacloud_db))
}


########################################
### 2. request parser initialization ###
########################################

parser = reqparse.RequestParser()
parser.add_argument('factorycode', type=str, location=['args'])
parser.add_argument('devicecode', type=str, location=['args'])



####################################
### 3. resource class definition ###
####################################


class ResourceFactory(Resource):
    @viewfunclog
    @marshal_with(fields_factory_list_response)
    def get(self, **kwargs):
        response_status = 201
        response_msg = 'all factory data'
        response_db = Factory.query.all()
        response_obj = {
            'status': response_status,
            'msg': response_msg,
            'data': response_db
        }
        return response_obj

class ResourceDevice(Resource):
    @viewfunclog
    @marshal_with(fields_device_list_response)
    def get(self, **kwargs):
        response_status = 201
        response_msg = 'all device data'
        response_db = Device.query.all()
        response_obj = {
            'status': response_status,
            'msg': response_msg,
            'data': response_db
        }
        return response_obj

class ResourceTestdata(Resource):
    @viewfunclog
    @marshal_with(fields_testdatacloud_response)
    def get(self, **kwargs):
        args = parser.parse_args()
        factorycode = args.get('factorycode')
        devicecode = args.get('devicecode')
        if factorycode is not None:
            response_obj = {
                'status': 201,
                'msg': 'al the test data with factorycode {}'.format(factorycode),
                'data': Testdata.query.filter_by(factorycode=factorycode).all() 
            }
            return response_obj
        if devicecode is not None:
            response_obj = {
                'status': 201,
                'msg': 'all the test data with devicecode {}'.format(devicecode),
                'data': Testdata.query.filter_by(devicecode=devicecode).all() 
            }
            return response_obj
        response_obj = {
            'status': 201,
            'msg': 'all the test data',
            'data': Testdata.query.all() 
        }
        return response_obj



##############################
### 4. Resourceful Routing ###
##############################


# api_db.add_resource(ResourceFactory, '/factory')
# api_db.add_resource(ResourceDevice, '/device')
api_db.add_resource(ResourceTestdata, '/testdata')



