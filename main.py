# -*- coding: utf-8 -*-
from flask import Flask, abort
from flask import request
from flask import render_template
from flask import make_response
from flask import session, url_for, redirect, flash
from flask_wtf.csrf import CSRFProtect
#G permite persistir una viriable mientras dure el request
from flask import g, copy_current_request_context
from flask_mail import Mail, Message
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import DevelopmentConfig
from models import db, User, Comment, Location, Device
from helpers import date_format
import flask_excel as excel
import threading
import forms

app = Flask(__name__)
#cargo las configuraciones desde clases
app.config.from_object(DevelopmentConfig)
#app.secret_key = 'estasdelachingadamano'
csrf = CSRFProtect()
csrf.init_app(app)
#csrf = CSRFProtect(app)

#para que la db tome las configuraciones de config
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

mail = Mail(app)


def send_email(username, email):
#Configuracion del email de registro
    msg = Message('Gracias por registrarte!',
        sender=app.config['MAIL_USERNAME'],
        recipients=[email, ])
#renderizo un template como cuerpo de mensaje
    msg.html = render_template('mail.html', user=username)
    mail.send(msg)

with app.app_context():
    db.create_all()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


#Este decorador hace que la funcion se ejecute antes de cualquier otra peticion
@app.before_request
def berfore_request():
#    g.test = 'test'
    if 'username' not in session:
        #endpoint da la ruta a la que se esta queriendo acceder
#        print(request.endpoint)
#        print('El usuario necesita login!!"')
#        flash(('info', 'Solo usuarios autenticados tienen acceso al recurso solicitado.'))
        g.urls = ({'url': 'index', 'name': 'Home'},
            {'url': 'login', 'name': 'Login'},
            {'url': 'create_user', 'name': 'New User'})
#        print(g.urls)
#        return redirect(url_for('login'))
    else:
#        flash(('info', 'Ya estas logueado!'))
#        return redirect(url_for('index'))
        g.urls = ({'url': 'index', 'name': 'Home'},
#            {'url': 'comment', 'name': 'Comment'},
#            {'url': 'view_comments', 'name': 'View Comments'},
            {'url': 'new_location', 'name': 'Locations'},
            {'url': 'new_device', 'name': 'New Device'},
            {'url': 'logout', 'name': 'Logout'})
#        print(g.urls)


#Este se prosesa posteriormente de que se procese la url solicitada
#siempre devuelve el objeto response
@app.after_request
def after_request(response):
#    print(g.test)
    return response


@app.route('/')
@app.route('/index')
def index():
#    print(g.test)
#    print(request.endpoint)
    """
    my_cookie = request.cookies.get('my_cookie', False)
    if my_cookie:
        #imprime el valor de la cookie si existe
        print(my_cookie)"""
    return render_template('index.html', urls=g.urls)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            flash(('primary', 'Bienvenido {}.'.format(username)))
            session['username'] = username
            session['user_id'] = user.id
            return redirect(url_for('index', urls=g.urls))
        else:
            flash(('danger', 'Contraseña o usuario incorrectos.'))
    return render_template('login.html', form=login_form, urls=g.urls)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
    #url_for devuelve la ruta de un recurso, en este caso el de la funcion login
    flash(('info', 'Vuelva pronto!.'))
    return redirect(url_for('index', urls=g.urls))


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    comment_form = forms.CommentForm(request.form)
    #manejando sessiones (como si fuera un diccionario)
#    if 'username' in session:
#        user = session['username']
#        comment_form.username.data = user
    if request.method == 'POST' and comment_form.validate():
        user_id = session['user_id']
        comment = Comment(user_id=user_id,
            text=comment_form.comment.data)
        try:
            db.session.add(comment)
            db.session.commit()
            flash(('success', 'Comentario guardado exitosamente!.'))
            return redirect(url_for('index', urls=g.urls))
        except Exception as e:
            print(e)
            flash(('danger', 'Lo sentimos algo salio mal!.'))
    return render_template('comment.html', form=comment_form, urls=g.urls)


