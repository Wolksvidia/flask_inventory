from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(40))
    password = db.Column(db.String(120))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    staff = db.Column(db.Boolean)
    #comments = db.relationship('Comment')
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
#cambiar a divice_id
    device_assigned = db.relationship('Device', back_populates='user')

    def __init__(self, username, email, password):
            self.username = username
            self.email = email
            self.password = self._create_password(password)
            self.staff = False

    def __repr__(self):
        return '<User %r>' % self.username

    def _create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.location_name = name

    def __repr__(self):
        return '<Location %r>' % self.location_name


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    serial_number = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    teamviwer = (db.String(9))
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
    type_device = db.column(db.String(50))
    active = db.Column(db.Boolean)
#cambiar a user_id
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='device_assigned')


    def __init__(self, name, description, type_device, serial_number, teamviwer,
        location):
        self.name = name
        self.description = description
        self.type_device = type_device
        self.active = True
        self.assigned_to = None
        self.serial_number = serial_number
        self.teamviwer = teamviwer
        self.location = location

    def __repr__(self):
        return '<Device %r>' % self.name