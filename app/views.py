from flask_appbuilder import ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.baseviews import BaseView
from flask_appbuilder.security.decorators import has_access
from flask import render_template
from sqlalchemy import func
from . import appbuilder, db
from .models import Especialidad, Medico, Paciente, Medicamento, Cita, Diagnostico
from .api.claude_api import (
    analizar_citas_por_medico,
    analizar_pacientes_por_genero,
    analizar_medicamentos_frecuentes
)


class EspecialidadView(ModelView):
    datamodel = SQLAInterface(Especialidad)
    list_columns = ['nombre', 'descripcion']


class MedicoView(ModelView):
    datamodel = SQLAInterface(Medico)
    list_columns = ['nombre', 'apellido', 'especialidad', 'telefono', 'email']


class MedicamentoView(ModelView):
    datamodel = SQLAInterface(Medicamento)
    list_columns = ['nombre', 'descripcion', 'dosis']


class PacienteView(ModelView):
    datamodel = SQLAInterface(Paciente)
    list_columns = ['nombre', 'apellido', 'genero', 'telefono', 'email']
    label_columns = {
        'nombre': 'Nombre',
        'apellido': 'Apellido',
        'genero': 'Género',
        'telefono': 'Teléfono',
        'email': 'Correo electrónico',
        'fecha_nacimiento': 'Fecha de Nacimiento',
        'direccion': 'Dirección'
    }
    search_columns = ['nombre', 'apellido', 'email']


class CitaView(ModelView):
    datamodel = SQLAInterface(Cita)
    list_columns = ['fecha', 'paciente', 'medico', 'motivo', 'estado']


class DiagnosticoView(ModelView):
    datamodel = SQLAInterface(Diagnostico)
    list_columns = ['fecha', 'cita', 'descripcion', 'medicamento']


class ReporteP1View(BaseView):
    route_base = '/reporte-p1'
    default_view = 'citas_por_medico'

    @expose('/citas_por_medico')
    @has_access
    def citas_por_medico(self):
        datos = (
            db.session.query(
                Medico.nombre,
                Medico.apellido,
                func.count(Cita.id).label('total')
            )
            .join(Cita, Cita.medico_id == Medico.id)
            .group_by(Medico.id)
            .all()
        )
        medicos = [f"{r.nombre} {r.apellido}" for r in datos]
        totales = [r.total for r in datos]
        analisis = analizar_citas_por_medico(medicos, totales)

        return render_template(
            'reportes/citas_por_medico.html',
            datos=datos,
            analisis=analisis
        )


class ReporteP2View(BaseView):
    route_base = '/reporte-p2'
    default_view = 'pacientes_genero'

    @expose('/pacientes_genero')
    @has_access
    def pacientes_genero(self):
        datos = (
            db.session.query(
                Paciente.genero,
                func.count(Paciente.id).label('total')
            )
            .group_by(Paciente.genero)
            .all()
        )
        generos = [r.genero for r in datos]
        totales = [r.total for r in datos]
        analisis = analizar_pacientes_por_genero(generos, totales)

        return render_template(
            'reportes/pacientes_por_genero.html',
            datos=datos,
            analisis=analisis
        )


class ReporteP3View(BaseView):
    route_base = '/reporte-p3'
    default_view = 'medicamentos_frecuentes'

    @expose('/medicamentos_frecuentes')
    @has_access
    def medicamentos_frecuentes(self):
        datos = (
            db.session.query(
                Medicamento.nombre,
                func.count(Diagnostico.id).label('total')
            )
            .join(Diagnostico, Diagnostico.medicamento_id == Medicamento.id)
            .group_by(Medicamento.id)
            .order_by(func.count(Diagnostico.id).desc())
            .limit(10)
            .all()
        )
        medicamentos = [r.nombre for r in datos]
        totales = [r.total for r in datos]
        analisis = analizar_medicamentos_frecuentes(medicamentos, totales)

        return render_template(
            'reportes/diagnosticos_frecuentes.html',
            datos=datos,
            analisis=analisis
        )


# Registro en menú
appbuilder.add_view(EspecialidadView, "Especialidades", icon="fa-stethoscope", category="Administración")
appbuilder.add_view(MedicoView, "Médicos", icon="fa-user-md", category="Administración")
appbuilder.add_view(MedicamentoView, "Medicamentos", icon="fa-pills", category="Administración")
appbuilder.add_view(PacienteView, "Pacientes", icon="fa-users", category="Gestión")
appbuilder.add_view(CitaView, "Citas", icon="fa-calendar", category="Gestión")
appbuilder.add_view(DiagnosticoView, "Diagnósticos", icon="fa-file-medical", category="Gestión")
appbuilder.add_view(ReporteP1View, "Citas por Médico", icon="fa-chart-bar", category="Reportes")
appbuilder.add_link("Pacientes por Género", href='/reporte-p2/pacientes_genero', icon="fa-chart-pie", category="Reportes")
appbuilder.add_link("Medicamentos Frecuentes", href='/reporte-p3/medicamentos_frecuentes', icon="fa-chart-line", category="Reportes")
appbuilder.add_view(ReporteP2View, "Reporte Géneros", icon="fa-chart-pie", category="Reportes")
appbuilder.add_view(ReporteP3View, "Reporte Medicamentos", icon="fa-chart-line", category="Reportes")


