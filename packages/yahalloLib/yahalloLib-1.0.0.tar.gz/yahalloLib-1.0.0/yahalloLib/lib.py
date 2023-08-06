import argparse

from yahalloLib.base import Serializer
from yahalloLib.serialize import JSONSerializer, XMLSerializer


def main():
    parser = argparse.ArgumentParser(prog="yahalloLib")
    parser.add_argument('file_from')
    parser.add_argument('file_to')
    parser.add_argument('format_from')
    parser.add_argument('format_to')

    args = parser.parse_args()
    file_from, file_to, format_from, format_to = (
        args.file_from,
        args.file_to,
        args.format_from,
        args.format_to
    )

    format_mapping: dict[str, Serializer] = {
        'json': JSONSerializer(),
        'xml': XMLSerializer()
    }

    with open(file_from, 'r') as ff, open(file_to, 'w+') as ft:
        ser_from: Serializer = format_mapping[format_from]
        ser_to: Serializer = format_mapping[format_to]

        ser_to.dump(ser_from.load(ff), ft)


if __name__ == '__main__':
    filename = "/home/artem/Desktop/file1.json"

    with open(filename, 'w+') as fp:
        JSONSerializer().dump({
            1: "123",
            None: [True, False, "sdf", -11],
            90: 1,
        }, fp)

    main()
