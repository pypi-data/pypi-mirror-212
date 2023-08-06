__all__ = ['Patient', 'Doctor', 'Therapist', 'Employee']


from dataclasses import dataclass
from smartjs.functions import *
from dhint import *
from dmodel import *
from .person import *
from .facility import *

@dataclass
class Profile(DetaModel):
    SEARCH_PARAM = 'search'
    EXIST_PARAMS = 'person_key'
    person_key: Person = KeyValidator(search=True, required=True)

    def __str__(self):
        return self.person.fullname
    
    @property
    def age(self):
        return self.person.age
    

@dataclass
class Staff(Profile):
    facility_key: Facility = KeyValidator(required=True)

@dmcontext
@dataclass
class Patient(Profile):
    SINGULAR = 'Paciente'
    phone: Phone = RegexValidator(label='Telefone')
    email: Email = RegexValidator(label='Email')
    address: str = StringValidator(label='Endereço')
    city: str = StringValidator(label='Cidade/Estado')
    notes: str = TextAreaValidator(label='Anotações')
    key: str = SelfKeyValidator()
    search: str = SearchValidator()


@dmcontext
@dataclass
class Doctor(Staff):
    SINGULAR = 'Médico'
    register: str = StringValidator(required=True, label='Registro Profissional')
    university: str = StringValidator(label='Universidade')
    graduation_field: GraduationField = SelectValidator(label='Área de Graduação')
    graduation_year: int = IntValidator(label='Ano de Graduação')
    specialties: list[str] = Validator(label='Especialidades')
    health_insuances: list[str] = Validator(label='Planos de Saúde')  # todo: modificar para health_insurances
    notes: str = TextAreaValidator(label='Anotações')
    key: str = SelfKeyValidator()
    search: str = SearchValidator()
    
    def __str__(self):
        return '{} {} ({})'.format(
                'Dr.' if self.person.gender == Gender.M else 'Dra.',
                str(self.person),
                self.graduation_field.value
        )


@dmcontext
@dataclass
class Therapist(Doctor):
    SINGULAR = 'Terapeuta'


@dmcontext
@dataclass
class Employee(Staff):
    SINGULAR = 'Colaborador'
    scope: EmployeeScope = SelectValidator(required=True, label='Escopo')
    active: bool = BoolValidator(label='Ativo')
    phone: Phone = RegexValidator(label='Telefone')
    email: Email = RegexValidator(label='Email')
    address: str = StringValidator(label='Endereço')
    city: str = StringValidator(label='Cidade/Estado')
    base_value: float = FloatValidator(label='Salário Base', step=0.01, min=0)
    salary_indexed: bool = BoolValidator(label='Base Indexada ao Mínimo')
    days_month: int = IntValidator(label='Dias de Trabalho por Mês')
    hours_day: int = IntValidator(label='Horas de Trabalho por Dia')
    external: bool = BoolValidator(label='Serviços Externos')
    financial: bool = BoolValidator(label='Serviços Financeiros')
    housekeeping: bool = BoolValidator(label='Serviço de Limpeza')
    management: bool = BoolValidator(label='Gerência')
    reception: bool = BoolValidator(label='Recepção')
    telephonist: bool = BoolValidator(label='Telefonista')
    key: str = SelfKeyValidator()
    search: str = SearchValidator()
    
    def __str__(self):
        return '{} ({})'.format(
                str(self.person),
                self.scope.value
        )