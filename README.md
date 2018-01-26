# flask_inventory
![Travis](https://img.shields.io/travis/Wolksvidia/flask_inventory.svg)
[![BCH compliance](https://bettercodehub.com/edge/badge/Wolksvidia/flask_inventory?branch=master)](https://bettercodehub.com/)https://img.shields.io/teamcity/codebetter/bt428.svg
Deployed on Heroku: https://flask-inventory.herokuapp.com (User: admin | password: admin)
Aplicación de inventario y gestion de asignacion de equipos informaticos. Construida principalmente con fines didacticos y de uso particular en la empresa en la que trabajo.
Se utilizo Flask, Boostrap3 y la libreria JQuery DataTables.
Se implento una pequeña api con Flask-Restful para posibilitar el relevamiento de los equipos de forma automatica, distribuyendo un escript a los equipos mediante un dominio Windows. El escript "get_data_machine.py" utiliza la libreria urllib3.
