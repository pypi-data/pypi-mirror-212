from __future__ import annotations

__all__ = ['FormField', 'HTMLForm', 'HTMXForm']

from abc import ABC
from typing import Any, Union
from dataclasses import dataclass
from dhint import *
from .descriptors import *

@dataclass
class FormField(ABC):
    descriptor: Descriptor
    
    @property
    def field_type(self):
        return self.descriptor.field_type
    
    @property
    def element_tag(self):
        return self.descriptor.html_tag
    
    @property
    def input_type(self):
        return self.descriptor.input_type
    
    @property
    def label_class(self):
        if self.input_type == 'checkbox':
            return 'form-check-label'
        return 'form-label'
    
    @property
    def label(self):
        return self.descriptor.label_element or ''
    
    @property
    def element_class(self):
        return self.descriptor.field_bs_class
    
    @property
    def required(self):
        return 'required' if self.descriptor.is_required else ''
    
    @property
    def field_id(self):
        return f'{self.descriptor.public_name}__field'
    
    @property
    def public_name(self):
        return self.descriptor.public_name
    
    def datalist(self):
        if self.descriptor.datalist:
            return self.descriptor.datalist_element()
        return ''
    
    def select_field(self, value=''):
        return f'<select {self.required} id="{self.field_id}" name="{self.public_name}" class="{self.element_class}">' \
               f'{self.field_type.options(value)}</select>{self.label}'
    
    def textarea_field(self, value=None):
        return f'<textarea {self.required} id="{self.field_id}" name="{self.public_name}" ' \
               f'class="{self.element_class}" style="height: {self.descriptor.height}">{value}</textarea>{self.label}'
    
    def key_or_modelkey_field(self, value=None):
        return f'<input {self.required} id="{self.field_id}" list="{self.descriptor.datalist_id}" ' \
               f'name="{self.descriptor.public_name}" type="{self.input_type}" ' \
               f'class="{self.element_class}" {self.value(value)}>{self.label}{self.datalist()}'
        
    def hidden_field(self, value=''):
        return f'<input {self.required} id="{self.field_id}" name="{self.descriptor.public_name}" {self.value(value)} ' \
               f'type="{self.input_type}">'
    
    def range_or_checkbox_field(self, value=""):
        return f'{self.label}<input {self.required} id="{self.field_id}" name="{self.descriptor.public_name}" {self.value(value)}' \
               f'type="{self.input_type}" class="{self.element_class}">'
    
    def number_field(self, value=''):
        return f'<input {self.required} id="{self.field_id}" name="{self.descriptor.public_name}" ' \
               f'type="{self.input_type}" class="{self.element_class}" {self.value(value)}' \
               f' {self.step} {self.min} {self.max}>{self.label}'
    
    def input_field(self, value=''):
        return f'<input {self.required} id="{self.field_id}" name="{self.descriptor.public_name}" ' \
               f'type="{self.input_type}" class="{self.element_class}" {self.value(value)}">{self.label}'
    
    @property
    def step(self):
        val = getattr(self.descriptor, 'step', None)
        return '' if val is None else f'step="{val}"'
    
    def value(self, v: Any):
        if any([v is not None, v != '']):
            if self.descriptor.is_input:
                if self.input_type == 'checkbox':
                    return 'checked' if v is True else ''
                return f'value="{v}"'
            return v
        return ''
    
    @property
    def min(self):
        val = getattr(self.descriptor, 'min', None)
        return '' if val is None else f'min="{val}"'
    
    @property
    def max(self):
        val = getattr(self.descriptor, 'max', None)
        return '' if val is None else f'max="{val}"'
    
    def render(self, value: Any = None):
        if self.element_tag == 'select':
            return self.select_field(value)
        elif self.element_tag == 'input':
            if isinstance(self.descriptor, (KeyValidator, ModelKeyValidator)):
                return self.key_or_modelkey_field(value)
            elif self.input_type in ['range', 'checkbox']:
                return self.range_or_checkbox_field(value)
            elif self.input_type == 'number':
                return self.number_field(value)
            return self.input_field(value)
        elif self.element_tag == 'textarea':
            return self.textarea_field(value)
        return ''


@dataclass
class HTMLForm:
    model: Union[BaseDetaModel, type[BaseDetaModel]]
    action: str
    method: str
    delete: bool = False
    search: bool = False
    
    @property
    def _action(self):
        return f'action="{self.action}"'
    
    def form(self, form_fields):
        if self.search:
            method = 'get'
            name = f'Search{self.model.class_name()}'
        else:
            method = 'post'
            if self.delete:
                name = f'Delete{self.model.class_name()}'
            elif isdataclass_instance(self.model):
                name = f'Update{self.model.class_name()}'
            else:
                name = f'New{self.model.class_name()}'
        return f'{self.title}<form id="{name}" method="{method}" {self._action}>' \
               f'{"".join([self.container(item) for item in form_fields])}{self.button}</form>'
    
    @property
    def title(self):
        if self.search:
            return f'<h2>Buscar {self.model.singular()}</h2>'
        elif self.delete:
            return f'<h2>Apagar {self.model.singular()}</h2>'
        elif isdataclass_instance(self.model):
            return f'<h2>Atualizar {self.model.singular()}</h2>'
        return f'<h2>Adicionar {self.model.singular()}</h2>'
    
    def defaults(self):
        if isdetamodel_instance(self.model):
            return {k: getattr(self.model, k) for k in self.model.fields_names()}
        else:
            return {item.public_name: item.get_default() for item in self.model.descriptors().values()}
    
    @property
    def button(self):
        if self.search:
            return f'<button class="btn form-control search">buscar</button>'
        elif self.delete:
            return f'<button class="btn form-control delete">apagar</button>'
        elif isdataclass_instance(self.model):
            return f'<button class="btn form-control update">atualizar</button>'
        return f'<button class="btn form-control new">adicionar</button>'
    
    @staticmethod
    def container(form_field: str):
        return f'<div class="form-floating mb-2">{remove_extra_whitespaces(form_field)}</div>'
    
    def render(self, defaults: dict = None):
        if not defaults:
            defaults = self.defaults()
        defaults = {k: '' if v is None else v for k,v in defaults.items()}
        if self.search:
            form_fields = [FormField(item).render(defaults.get(item.public_name, '')) for item in
                           self.model.descriptors().values() if issearchfield(item)]
        elif self.delete:
            form_fields = [f'<h3>Apagar {str(self.model)}</h3>']
        else:
            if defaults:
                form_fields = [FormField(item).render(defaults.get(item.public_name, '')) for item in
                               self.model.descriptors().values() if not item in self.model.no_form_descriptors()]
            else:
                form_fields = [FormField(item).render(item.get_default()) for item in
                               self.model.descriptors().values() if not item in self.model.no_form_descriptors()]
        return self.form(form_fields)


@dataclass
class HTMXForm(HTMLForm):
    
    @property
    def _action(self):
        return f'data-hx-{self.method}="{self.action}"'