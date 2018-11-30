# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

dbm = SQLAlchemy()


class CRUD():
    """Clase para la implementacion de las operciones de DB Add, Update,
    Delete como metodos desde los objetos"""
    def add(self):
        dbm.session.add(self)
        return dbm.session.commit()

    def update(self):
        return dbm.session.commit()

    def delete(self):
        dbm.session.delete(self)
        return dbm.session.commit()


class User(dbm.Model, CRUD):
    __tablename__ = 'users'
    id = dbm.Column(dbm.Integer, primary_key=True)
    username = dbm.Column(dbm.String(50), unique=True)
    first_name = dbm.Column(dbm.String(40))
    last_name = dbm.Column(dbm.String(40))
    email = dbm.Column(dbm.String(40))
    phone = dbm.Column(dbm.String(40))
    password = dbm.Column(dbm.String(120))
    create_date = dbm.Column(dbm.DateTime, default=datetime.datetime.now)
    staff = dbm.Column(dbm.Boolean)
    location = dbm.Column(dbm.Integer, dbm.ForeignKey('locations.id'))
    device_id = dbm.relationship('Device', back_populates='user')
    comment_id = dbm.relationship('Comment', back_populates='user')

    def __init__(self, username, email, password=None, staff=False,
        first_name=None, last_name=None, location=None, phone=None):
            self.username = username
            self.email = email
            self.password = self._create_password(password)
            self.staff = staff
            self.first_name = first_name
            self.last_name = last_name
            self.location = location
            self.phone = phone

    def __repr__(self):
        return '<User %r>' % self.username

    def _create_password(self, password):
        """Genera un hash a paratir de la password"""
        return generate_password_hash(password)

    def verify_password(self, password):
        """Verifica que la password suministrada
        concuerde con la almacenada"""
        return check_password_hash(self.password, password)

    def json(self):
        """Genera un diccionario con los datos del objeto User
        para poder ser transformados a json"""
        datos = {}
        datos['id'] = self.id
        datos['username'] = self.username
        datos['first_name'] = self.first_name
        datos['last_name'] = self.last_name
        datos['email'] = self.email
        datos['phone'] = self.phone
        return datos


class Comment(dbm.Model, CRUD):
    __tablename__ = 'comments'
    id = dbm.Column(dbm.Integer, primary_key=True)
    text = dbm.Column(dbm.Text)
    create_date = dbm.Column(dbm.DateTime)
    user_id = dbm.Column(dbm.Integer, dbm.ForeignKey('users.id'))
    user = dbm.relationship('User', back_populates='comment_id')
    device_id = dbm.Column(dbm.Integer, dbm.ForeignKey('devices.id'))
    device = dbm.relationship('Device', back_populates='comments')

    def __init__(self, user, device, text):
        self.user_id = user
        self.device_id = device
        self.text = text
        self.create_date = datetime.datetime.now()


class Location(dbm.Model, CRUD):
    __tablename__ = 'locations'
    id = dbm.Column(dbm.Integer, primary_key=True)
    location_name = dbm.Column(dbm.String(50), unique=True)

    def __init__(self, name):
        self.id = None
        self.location_name = name

    def __repr__(self):
        return '<Location %r>' % self.location_name

    def json(self):
        """Genera un diccionario con los datos del objeto Location
        para poder ser transformados a json"""
        datos = {}
        datos['id'] = self.id
        datos['name'] = self.location_name
        return datos


class Device(dbm.Model, CRUD):
    __tablename__ = 'devices'
    id = dbm.Column(dbm.Integer, primary_key=True)
    name = dbm.Column(dbm.String(50), unique=True)
    marca = dbm.Column(dbm.String(50))
    model = dbm.Column(dbm.String(50))
    serial_number = dbm.Column(dbm.String(50))
    description = dbm.Column(dbm.Text)
    system = dbm.Column(dbm.String(20))
    teamviwer = dbm.Column(dbm.String(9))
    location = dbm.Column(dbm.Integer, dbm.ForeignKey('locations.id'))
    type_device = dbm.Column(dbm.String(4))
    active = dbm.Column(dbm.Boolean)
    user_id = dbm.Column(dbm.Integer, dbm.ForeignKey('users.id'))
    user = dbm.relationship('User', back_populates='device_id')
    comments = dbm.relationship('Comment', back_populates='device')

    def __init__(self, name, description, type_device, serial_number, teamviwer,
        location, marca, model, system):
        self.id = None
        self.name = name
        self.description = description
        self.type_device = type_device
        self.active = True
        self.assigned_to = None
        self.serial_number = serial_number
        self.teamviwer = teamviwer
        self.location = location
        self.model = model
        self.marca = marca
        self.system = system

    def __repr__(self):
        return '<Device %r>' % self.name

    def resolv_type(self):
        """Metodo que devuelve el tipo de dispositivo de manera legible por
        humanos"""
        choice = {'dk': 'Desktop', 'lp': 'Laptop', 'imp': 'Impresora'}
        return choice[self.type_device]

    def resolv_system(self):
        """Metodo que devuelve el nombre del sistema operativo"""
        choice = {'wx': 'Windows XP', 'w7': 'Windows 7', 'w8': 'Windows 8/8.1',
            'w2003Server': 'Windows Server 2003/R2',
            'w2008Server': 'Windows Server 2008/R2',
            'w2012Server': 'Windows Server 2012/R2', 'w10': 'Windows 10',
            'ld': 'Linux Debian'}
        return choice[self.system]

    def json(self):
        """Genera un diccionario con los datos del objeto Device
        para poder ser transformados a json"""
        datos = {}
        datos['id'] = self.id
        datos['name'] = self.name
        datos['type_device'] = self.resolv_type()
        datos['active'] = self.active
        datos['model'] = self.model
        datos['marca'] = self.marca
        datos['system'] = self.resolv_system()
        datos['description'] = self.description
        return datos