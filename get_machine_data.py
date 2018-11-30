# -*- coding: utf-8 -*-

"""Script destinado a obtener datos del equipo mediante el comando systeminfo,
solo valido en windows, y posterior alta del mismo utilizando la api de la
aplicacion de inventario"""

import platform as pf
import urllib3
import json
import os

URL_BASE = 'http://127.0.0.1:8080'
URL_LOC = '/api/location'
URL_DEV = '/api/device'


def device(loc, desc, marca, modelo):
    """Funcion que arma el diccionario de datos
     para que puedan ser pasados a json"""
    datos = {}
    datos['name'] = pf.node()
    system = pf.system()
    if system == 'Windows':
        datos['system'] = "w" + pf.release()
    elif system == 'Linux':
        datos['system'] = "ld"
    datos['marca'] = marca
    datos['model'] = modelo
    datos['location'] = loc
    datos['description'] = desc
    return datos


http = urllib3.PoolManager()

#obtencion del lista de localidades
#response = http.request('GET', URL_BASE + URL_LOC)
#locations = json.loads(response.data.decode('utf-8'))

#generacion de una lista de id de localidad para usarlo como validacion
#loc_ids = [l.get('id') for l in locations]

#obtencion de los datos del comando systeminfo
command = 'systeminfo'
result = os.popen(command)
datos = result.readlines()

lista = []
desc = ''
marca = ''
modelo = ''

#Modelado de la descripcion a partir de datos del comando systeminfo
for d in datos:
    if d.find('Nombre de host:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)
    if d.find('Nombre del sistema operativo:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)
    if d.find('Versi¢n del sistema operativo:') == 0:
        desc += d.replace('\n', '<BR>').replace('¢', 'o')
        lista.append(d)
    if d.find('Fecha de instalaci¢n original:') == 0:
        desc += d.replace('\n', '<BR>').replace('¢', 'o')
        lista.append(d)
    if d.find('Fabricante del sistema:') == 0:
        desc += d.replace('\n', '<BR>')
        marca = d.split(" ")[-1].split("\n")[0]
        lista.append(d)
    if d.find('Modelo el sistema:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)
        modelo = d.split(" ")[-1].split("\n")[0]
    if d.find('Tipo de sistema:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)
    if d.find('Cantidad total de memoria f¡sica:') == 0:
        desc += d.replace('\n', '<BR>').replace('¡', 'i')
        lista.append(d)
    if d.find('Dominio:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)

#Seleccion y validacion del id de localidad elejido por el usuario
#print(locations)
#lid = eval(input('Ingrese el id de la localidad: '))
#isApple = False if int(lid) in loc_ids else True
#while isApple:
#    print('Seleccione un id correcto')
#    print(locations)
#    lid = eval(input('Ingrese el id de la localidad: '))
#    isApple = False if int(lid) in loc_ids else True

#Armado del diccionario de datos y Codificacion del diccionario a json
r = device(1, desc, marca, modelo)
encoded_data = json.dumps(r).encode('utf-8')

response = http.request('POST', URL_BASE + URL_DEV,
    body=encoded_data, headers={'Content-Type': 'application/json'})

#Imprimo codigo de estado debuento por el servidor y json devuelto por api
print('*=========RESPONSE===========*')
print(response.status)
print(json.loads(response.data.decode('utf-8')))

