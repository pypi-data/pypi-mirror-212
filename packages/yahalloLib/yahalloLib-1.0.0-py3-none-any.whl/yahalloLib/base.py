import re
from abc import ABC, abstractmethod
from types import NoneType, FunctionType, MethodType, CodeType, ModuleType,\
    CellType, BuiltinMethodType, BuiltinFunctionType, WrapperDescriptorType, \
    MethodDescriptorType, MappingProxyType, GetSetDescriptorType, MemberDescriptorType, GeneratorType
from typing import Any, IO, Hashable, Collection, Iterable

from yahalloLib.utils.constants import TYPE_MAPPING
from yahalloLib.utils.helpers import Formatter


class Serializer(ABC):
    _IGNORED_FIELDS: set[str] = (
        '__weakref__',
        '__subclasshook__',
        '__dict__',
        '__doc__'
    )
    _IGNORED_FIELD_TYPES: set[str] = (
        BuiltinFunctionType, BuiltinMethodType,
        WrapperDescriptorType, MethodDescriptorType,
        MappingProxyType, GetSetDescriptorType,
        MemberDescriptorType
    )
    formatter = Formatter()

    @staticmethod
    def _get_key(value: Hashable, obj: dict):
        return [key for key in obj if obj[key] == value][0]

    @classmethod
    def _type_from_str(cls, s: str, pattern: str) -> type:
        if not re.search(pattern, s):
            return NoneType

        return TYPE_MAPPING[re.search(pattern, s).group(1)]

    def get_items(self, obj) -> dict[str, Any]:
        """

        :param obj:
        :return:
        """
        if isinstance(obj, (BuiltinFunctionType, BuiltinMethodType)):
            return {}

        if isinstance(obj, dict):
            return obj

        elif isinstance(obj, Collection):
            return dict(enumerate(obj))

        elif isinstance(obj, CodeType):
            return {
                "argcount": obj.co_argcount,
                "posonlyargcount": obj.co_posonlyargcount,
                "kwonlyargcount": obj.co_kwonlyargcount,
                "nlocals": obj.co_nlocals,
                "stacksize": obj.co_stacksize,
                "flags": obj.co_flags,
                "code": obj.co_code,
                "consts": obj.co_consts,
                "names": obj.co_names,
                "varnames": obj.co_varnames,
                "filename": obj.co_filename,
                "name": obj.co_name,
                "firstlineno": obj.co_firstlineno,
                "lnotab": obj.co_lnotab,
                "freevars": obj.co_freevars,
                "cellvars": obj.co_cellvars,
            }

        elif isinstance(obj, property):
            return {
                "getter": obj.fget,
                "setter": obj.fset,
                "deleter": obj.fdel
            }

        elif isinstance(obj, GeneratorType):
            a = []
            for i in obj:
                a.append(i)
            return{
                "values":a
            }

        elif isinstance(obj, FunctionType):
            if obj.__closure__ and "__class__" in obj.__code__.co_freevars:
                closure = ([... for _ in obj.__closure__])
            elif obj.__closure__:
                closure = ([cell.cell_contents for cell in obj.__closure__])
            else:
                closure = None

            return {
                "argcount": obj.__code__.co_argcount,
                "posonlyargcount": obj.__code__.co_posonlyargcount,
                "kwonlyargcount": obj.__code__.co_kwonlyargcount,
                "nlocals": obj.__code__.co_nlocals,
                "stacksize": obj.__code__.co_stacksize,
                "flags": obj.__code__.co_flags,
                "code": obj.__code__.co_code,
                "consts": obj.__code__.co_consts,
                "names": obj.__code__.co_names,
                "varnames": obj.__code__.co_varnames,
                "filename": obj.__code__.co_filename,
                "name": obj.__code__.co_name,
                "firstlineno": obj.__code__.co_firstlineno,
                "lnotab": obj.__code__.co_lnotab,
                "freevars": obj.__code__.co_freevars,
                "cellvars": obj.__code__.co_cellvars,
                "globals": {
                    k: obj.__globals__[k]
                    for k in (
                        set(
                            k for k, v in obj.__globals__.items()
                            if isinstance(v, ModuleType)
                        ) |
                        set(obj.__globals__) &
                        set(obj.__code__.co_names) -
                        {obj.__name__}
                    )
                },
                "closure": closure,
                "qualname": obj.__qualname__
            }

        elif isinstance(obj, MethodType):
            return {
                "__func__": obj.__func__,
                "__self__": obj.__self__
            }

        elif issubclass(type(obj), type):
            return {
                'name': obj.__name__,
                'mro': tuple(obj.mro()[1:-1]),
                'attrs': {
                    k: v for k, v in obj.__dict__.items()
                    if (
                        k not in self._IGNORED_FIELDS and
                        type(v) not in self._IGNORED_FIELD_TYPES
                    )
                }
            }

        elif issubclass(type(obj), ModuleType):
            return {'name': obj.__name__}

        elif isinstance(obj, staticmethod):
            return self.get_items(obj.__func__)

        elif isinstance(obj, classmethod):
            return self.get_items(obj.__func__)

        else:
            return {
                'class': obj.__class__,
                'attrs': {
                    k: v for k, v in obj.__dict__.items()
                    if (
                        k not in self._IGNORED_FIELDS and
                        type(k) not in self._IGNORED_FIELD_TYPES
                    )
                }
            }

    # noinspection PyArgumentList,PyUnresolvedReferences
    def create_object(self, obj_type: type, obj_data):
        if issubclass(obj_type, dict):
            return obj_data

        elif issubclass(obj_type, GeneratorType):
            return (x for x in obj_data["values"])

        elif issubclass(obj_type, Iterable):
            return obj_type(obj_data.values())

        elif issubclass(obj_type, CodeType):
            return CodeType(*list(obj_data.values()))

        elif issubclass(obj_type, FunctionType):
            if obj_data.get('closure'):
                closure = tuple([CellType(x) for x in obj_data.get('closure')])
            elif obj_data.get('closure') and '__class__' in obj_data.get('freevars'):
                closure = tuple([CellType(...) for _ in obj_data.get('closure')])
            else:
                closure = tuple()

            obj = FunctionType(
                code=CodeType(*list(obj_data.values())[:16]),
                globals=obj_data.get('globals'),
                name=obj_data['name'],
                closure=closure
            )
            obj.__qualname__ = obj_data.get('qualname')
            obj.__globals__[obj.__name__] = obj

            return obj

        elif issubclass(obj_type, property):
            return property(fget=obj_data.get("getter"), fdel=obj_data.get("deleter"), fset=obj_data.get("setter"))

        elif issubclass(obj_type, MethodType):
            return MethodType(
                obj_data.get('__func__'),
                obj_data.get('__self__'),
            )

        elif issubclass(obj_type, (staticmethod, classmethod)):
            return self.create_object(FunctionType, obj_data)

        elif issubclass(obj_type, type):
            obj = type(obj_data.get('name'), obj_data.get('mro'), obj_data.get('attrs'))

            try:
                obj.__init__.__closure__[0].cell_contents = obj
            except (AttributeError, IndexError):
                ...

            return obj

        elif issubclass(obj_type, ModuleType):
            return __import__(obj_data.get('name'))

        else:
            obj = object.__new__(obj_data.get('class'))
            obj.__dict__ = obj_data.get('attrs')

            return obj

    def dump(self, obj: Any, fp: IO[str]) -> None:
        """Dumps an object to .json file.

        :param obj: object to dump.
        :param fp: json file object.
        """
        fp.write(self.dumps(obj))

    def load(self, fp: IO[str]):
        """Loads an object from .json file.

        :param fp: json file object to extract object from.
        :return: deserialized Python object.
        """
        return self.loads(fp.read())

    @abstractmethod
    def dumps(self, obj) -> str:
        """Dumps an object to a string and returns the string.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        raise NotImplementedError

    @abstractmethod
    def loads(self, s):
        """Loads an object from a string and returns it.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        raise NotImplementedError