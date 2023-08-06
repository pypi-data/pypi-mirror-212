from __future__ import annotations

__all__ = ['DetaModel']

from contextvars import ContextVar
from typing import ClassVar, Optional, Union, Any, Generator
from dataclasses import dataclass
from starlette.requests import Request
from typing_extensions import Self
from anyio import create_task_group
from dhint import *
from dtbase import *
from .descriptors import *
from .context import *



@dataclass
class JsonBase(BaseDetaModel):

    def json_parse(self) -> Jsonable:
        return json_parse(self)

    def asjson(self) -> Jsonable:
        return self.json_parse()

    def json_dumps(self) -> str:
        return json_dumps(self)
        
    
@dataclass
class DTBase(JsonBase):
    DETA_QUERY: ClassVar[Optional[DetaQuery]] = None
    SEARCH_PARAM: ClassVar[SearchParam] = None
    EXIST_PARAMS: ClassVar[ExistParams] = None
    # TABLEDATA: ClassVar[list[dict]] = None
    TABLEGEN: ClassVar[Generator] = None
    
    def asjson_to_save(self) -> Jsonable:
        return {k: v for k, v in self.json_parse().items() if not k in self.no_db_descriptors()}
    
    @classmethod
    async def get(cls, k: str):
        return await DetaBase(cls.table()).get(k)
    
    @classmethod
    async def fetch_all(cls, query: DetaQuery = None):
        print('{}: fetching all'.format(cls.table()))
        return await DetaBase(cls.table()).fetch_all(query)
    
    @classmethod
    async def fetch(cls, query: DetaQuery = None, _last: str = None, limit: int = 1000):
        return await DetaBase(cls.table()).fetch(query, _last, limit)
    
    @classmethod
    async def tablegen(cls, query: DetaQuery = None):
        return (i for i in await DetaBase(cls.table()).fetch_all(query))
    
    @classmethod
    async def set_tablegen(cls, query: DetaQuery = None):
        # cls.TABLEDATA = await cls.fetch_all(cls.DETA_QUERY)
        cls.TABLEGEN = await cls.tablegen(query)
        
    def string_params_to_query_dict(self, string: str) -> dict:
        keys = string.split()
        return json_parse({k: getattr(self, k) for k in keys if getattr(self, k, None)})
    
    def exist_query(self):
        query = ValueError(f'{type(self).__name__} necessita cadastrar EXIST_PARAMS')

        if self.EXIST_PARAMS:
            if isinstance(self.EXIST_PARAMS, list):
                lquery = list()
                for item in self.EXIST_PARAMS:
                    q = self.string_params_to_query_dict(item)
                    if len(q) > 0:
                        lquery.append(q)
                if len(lquery) == 1:
                    query = lquery[0]
                elif len(lquery) > 1:
                    query = lquery
            else:
                q = self.string_params_to_query_dict(self.EXIST_PARAMS)
                if len(q) > 0:
                    query = q
        else:
            raise query
        return query
    
    async def exist(self):
        return await self.fetch(self.exist_query())
    
    @classmethod
    async def instance_request(cls, request: Request):
        data = await request.form()
        instance = cls.create(**{k: v for k, v in data.items() if not all([k == 'key', any([v is None, v == ''])])})
        return instance
    
    async def save(self):
        new = await DetaBase(self.table()).put(self.asjson_to_save())
        if new:
            await self.set_tablegen()
            return self.create(**new)
        raise ValueError(f'{type(self).__name__}: erro ao salvar o item.')

    async def save_new(self):
        exist = await self.exist()
        if exist.count == 1:
            return exist.items[0]
        elif exist.count > 1:
            raise ValueError(f'{type(self).__name__}: erro ao salvar por exibir mais de um resultado compactível no '
                             f'banco de dados.')
        return await self.save()

    async def delete(self):
        await DetaBase(self.table()).delete(self.get_key)
        await self.set_tablegen()

            
    @classmethod
    async def modelgen(cls: DetaModel, query: DetaQuery = None):
        await model_context.update_context(cls.full_dependants())
        gen = await cls.tablegen(query)
        try:
            while True:
                yield cls.create(**next(gen))
        except StopIteration:
            pass
        
