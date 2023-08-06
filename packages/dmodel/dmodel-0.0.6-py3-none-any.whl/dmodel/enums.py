
__all__ = ['Gender', 'GraduationField', 'EmployeeScope']


from dhint.base.base_enum import BaseEnum

class EmployeeScope(BaseEnum):
    SOC = 'Proprietário'
    CLT = 'Funcionário'
    EST = 'Estagiário'
    TER = 'Terceirizado'
    DIA = 'Diarista'

class Gender(BaseEnum):
    M = 'Masculino'
    F = 'Feminino'
    
    
class GraduationField(BaseEnum):
    MED = 'Medicina'
    PSI = 'Psicologia'