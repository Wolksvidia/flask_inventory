from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(40))
    phone = db.Column(db.String(40))
    password = db.Column(db.String(120))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    staff = db.Column(db.Boolean)
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
    device_id = db.relationship('Device', back_populates='user')
    comment_id = db.relationship('Comment', back_populates='user')

    def __init__(self, username, email, password=None, staff=False, first_name=None, last_name=None, location=None, phone=None):
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
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def parse_user(self):
        datos = {}
        datos['id'] = self.id
        datos['username'] = self.username
        datos['first_name'] = self.first_name
        datos['last_name'] = self.last_name
        datos['email'] = self.email
        datos['phone'] = self.phone
        return datos


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='comment_id')
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    device = db.relationship('Device', back_populates='comments')

    def __init__(self, user, device, text):
        self.user_id = user
        self.device_id = device
        self.text = text
        self.create_date = datetime.datetime.now()


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.location_name = name

    def __repr__(self):
        return '<Location %r>' % self.location_name

    def parse_location(self):
        datos = {}
        datos['id'] = self.id
        datos['name'] = self.location_name
        return datos


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    marca = db.Column(db.String(50))
    model = db.Column(db.String(50))
    serial_number = db.Column(db.String(50))
    description = db.Column(db.Text)
    system = db.Column(db.String(10))
    teamviwer = db.Column(db.String(9))
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
    type_device = db.Column(db.String(4))
    active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='device_id')
    comments = db.relationship('Comment', back_populates='device')


    def __init__(self, name, description, type_device, serial_number, teamviwer,
        location, marca, model, system):
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
        choice = {'dk': 'Desktop', 'lp': 'Laptop', 'imp': 'Impresora'}
        return choice[self.type_device]

    def resolv_system(self):
        choice = {'wx': 'Windows XP', 'w7': 'Windows 7', 'w8': 'Windows 8/8.1',
            'ws03': 'Windows Server 2003/R2', 'ws08': 'Windows Server 2008/R2',
            'ws12': 'Windows Server 2012/R2', 'w10': 'Windows 10',
            'ld': 'Linux Debian'}
        return choice[self.system]

    def parse_device(self):
        datos = {}
        datos['id'] = self.id
        datos['name'] = self.name
        datos['type_device'] = self.resolv_type()
        datos['active'] = self.active
        datos['model'] = self.model
        datos['marca'] = self.marca
        datos['system'] = self.resolv_system()
        return datos