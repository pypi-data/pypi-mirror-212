"""Serialization of Lab_3"""
import re
from types import NoneType, EllipsisType
from typing import Iterator

from .base import Serializer
from yahalloLib.utils.templates import JSON, XML, XML_PRIMITIVE
from yahalloLib.utils.constants import PRIMITIVE_TYPES, TYPE_MAPPING


class JSONSerializer(Serializer):
    """JSON serializer class."""
    _TYPE_PATTERN: str = r"<class '(\w\S+)'>_"
    _KEYWORDS: dict[None | bool, str] = {
        None: 'null',
        True: 'true',
        False: 'false'
    }

    def __init__(self):
        super().__init__()

    @classmethod
    def _to_number(cls, s: str) -> int | float | complex | None:
        for num_type in (int, float, complex):
            try:
                return num_type(s)
            except (ValueError, TypeError):
                pass

    def _load_from_json(self, template: str) -> dict:
        """Takes a string of specific format (visit ``utils.templates``
        for more clarity) as an input, loads object data,
        and returns it in the form of dict.

        :param template: string template to retrieve object from.
        :return: dictionary with object data.
        """
        obj: dict = {}
        lines: list[str] = template.split("\n")
        it: Iterator[str] = enumerate(lines)

        for i, line in it:
            if not re.search(r'\s*(.+):\s*([^,]*)', line):
                continue

            key, value = re.search(r'\s*(.+):\s*([^,]*)', line).groups()

            if value != "{":
                obj[self.loads(key)] = self.loads(value)

            elif value == "{" and "<class" not in key:
                brackets = 1
                start = i + 1

                while brackets and i < len(lines) - 1:
                    i, line = next(it, None)
                    brackets += ("{" in lines[i]) - ("}" in lines[i])

                obj[self.loads(key)] = self.loads('\n'.join(lines[start:i]))

        return obj

    def dumps(self, obj) -> str:
        """Dumps an object to a string and returns the string.
        Dumping is done via general JSON object template. It can
        overcomplicate simple structure serialization, but can be
        applied to much larger scale of python objects.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        if type(obj) == str:
            return f'"{obj}"'
        if type(obj) == type(Ellipsis):
            return ' '
        if type(obj) in (int, float, complex):
            return str(obj)
        if type(obj) in [bool, NoneType]:
            return self._KEYWORDS[obj]

        return JSON.format(
            type=type(obj) if type(obj) in TYPE_MAPPING.values() else object,
            id=id(obj),
            items=self.formatter.to_json(self.get_items(obj), self.dumps)
        )

    def loads(self, s: str):
        """Loads an object from a string and returns it.
        Operates using JSON template from ``utils.templates``.
        However, primitive types are serialized without this
        or any other template.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        if not len(s):
            return

        if s == ' ':
            return ...
        if s.startswith('"'):
            return s.strip('"')
        if s in self._KEYWORDS.values():
            return self._get_key(s, self._KEYWORDS)
        if self._to_number(s) is not None:
            return self._to_number(s)

        return self.create_object(
            self._type_from_str(s, self._TYPE_PATTERN),
            self._load_from_json(s)
        )


class XMLSerializer(Serializer):
    _TYPE_PATTERN: str = r'type="(\w+)"'

    def _get_tag(self, tagname: str, lines) -> str:
        counter = 1
        it = enumerate(lines)

        for i, line in it:
            if not counter:
                return lines[:i]

            counter += bool(re.search(rf"<{tagname}.*>", line.strip("\t\n ")))
            counter -= bool(re.search(rf"</{tagname}>", line.strip("\t\n ")))

    def _load_from_xml(self, template: str) -> dict:
        obj: dict = {}
        lines: list[str] = template.split("\n")
        it: Iterator[str] = enumerate(lines)

        for i, line in it:
            if "<item>" == line.strip("\t\n "):
                item = self._get_tag("item", lines[i+1:])
                key = self._get_tag("key", item[1:])
                value = self._get_tag("value", item[len(key)+2:])

                obj[self.loads("\n".join(key[:-1]))] = self.loads("\n".join(value[:-1]))

                [next(it, None) for _ in range(len(item))]

        return obj

    def dumps(self, obj) -> str:
        """Dumps an object to a string and returns the string.

        Dumping is done via string templates with XML prefix in
        ``utils.templates`` module.

        :param obj: object to dump.
        :return: string containing serialized (dumped) object.
        """
        if type(obj) in PRIMITIVE_TYPES:
            obj_type = self._get_key(type(obj), TYPE_MAPPING)
            return f'<primitive type="{obj_type}">{obj}</primitive>'

        return XML.format(
            type=self._get_key(type(obj), TYPE_MAPPING) if type(obj) in TYPE_MAPPING.values() else "object",
            id=id(obj),
            items=self.formatter.to_xml(self.get_items(obj), self.dumps)
        )

    def loads(self, s):
        """Loads an object from a string and returns it.

        Operates using templates with XML prefix from ``utils.templates``.

        :param s: string to extract object from.
        :return: deserialized Python object.
        """
        if not len(s):
            return

        if "primitive" in s.split("\n")[0]:
            obj_data = re.search(
                XML_PRIMITIVE.format(
                    type="\w+",
                    obj="(.*)"
                ), s).group(1)
            obj_type = self._type_from_str(
                s=s.split("\n")[0],
                pattern=self._TYPE_PATTERN
            )

            if obj_type == NoneType:
                return None

            if obj_type == bool:
                return obj_data == "True"

            if obj_type == EllipsisType:
                return ...

            return obj_type(obj_data)

        return self.create_object(
            self._type_from_str(s, self._TYPE_PATTERN),
            self._load_from_xml(s)
        )