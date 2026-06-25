import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Clave secreta
SECRET_KEY = "0000clinica123456789"

# Conexion MySQL XAMPP puerto 3305
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3305/clinicaapp'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-WTF
CSRF_ENABLED = True

# Flask-AppBuilder
AUTH_TYPE = 1
AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLE_PUBLIC = 'Public'
APP_NAME = "Clínica App"
APP_ICON = ""


