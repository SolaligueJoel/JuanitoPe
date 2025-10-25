# JuanitoPe

Aplicación backend ligera construida con Python y Flask. Provee API HTTP y comunicación en tiempo real mediante WebSockets.

## Tabla de contenido
- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Estructura básica del proyecto](#estructura-básica-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Configuración](#configuración)
- [Notas de mantenimiento](#notas-de-mantenimiento)
- [Contacto](#contacto)

## Descripción
Proyecto servidor que expone endpoints REST y soporte en tiempo real con Flask-SocketIO. Usa SQLite por defecto y carga parámetros desde un archivo INI.

## Tecnologías
- Python 3.8+
- Flask
- Flask-SocketIO
- SQLAlchemy (ORM)
- SQLite (almacén por defecto)
- ConfigParser para gestión de configuración (configuracion/config.ini)

## Estructura básica del proyecto
- app.py — punto de entrada y creación de la instancia de SocketIO
- configuracion/ — configuración y utilidades (config.ini, config.py)
- models/ — modelos de datos (p. ej. models/user.py)
- requirements.txt — dependencias

## Requisitos
- Git
- Python 3.8 o superior
- pip

## Instalación y ejecución local

macOS / Linux
```sh
cd /Users/joelsolaligue/Desktop/Proyectos/JuanitoPe
python3 -m venv venv
source venv/bin/activate
pip install -r [requirements.txt](http://_vscodecontentref_/0)
# (Opcional) revisar y ajustar [config.ini](http://_vscodecontentref_/1)
python [app.py](http://_vscodecontentref_/2)