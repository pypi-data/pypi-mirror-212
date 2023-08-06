__all__ = ['Person']

import datetime
import re
from dataclasses import dataclass
from dhint import *
from dmodel import *
from smartjs.functions import age

@dmcontext
@dataclass
class Person(DetaModel):
    SEARCH_PARAM = 'search_name'
    SINGULAR = 'Pessoa'
    fname: str = StringValidator(search=True, required=True, label='Primeiro Nome')
    lname: str = StringValidator(search=True, required=True, label='Sobrenome')
    bdate: datetime.date = Validator(search=True, required=True, label='Nascimento')
    gender: Gender = SelectValidator(search=True, required=True, label='Gênero')
    cpf: CPF = RegexValidator(search=True, label='CPF')
    transgender: bool = BoolValidator(label='Transgênero')
    non_binary: bool = BoolValidator(label='Não Binário')
    name: str = StringValidator(search=True, label='Nome Social')
    key: str = SelfKeyValidator()
    search_name: str = AutoUpdateValidator(func=lambda self: self.search_getter)
    code: str = AutoValidator(func=lambda self: self.code_getter)
    

    def __str__(self):
        return self.fullname
    
    @property
    def code_getter(self):
        return '{}{}{}{}'.format(
                self.gender.name,
                self.bdate.isoformat().replace('-', ''),
                self.fname[:2].upper(),
                self.lname.split()[-1][:2].upper()
        )

    @property
    def fullname(self):
        return self.name if all([self.name is not None, self.name != '']) else f'{self.fname} {self.lname}'
    
    @property
    def age(self):
        return age(self.bdate)
