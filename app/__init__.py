from flask import Flask
from flask_appbuilder import AppBuilder
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
appbuilder = AppBuilder()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)

    with app.app_context():
        appbuilder.init_app(app, db.session)

        # Importar modelos ANTES de create_all
        from app import models
        db.create_all()

        # Crear roles
        _crear_roles()

        # Registrar vistas
        from app import views

    return app


def _crear_roles():
    roles = ['Admin', 'Supervisor', 'Usuario']
    for rol in roles:
        if not appbuilder.sm.find_role(rol):
            appbuilder.sm.add_role(rol)


            