@dataclass
class DependantsBase(DTBase):
    DEPENDANTS: ClassVar[list[DetaModel]] = None
    FULL_DEPENDANTS: ClassVar[list[DetaModel]] = None

    @classmethod
    def dependant_descriptors(cls) -> list[Optional[Union[KeyValidator, ModelKeyValidator]]]:
        return [d for d in cls.descriptors().values() if isinstance(d, (KeyValidator, ModelKeyValidator))]
    
    @classmethod
    def model_dependants(cls):
        if not cls.DEPENDANTS:
            result = ListModel()
            for item in cls.dependant_descriptors():
                result.include(*item.dependants)
            cls.DEPENDANTS = ordered_unique_items_list(result.data)
        return cls.DEPENDANTS
    
    @classmethod
    def full_dependants(cls):
        if not cls.FULL_DEPENDANTS:
            result = ListModel()
            for item in cls.model_dependants():
                result.include(*item.full_dependants())
            result.include(cls.model_dependants())
            result.include(cls)
            cls.FULL_DEPENDANTS = ordered_unique_items_list(result.data)
        return cls.FULL_DEPENDANTS
    

@dataclass
class ComparisionBase(DependantsBase):
    
    @property
    def hash_keys(self):
        return tuple([item.public_name for item in self.hash_descriptors()])
    
    @property
    def hash_tuple(self):
        return tuple([v for k, v in self.asjson().items() if k in self.hash_keys])
    
    def __eq__(self, other):
        return all([type(self) == type(other), hash(self.hash_tuple) == hash(other.hash_tuple)])
    
    def __lt__(self, other):
        return normalize_lower(str(self)) < normalize_lower(str(other))
    
    @classmethod
    def equality_dict(cls, instance: Self):
        return {k: v for k, v in instance.excluded_key_dict(instance) if k in cls.compare_descriptors()}
    
    @classmethod
    def excluded_key_dict(cls, instance: Self):
        return {k:v for k, v in instance.json_parse() if not k == 'key'}


@dataclass
class ContextVarBase(ComparisionBase):
    CTXVAR: ClassVar[ContextVar] = None
    
    @classmethod
    def setup_ctxvar(cls):
        cls.CTXVAR = ContextVar(f'{cls.__name__}Var')
    
    @classmethod
    def ctxvar_set(cls) -> None:
        cls.CTXVAR.set({i['key']: cls.create(**i) for i in list(cls.TABLEGEN)})
    
    @classmethod
    def ctxvar_get(cls, k) -> Optional[Self]:
        return context.get(cls.CTXVAR).get(k)
    
    @classmethod
    def instances(cls) -> list[Self]:
        return sorted([*context.get(cls.CTXVAR).values()])
    
    @classmethod
    def instance(cls, k: str) -> Self:
        return cls.ctxvar_get(k)
    
    @classmethod
    async def ctxrun(cls):
        context.run(cls.ctxvar_set)


@dataclass(repr=False)
class DetaModel(ContextVarBase):
    
    def __repr__(self):
        return self.repr_string
    
    @classmethod
    def instance_list(cls) -> list[Self]:
        return sorted([*cls.ctxvar_get()])

    def option(self, default: str = None, model_key: bool = False):
        selected = 'selected' if self.get_key == default else ""
        if model_key:
            return f'<option {selected} id="{self.table()}.{self.get_key}" value="{self.table()}.{self.get_key}">{str(self)}</option>'
        return f'<option {selected} id="{self.table()}.{self.get_key}" value="{self.get_key}">{str(self)}</option>'
    
    @classmethod
    def options(cls, default: str = None, model_key: bool = False):
        return ''.join([item.option(default, model_key) for item in cls.instances()])
    
    @classmethod
    def base_subclass(cls):
        return DetaModel
    
    @classmethod
    def filter_initfields(cls, data: dict) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k in cls.initfields_names()}
    
    @classmethod
    def initfields_names(cls) -> tuple[str]:
        if not cls.INITFIELDS_NAMES:
            cls.INITFIELDS_NAMES = tuple([k for k in cls.init_fields()])
        return cls.INITFIELDS_NAMES
    
    @classmethod
    def create(cls, *args, **kwargs) -> Optional[Self]:
        return cls(*args, **cls.filter_initfields(kwargs))
    
    def display_data(self):
        for item in self.descriptors().values():
            if not item.private:
                if not isinstance(item, InitVarValidator):
                    if isinstance(item, (KeyValidator, ModelKeyValidator)):
                        yield item.item_name, getattr(self, item.item_name)
                    else:
                        yield item.label, getattr(self, item.public_name)




