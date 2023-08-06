from .constants import PRIMITIVE_TYPES
from yahalloLib.utils.templates import XML_ITEM


class Formatter:

    @staticmethod
    def move_line(string, indent):
        """

        :param string:
        :param indent:
        :return:
        """
        return "\t" * indent + string

    def to_json(self, obj, dumps):
        """

        :param obj:
        :param dumps:
        :return:
        """
        items_repr = ""

        for k, v in obj.items():
            if type(v) in PRIMITIVE_TYPES:
                items_repr += f"\t{dumps(k)}: {dumps(v)},\n"
                continue

            items_repr += f"\t{dumps(k)}: {{\n"

            for line in dumps(v).split("\n")[1:]:
                items_repr += f"{self.move_line(line, 1)}\n"

        return items_repr

    def to_xml(self, obj, dumps):
        items_repr = ""

        for k, v in obj.items():
            items_repr += self.move_line(
                XML_ITEM.format(
                    key=dumps(k),
                    value=dumps(v)
                ), 1)

        return items_repr