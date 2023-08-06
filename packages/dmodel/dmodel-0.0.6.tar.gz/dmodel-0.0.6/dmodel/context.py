__all__ = ['model_context', 'dmcontext', 'context', 'ordered_unique_items_list', 'full_setup']

from contextvars import ContextVar, copy_context
from functools import wraps, cache
from anyio import create_task_group, sleep
from dhint import *
from dtbase import DetaBase

context = copy_context()

def ordered_unique_items_list(value: list):
    data = list()
    for item in value:
        if item is not None:
            if not item in data:
                data.append(item)
    return data


class ModelContext(BaseContext):
    
    def model(self, model_name: str):
        return self.get(model_name, None)
    
    def table(self, table: str):
        return self.get(table, None)
    
    def set_model(self, model: type['DetaModel']):
        self[model.class_name()] = model
        self[model.table()] = model
        
    def __setitem__(self, key, value):
        if isdetamodel_type(value):
            super().__setitem__(key, value)
            
    def values(self):
        return ordered_unique_items_list([*super().values()])
    
    @staticmethod
    async def set_tabledata(models: list[type['DetaModel']]):
        async with create_task_group() as tks:
            for m in models:
                if not m.TABLEGEN:
                    tks.start_soon(m.set_tablegen)
        
    @staticmethod
    async def ctxrun(models: list[type['DetaModel']]):
        async with create_task_group() as tks:
            for m in models:
                tks.start_soon(m.ctxrun)
    
    async def update_context(self, models: list[type['DetaModel']] = None):
        models = models or self.values()
        await self.set_tabledata(models)
        await self.ctxrun(models)


model_context = ModelContext()


def dmcontext(cls: type['DetaModel']) -> type['DetaModel']:
    @wraps(cls)
    def wrapper():
        cls.class_setup()
        cls.setup_ctxvar()
        model_context.set_model(cls)
        return cls
    return wrapper()


def full_setup() -> None:
    for cls in model_context.values():
        cls.setup_dependants()
    
    