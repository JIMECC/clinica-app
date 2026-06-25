from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship


class Especialidad(Model):
    __tablename__ = 'especialidad'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200))

    def __repr__(self):
        return self.nombre


class Medico(Model):
    __tablename__ = 'medico'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    especialidad_id = Column(Integer, ForeignKey('especialidad.id'), nullable=False)
    especialidad = relationship('Especialidad')

    def __repr__(self):
        return f'{self.nombre} {self.apellido}'


class Paciente(Model):
    __tablename__ = 'paciente'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date)
    genero = Column(String(10))
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(String(200))

    def __repr__(self):
        return f'{self.nombre} {self.apellido}'


class Medicamento(Model):
    __tablename__ = 'medicamento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200))
    dosis = Column(String(50))

    def __repr__(self):
        return self.nombre


class Cita(Model):
    __tablename__ = 'cita'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    motivo = Column(String(200))
    estado = Column(String(20), default='Pendiente')
    medico_id = Column(Integer, ForeignKey('medico.id'), nullable=False)
    paciente_id = Column(Integer, ForeignKey('paciente.id'), nullable=False)
    medico = relationship('Medico')
    paciente = relationship('Paciente')

    def __repr__(self):
        return f'Cita {self.fecha} - {self.paciente}'


class Diagnostico(Model):
    __tablename__ = 'diagnostico'
    id = Column(Integer, primary_key=True)
    descripcion = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    cita_id = Column(Integer, ForeignKey('cita.id'), nullable=False)
    medicamento_id = Column(Integer, ForeignKey('medicamento.id'))
    cita = relationship('Cita')
    medicamento = relationship('Medicamento')

    def __repr__(self):
        return f'Diagnostico {self.id}'
    

    