@app.route('/view_comments', methods=['GET'])
@app.route('/view_comments/<int:page>', methods=['GET'])
def view_comments(page=1):
#paginate(pagina inicial, cantidad de registros, pagina invalida)
    per_page = 3
    comment_list = Comment.query.join(User).add_columns(User.username,
        Comment.text, Comment.create_date).paginate(page, per_page, False)
    return render_template('view_comments.html', comments=comment_list,
        activo=page, date_format=date_format, urls=g.urls)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    user_form = forms.CreateUserForm(request.form)
    if request.method == 'POST' and user_form.validate():
        user = User(user_form.username.data,
            user_form.email.data,
            user_form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(('success', 'Usuario creado correctamente.'))

            @copy_current_request_context
            def send_message(username, email):
                send_email(username, email)

            sender = threading.Thread(name='mail_sender',
                target=send_message, args=(user.username, user.email, ))
            sender.start()
            return redirect(url_for('login', urls=g.urls))
        except Exception as e:
            print(e)
            flash(('danger', 'Lo sentimos algo salio mal!.'))
    return render_template('create_user.html', form=user_form, urls=g.urls)


@app.route('/device/new', methods=['GET', 'POST'])
@app.route('/device/new/<int:id>', methods=['GET', 'POST']) #no implementado
def new_device(id=None):
    if id is None:
        form = forms.CreateDevice(request.form)
    else:
        form = forms.UpdateDevice(request.form)
    form.location.choices = [(g.id, g.location_name) for g in Location.query.order_by('location_name').all()]
#    form.assigned_to.choices = [(g.id, g.username) for g in User.query.order_by('username').all()]
    if request.method == 'GET' and id is not None:
        dev = Device.query.filter(Device.id == id).one_or_none()
        if dev is not None:
            #pass
            form.name.data = dev.name
            form.location.data = dev.location
            form.serial_number.data = dev.serial_number
            form.description.data = dev.description
            #form.teamviwer.data = dev.teamviwer
            #form.type_device = dev.type_device
        else:
            abort(404)
    if request.method == 'POST' and form.validate():
        if id is not None:
            dev = Device.query.filter(Device.id == id).one()
            form.populate_obj(dev)
            """
            dev.name = form.name.data
            dev.serial_number = form.serial_number.data
            dev.description = form.description.data
            dev.teamviwe = form.teamviwer.data
            dev.type_device = form.type_device.data
            dev.location = form.location.data"""
        else:
            dev = Device(name=form.name.data, serial_number=form.serial_number.data,
                description=form.description.data, teamviwer=form.teamviwer.data,
                type_device=form.type_device.data, location=form.location.data)
        try:
            db.session.add(dev)
            db.session.commit()
            flash(('success', 'Dispositivo guardado exitosamente!.'))
            return redirect(url_for('new_device', urls=g.urls))
        except Exception as e:
            print(e)
            flash(('danger', 'Lo sentimos algo salio mal!.'))
    return render_template('new_device.html', form=form, urls=g.urls)


@app.route('/device/del/<int:id>')
def del_device(id):
    dev = Device.query.filter(Device.id == id).one_or_none()
    if dev is not None:
        try:
            db.session.delete(dev)
            db.session.commit()
            flash(('success', 'Dispositivo se borro exitosamente!.'))
            return redirect(url_for('new_device', urls=g.urls))
        except Exception as e:
            print(e)
            flash(('danger', 'Lo sentimos algo salio mal!.'))
    return redirect(url_for('new_device', urls=g.urls))


@app.route('/device/assign/<int:id>')
def assign_device(id):
    pass


@app.route('/location/new', methods=['GET', 'POST'])
@app.route('/location/new/<int:id>', methods=['GET', 'POST'])
def new_location(id=None):
    locations = Location.query.order_by('location_name').all()
    form = forms.CreateLocation(request.form)
    if request.method == 'GET' and id is not None:
        loc = Location.query.filter(Location.id == id).one_or_none()
        if loc is not None:
            form.name.data = loc.location_name
        else:
            abort(404)
    if request.method == 'POST' and form.validate():
        if id is not None:
            loc = Location.query.filter(Location.id == id).one()
            loc.location_name = form.name.data
        else:
            loc = Location(name=form.name.data)
        try:
            db.session.add(loc)
            db.session.commit()
            flash(('success', 'Locacion guardado exitosamente!.'))
            return redirect(url_for('new_location', urls=g.urls))
        except Exception as e:
            print(e)
            flash(('danger', 'Lo sentimos algo salio mal!.'))
    return render_template('new_location.html',form=form, urls=g.urls, locations=locations)


@app.route('/location/del/<int:id>')
def del_location(id):
    loc = Location.query.filter(Location.id == id).one_or_none()
    if loc is not None:
        try:
            db.session.delete(loc)
            db.session.commit()
            flash(('success', 'Locacion se borro exitosamente!.'))
            #return render_template('index.html', urls=g.urls)
            return redirect(url_for('new_location', urls=g.urls))
        except Exception as e:
            print(e)
            flash(('danger', 'Lo sentimos algo salio mal!.'))
    #return render_template('index.html', urls=g.urls)
    return redirect(url_for('new_location', urls=g.urls))


@app.route('/params')
def params():
    param = request.args.get('params1', 'no hay')
    return 'El parametro es {}'.format(param)
    #?params1=ALGO


@app.route('/paramsplus/')
@app.route('/paramsplus/<name>/')
@app.route('/paramsplus/<name>/<int:num>/')
def params_plus(name='Default', num=0):
    return 'Bienvenido : {} {}'.format(name, num)
#int:num hace que solo admita un numero como parametro


@app.route('/user/<name>')
def user(name="default"):
    age = 32
    lista = [1, 2, 3, 4, 5, ]
    return render_template('user.html', nombre=name, edad=age, listar=lista)


@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('my_cookie', 'Emiliano')
    return response


@app.route('/excel', methods=['GET'])
def return_excel():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")


@app.route("/excel1", methods=['GET'])
def doexport():
    return excel.make_response_from_tables(db.session, [User, Comment],
        file_type="csv", status=200, file_name='name')


@app.route("/excel2", methods=['GET'])
def docustomexport():
    comment_list = Comment.query.join(User).add_columns(User.username,
        Comment.text, Comment.create_date).all()
    column_names = ['username', 'text', 'create_date']
    return excel.make_response_from_query_sets(comment_list,
        column_names=column_names, file_type="xlsx", file_name='comments')


if __name__ == '__main__':
    manager.run()
    #app.run(port=8000)
