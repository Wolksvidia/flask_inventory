import platform as pf
import urllib3
import json
import os


def device(loc, desc, marca, modelo):
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

response = http.request('GET', 'http://127.0.0.1:5000/api/location')
locations = json.loads(response.data.decode('utf-8'))
loc_ids = []
for l in locations:
    loc_ids.append(l.get('id'))

command = 'systeminfo'
result = os.popen(command)
datos = result.readlines()

lista = []
desc = ''
marca = ''
modelo = ''

for d in datos:
    if d.find('Nombre de host:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)
    if d.find('Nombre del sistema operativo:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)
    if d.find('Versi¢n del sistema operativo:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)
    if d.find('Fecha de instalaci¢n original:') == 0:
        desc += d.replace('\n', '<BR>')
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
        desc += d.replace('\n', '<BR>')
        lista.append(d)
    if d.find('Dominio:') == 0:
        desc += d.replace('\n', '<BR>')
        lista.append(d)

print(locations)
lid = input('Ingrese el id de la localidad: ')
isApple = False if int(lid) in loc_ids else True
while isApple:
    print('Seleccione un id correcto')
    print(locations)
    lid = input('Ingrese el id de la localidad: ')
    isApple = False if int(lid) in loc_ids else True

r = device(lid, desc, marca, modelo)
encoded_data = json.dumps(r).encode('utf-8')
response = http.request('POST', 'http://127.0.0.1:5000/api/device',
    body=encoded_data, headers={'Content-Type': 'application/json'})

print('*=========RESPONSE===========*')
print(response.status)
print(json.loads(response.data.decode('utf-8')))