__all__ = ['Phone', 'CPF', 'Email']

import re
from dhint.collections import Regex


class CPF(Regex):
    def init_data(self) -> str:
        result = ''.join(re.findall(r'\d', self.initial))
        if len(result) != 11:
            raise ValueError('o cpf deve conter 11 dígitos')
        return '{}.{}.{}-{}'.format(result[:3], result[3:6], result[6:9], result[9:])

class Phone(Regex):
    def init_data(self) -> str:
        return ''.join(re.findall(r'\d', self.initial))
    

class Email(Regex):
    def init_data(self) -> str:
        assert '@' in self.initial
        assert len(re.split(r'@', self.initial)) == 2
        return self.initial.strip()