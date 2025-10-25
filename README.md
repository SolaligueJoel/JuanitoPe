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

1. Clonar el repositorio (fork o remoto)
```sh
# Clonar el repositorio (reemplace <REPO_URL> por la URL del repo o del fork)
git clone <REPO_URL>
cd JuanitoPe
```

2. Crear y activar un entorno virtual, instalar dependencias
macOS / Linux
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Revisar configuración
- Editar configuracion/config.ini según el entorno (host, port, ruta de base de datos, modo debug).
- `configuracion/config.py` inicializa la base de datos y crea el usuario administrador en el primer arranque; revise si necesita ajustes.

4. Ejecutar la aplicación
```sh
python app.py
```
Luego abrir http://{host}:{port} con los valores establecidos en configuracion/config.ini.