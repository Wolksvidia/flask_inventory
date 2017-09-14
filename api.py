from models import User, Location, Device
from flask_restful import Resource


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


class Devices(Resource):

    def get(self, did=None):
        if did is None:
            devs = Device.query.all()
            lista = []
            for d in devs:
                lista.append(d.parse_device())
            return lista
        else:
            dev = Device.query.filter(Device.id == did).one_or_none()
            if dev is None:
                return None
            else:
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