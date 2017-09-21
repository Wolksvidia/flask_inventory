from models import User, Location, Device, dbm
from flask import Blueprint, request
from flask_restful import Resource, Api

api_blueprint = Blueprint('inventory_api', __name__)
api = Api(api_blueprint)


class HelloWorld(Resource):

    def get(self):
        return {'Hello': 'World'}


class Users(Resource):

    def get(self, uid=None):
        if uid is None:
            users = User.query.filter(User.username != 'admin').join(Location).add_columns(Location.location_name).order_by(User.username).all()
            lista = []
            for u, l in users:
                user = u.parse_user()
                user['location'] = l
                lista.append(user)
            return lista
        else:
            user = User.query.filter(User.id == uid).join(Location).add_columns(Location.location_name).one_or_none()
            if user is None:
                return None
            else:
                data = user[0].parse_user()
                data['location'] = user[1]
                return data


class DeviceId(Resource):

    def get(self, did=None):
        dev = Device.query.filter(Device.id == did).one_or_none()
        if dev is None:
            return None, 404
        else:
            return dev.parse_device()

    def put(self, did=None):
        return {'id': did}, 200


class Devices(Resource):

    def get(self):
        devs = Device.query.all()
        lista = []
        for d in devs:
            lista.append(d.parse_device())
        return lista

    def post(self):
        #parser = reqparse.RequestParser()
        #parser.add_argument('devs', type=list, location='json')
        lista = request.get_json(force=True)
        dev = Device(name=lista['name'],
                serial_number='',
                description=lista['description'],
                teamviwer='',
                type_device='dk', location=lista['location'],
                marca='', model='',
                system='w7')
                #system=lista['system'])
        try:
            dbm.session.add(dev)
            dbm.session.commit()
        except Exception as e:
            print(e)
            return None, 500
        return dev.parse_device()


class Locations(Resource):

    def get(self, lid=None):
        if lid is None:
            locs = Location.query.all()
            lista = []
            for loc in locs:
                lista.append(loc.parse_location())
            return lista
        else:
            loc = Location.query.filter(Location.id == lid).one_or_none()
            if loc is None:
                return None
            else:
                return loc.parse_location()


#api resources
api.add_resource(HelloWorld, '/api/hello')
api.add_resource(Users, '/api/user', '/api/user/<int:uid>')
api.add_resource(Devices, '/api/device')
api.add_resource(DeviceId, '/api/device/<int:did>')
api.add_resource(Locations, '/api/location', '/api/location/<int:lid>')