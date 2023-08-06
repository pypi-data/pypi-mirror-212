__all__ = ['group_instances_by', 'group_by_date', 'div_grouped_by']

from itertools import groupby
from smartjs.elements import Div, H4, Ul, Li
from smartjs.base import Text

def group_instances_by(table_data: list['DetaModel'], key: str):
    srt = sorted(table_data, key=lambda x: getattr(x, key))
    grouped = groupby(srt, key=lambda x: getattr(x, key))
    result = []
    for item in grouped:
        result.append({str(item[0]): list(item[1])})
    return result


def div_grouped_by(table_data: list['DetaModel'], key: str):
    div = Div()
    for i in group_instances_by(table_data, key):
        for k, v in i.items():
            div.elements.append(Div(elements=[H4(Text(str(k))), Ul(elements=[Li(Text(str(o))) for o in v])]))
    return div

def group_by_date(table_data: list['DetaModel']):
    grouped = groupby(table_data, key=lambda x: x.date)
    result = []
    for item in grouped:
        result.append({str(item[0]): list(item[1])})
    return result