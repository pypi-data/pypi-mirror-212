from types import (
    NoneType, FunctionType, LambdaType,
    MethodType, CodeType, CellType, ModuleType, EllipsisType, GeneratorType
)

PRIMITIVE_TYPES: tuple = (int, float, complex, str, bool, NoneType, EllipsisType)
TYPE_MAPPING = {
    'int': int,
    'float': float,
    'complex': complex,
    'str': str,
    'bool': bool,
    'NoneType': NoneType,
    'ellipsis': EllipsisType,
    'bytes': bytes,
    'list': list,
    'tuple': tuple,
    'set': set,
    'dict': dict,
    'code': CodeType,
    'cell': CellType,
    'function': FunctionType,
    'lambda': LambdaType,
    'method': MethodType,
    'staticmethod': staticmethod,
    'classmethod': classmethod,
    'type': type,
    'module': ModuleType,
    'object': object,
    'property': property,
    "generator": GeneratorType
}