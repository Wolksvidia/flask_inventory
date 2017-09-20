# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms import validators
from wtforms.fields.html5 import EmailField
#from models import User, Location, Device


#esta funcion verifica que el campo este vacio
def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe ser vacio.')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comentario')
    #el siguiente campo tiene una validacion personalizada
    honeypot = HiddenField('', [length_honeypot])
"""
    username = StringField('Username',
        [
        validators.DataRequired(message='El usuario es requerido.'),
        validators.Length(min=4, max=25, message='Ingrese un usuario valido.'),
        ])
    email = EmailField('Email',
        [
        validators.DataRequired(message='El email es requerido.'),
        validators.Email(message='Ingrese un email valido.')
        ])
"""


class LoginForm(FlaskForm):
    username = StringField('Username',
        [
        validators.DataRequired(message='El usuario es requerido.')
        ])
    password = PasswordField('Password',
        [
        validators.DataRequired(message='La password es requerida.')
        ])


class CreateUserForm(FlaskForm):
    username = StringField('Username',
        [
        validators.DataRequired(message='El usuario es requerido.'),
        validators.Length(min=4, max=50, message='Ingrese un usuario valido.'),
        ])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = EmailField('Email',
        [
        validators.DataRequired(message='El email es requerido.'),
        validators.Email(message='Ingrese un email valido.'),
        validators.Length(min=4, max=50, message='Ingrese un email valido.')
        ])
    phone = StringField('Telephone number')
    staff = BooleanField('Is Staff')
    password = PasswordField('Password',
        [
        validators.EqualTo('confirm', message='Las passwords deben coincidir!!')
        ])
    confirm = PasswordField('Repita la Password')
    location = SelectField('Location', coerce=int)

    #def validate_username(form, field):
        #username = field.data
        #user = User.query.filter_by(username=username).first()
        #if user is not None:
            #raise validators.ValidationError('El usuario ya se encuentra registrado!')



class CreateDevice(FlaskForm):
    name = StringField('Device Name', [
        validators.DataRequired(message='El nombre es requerido.'),
        validators.Length(min=4, max=50, message='Ingrese un usuario valido.'),
        ])
    serial_number = StringField('Serial Number')
    description = TextAreaField('Description')
    teamviwer = StringField('Id Teamviwer')
    location = SelectField('Location', coerce=int)
    type_device = SelectField('Device Type', default='',
        choices=[('dk', 'Deskltop'), ('lp', 'Laptop'), ('imp', 'Impresora')])
    marca = StringField('Marca')
    model = StringField('Model')
    system = SelectField('System', default='', choices=[('wx', 'Windows XP'),
        ('w7', 'Windows 7'), ('w8', 'Windows 8/8.1'),
        ('ws03', 'Windows Server 2003/R2'), ('ws08', 'Windows Server 2008/R2'),
        ('ws12', 'Windows Server 2012/R2'), ('w10', 'Windows 10'),
        ('ld', 'Linux Debian')])

    def validate_name(form, field):
        name = field.data
        device = Device.query.filter_by(name=name).first()
        if device is not None:
            raise validators.ValidationError('El nombre ya se encuentra registrado!')

    def validate_serial_number(form, field):
        serial_number = field.data
        if serial_number is not "":
            device = Device.query.filter_by(serial_number=serial_number).first()
            if device is not None:
                raise validators.ValidationError('El numero de serie ya se encuentra registrado!')

    def validate_teamviwer(form, field):
        num = field.data
        if num is not "":
            if len(num) == 9:
                device = Device.query.filter_by(teamviwer=num).first()
                if device is not None:
                    raise validators.ValidationError('El id ya se encuentra registrado!')
            else:
                raise validators.ValidationError('El id debe tener 9 caracteres!')


class UpdateDevice(FlaskForm):
    name = StringField('Device Name', [
        validators.DataRequired(message='El nombre es requerido.'),
        validators.Length(min=4, max=50, message='Ingrese un usuario valido.'),
        ])
    serial_number = StringField('Serial Number')
    description = TextAreaField('Description')
    teamviwer = StringField('Id Teamviwer')
    location = SelectField('Location', coerce=int)
    type_device = SelectField('Device Type', default='',
        choices=[('dk', 'Desktop'), ('lp', 'Laptop')])
    marca = StringField('Marca')
    model = StringField('Model')
    system = SelectField('System', default='', choices=[('wx', 'Windows XP'),
        ('w7', 'Windows 7'), ('w8', 'Windows 8/8.1'),
        ('ws03', 'Windows Server 2003/R2'), ('ws08', 'Windows Server 2008/R2'),
        ('ws12', 'Windows Server 2012/R2'), ('w10', 'Windows 10'),
        ('ld', 'Linux Debian')])


class CreateLocation(FlaskForm):
    name = StringField('Location Name',[
        validators.DataRequired(message='El nombre es requerido.'),
        ])

    def validate_name(form, field):
        name = field.data
        location = Location.query.filter_by(location_name=name).first()
        if location is not None:
            raise validators.ValidationError('La locacion ya se encuentra registrado!')


class AssignDevice(FlaskForm):
    user = SelectField('Users', coerce=int)
    device = SelectField('Devices', coerce=int)
    notify = BooleanField('¿Notificar al usuario?')
    #user_list = FieldList(users)
    #device_list = FieldList(devices)