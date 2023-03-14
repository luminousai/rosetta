from pathlib import Path

from dataclasses import dataclass
from functools import cache

import xmlschema


_XSD_DIR = Path(__file__).parent.parent / "data" / "jvfdtm" / "xsd"
_XSD_INDEX = xmlschema.XMLSchema(_XSD_DIR / "index" / "index.xsd")


@dataclass
class ObjectType:
    id: str
    name: str
    schema: xmlschema.XMLSchema

    @cache
    @staticmethod
    def list():
        object_types = []

        for schema in _XSD_INDEX.imports.values():
            url = schema.source.url

            if "objects" not in url:
                continue

            element = schema.root.find(
                ".//xs:element[@name='ObjektovyTypNazev']",
                schema.namespaces
            )

            id = Path(url).stem
            name = element.attrib["fixed"]

            object_type = ObjectType(id, name, schema)
            object_types.append(object_type)

        return object_types

    @cache
    @staticmethod
    def find(name):
        for object_type in ObjectType.list():
            if object_type.name == name:
                return object_type

        raise NameError
