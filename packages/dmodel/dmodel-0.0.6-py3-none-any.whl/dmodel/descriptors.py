from __future__ import annotations

__all__ = ['KeyValidator', 'ModelKeyValidator']


from typing import Optional, Callable
from dhint import *
from .context import *


class KeyValidator(Descriptor):
    DATALIST = True
    HTML_TAG = 'input'
    INPUT_TYPE = 'text'

    
    def __init__(self, *args, **kwargs):
        self._item_name: Optional[str] = kwargs.get('item_name', None)
        super().__init__(*args, **kwargs)
    
    def __set__(self, instance, value):
        super().__set__(instance, value)
        if value:
            setattr(instance, self.item_name, self.instance(value))
        else:
            setattr(instance, self.item_name, None)
    
    @property
    def dependants(self):
        return [self.model]
    
    @property
    def model(self) -> 'DetaModel':
        return self.type_hint.expected_type
    
    @property
    def model_name(self):
        return self.model.class_name()
    
    @property
    def item_name(self):
        return self._item_name or self.model.item_name()
    
    def instance(self, value: str) -> Optional['DetaModel']:
        if value:
            return self.model.instance(value)
        return None
    
    def options(self, default=None):
        return ''.join([item.option() for item in self.field_type.instances()])
    
    def datalist_element(self, default: str = None):
        return '<datalist id="{}">{}</datalist>'.format(
                self.datalist_id,
                self.options()
        )


class ModelKeyValidator(Descriptor):
    DATALIST = True
    HTML_TAG = 'input'
    INPUT_TYPE = 'text'
    
    def __init__(self, *args, **kwargs):
        self._item_name = kwargs.get('item_name', None)
        self.tables = kwargs.pop('tables')
        super().__init__(*args, **kwargs)
    
    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)
        setattr(instance, self.item_name, self.instance(value))
    
    @property
    def item_name(self):
        if not self._item_name:
            self._item_name = self.public_name.replace('_key', '')
        if self._item_name == self.public_name:
            self._item_name = f'{self.public_name}_instance'
        return self._item_name
    
    @property
    def dependants(self):
        return [m for m in [model_context.table(table) for table in self.tables] if m]
    
    def instance(self, value: str) -> Optional[BaseDetaModel]:
        if isinstance(value, str):
            if '.' in value:
                table, k = value.split('.')
                assert table in self.tables
                return model_context.table(table).instance(k)
        return None
    
    def options(self, default=None):
        text = ''
        for name in self.tables:
            model = model_context.get(name)
            for item in model.instances():
                text += item.option(None, model_key=True)
        return text
    
    def datalist_element(self):
        return '<datalist id="{}">{}</datalist>'.format(
                self.datalist_id,
                self.options()
        )
    
    @property
    def datalist_id(self):
        return f'{self.item_name}-list'


# class RegexValidator(Validator):
#     HTML_TAG = 'input'
#     INPUT_TYPE = 'text'
    
    
# class BoolValidator(Validator):
#     HTML_TAG = 'input'
#     INPUT_TYPE = 'checkbox'
#     FIELD_TYPE = bool
#
#
# class SearchValidator(AutoUpdateValidator):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._func: Callable = kwargs.pop('func', lambda self: self.search_getter)
#
#
# class InitVarValidator(Validator):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._db = False
#         self._repr = False
#         self._required = False
