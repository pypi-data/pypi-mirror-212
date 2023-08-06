__all__ = ['MedicalVisit']

import datetime
from dataclasses import dataclass
from smartjs.functions import *
from dhint import *
from dmodel import *
from .user import *
from .profile import *

@dmcontext
@dataclass
class MedicalVisit(DetaModel):
    EXIST_PARAMS = 'patient_key start'
    SINGULAR = 'Visita Médica'
    PLURAL = 'Visitas Médicas'
    patient_key: Patient = KeyValidator(required=True, label='Paciente')
    date: datetime.date = DateValidator(required=True, default_factory=datetime.date.today, label='Data da Consulta')
    start: datetime.datetime = DateTimeValidator(
            required=True,
            default_factory=lambda : datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3))).isoformat()[:16],
            label='Início'
    )
    main_complaint: str = StringValidator(label='Queixa Principal')
    intro: str = TextAreaValidator(label='Introdução')
    subjective: str = TextAreaValidator(label='Sintomas')
    treatment: str = TextAreaValidator(label='Tratamentos')
    response: str = TextAreaValidator(label='Resposta Terapêutica')
    complement: str = TextAreaValidator(label='Dados Complementares')
    context: str = TextAreaValidator(label='Contexto de Vida')
    objective: str = TextAreaValidator(label='Exame Médico')
    assessment: str = TextAreaValidator(label='Análise')
    plan: str = TextAreaValidator(label='Plano Terapêutico')
    creator: User = KeyValidator(item_name='provider', default='zjhm79ltaw87')
    # provider_key: User = KeyValidator()
    next: int = IntValidator(default=60)
    end: datetime.datetime = DateTimeValidator()
    key: str = SelfKeyValidator()
    
    def __post_init__(self):
        if not self.end:
            self.end = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3))).isoformat()[:16]
            
    def __lt__(self, other):
        return self.date < other.date
    
    def __str__(self):
        return f'Visita {self.patient} dia {self.date}'



@dmcontext
@dataclass
class Event(DetaModel):
    EXIST_PARAMS = 'key'
    SINGULAR = 'Evento'
    patient_key: Patient = KeyValidator()
    name: str = TextAreaValidator()
    age: float = FloatValidator()
    key: str = SelfKeyValidator()
    creator: User = KeyValidator(item_name='provider', default='zjhm79ltaw87')

    
    def __lt__(self, other):
        return self.age < other.age