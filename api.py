# -*- coding: utf-8 -*-

from models import User, Location, Device
from flask import Blueprint, request
from flask_restful import Resource, Api


class Users(Resource):
    def get(self, uid=None):
        """Se responde a la solicitud con la lista completa de usuarios, si
        uid no fue definido en la url, de lo contrario se devuelve el usuario
        especificado si existe"""
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
    def get(self, did):
        """Se retorna el dispositivo solicitado en la url si es que existe"""
        dev = Device.query.filter(Device.id == did).one_or_none()
        if dev is None:
            return None, 404
        else:
            return dev.parse_device()

    def put(self, did):
        """El metodo obtiene los datos json del dispositvo a acrtualizar
        para la actualizacion se deben suministrar todos los campos del objeto
        """
        dev = Device.query.filter(Device.id == did).one_or_none()
        if dev is None:
            return None, 404
        else:
            lista = request.get_json(force=True)
            dev.name = lista['name']
            dev.marca = lista['marca']
            dev.model = lista['model']
            dev.serial_number = lista['serial_number']
            dev.description = lista['description']
            dev.system = lista['system']
            dev.teamviwer = lista['teamviwer']
            dev.location = lista['location']
            dev.type_device = lista['type_device']
            dev.active = lista['active']
            try:
                dev.update()
            except Exception as e:
                print(e)
                return {'error': 'Lo sentimos un error a ocurrido!'}, 500
            return dev.parse_device()


class Devices(Resource):
    def get(self):
        """Se devuelve lista completa de dispositivos"""
        devs = Device.query.all()
        lista = []
        for d in devs:
            lista.append(d.parse_device())
        return lista

    def post(self):
        """Nota: se deben suministrar los datos en el body con la cabecera
        headers={'Content-Type': 'application/json'}"""
        lista = request.get_json(force=True)
        dev = Device(name=lista['name'],
                serial_number='',
                description=lista['description'],
                teamviwer='',
                type_device='dk', location=lista['location'],
                marca=lista['marca'], model=lista['model'],
                system=lista['system'])
        try:
            dev.add()
        except Exception as e:
            print(e)
            return {'error': 'Lo sentimos un error a ocurrido!'}, 500
        return dev.parse_device()


class Locations(Resource):
    def get(self, lid=None):
        """Se retorna la lista completa de localidades, si un lid valido no es
        suministrado en la url"""
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


api_blueprint = Blueprint('inventory_api', __name__)
api = Api(api_blueprint)

#Lista de recursos de la api
api.add_resource(Users, '/api/user', '/api/user/<int:uid>')
api.add_resource(Devices, '/api/device')
api.add_resource(DeviceId, '/api/device/<int:did>')
api.add_resource(Locations, '/api/location', '/api/location/<int:lid>')