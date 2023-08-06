__all__ = ['User']

import datetime
from dataclasses import dataclass, InitVar
from dhint import *
from dmodel import *


@dmcontext
@dataclass
class User(DetaModel):
    EXIST_PARAMS = 'username'
    SINGULAR = 'Usuário'
    username: str = StringValidator(hash=True)
    password: bytes = PasswordValidator(private=True)
    profile_key: str = ModelKeyValidator(tables=['Doctor', 'Patient', 'Employee', 'Therapist'])
    created: datetime.datetime = DateTimeValidator(form=False)
    key: str = SelfKeyValidator()
    password_repeat: InitVar[bytes] = InitVarValidator(input_type='password', html_tag='input')

    def __repr__(self):
        return self.repr_string
    
    def __str__(self):
        return '{} ({}, {})'.format(self.username, self.profile.person, self.profile.singular())
    
    @property
    def age(self):
        return self.profile.age


    def __post_init__(self, password_repeat: bytes):
        if password_repeat:
            if isinstance(password_repeat, str):
                password_repeat = password_repeat.encode('utf-8')
            if not (password_repeat == self.password):
                raise ValueError('As senhas digitadas não são iguais')