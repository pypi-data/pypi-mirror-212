__all__ = ['Facility']


from dataclasses import dataclass
from dhint import *
from dmodel import *


@dmcontext
@dataclass
class Facility(DetaModel):
    SEARCH_PARAM = 'search'
    SINGULAR = 'Empresa'
    name: str = StringValidator(required=True, search=True, label='Nome')
    phone: Phone = RegexValidator(search=True, label='Telefone')
    email: Email = RegexValidator(search=True, label='Email')
    address: str = StringValidator(search=True, label='Endereço')
    city: str = StringValidator(search=True, label='Cidade/Estado')
    cep: str = StringValidator(label='CEP')
    key: str = SelfKeyValidator()
    search: str = SearchValidator()
    
    def __str__(self):
        return '{} ({})'.format(self.name, self.email)

