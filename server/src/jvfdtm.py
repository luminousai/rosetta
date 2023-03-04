from pathlib import Path

from dataclasses import dataclass
from functools import cache

from bs4 import BeautifulSoup


ROOT_DIR = Path(__file__).parent.parent / "data" / "jvfdtm"


@dataclass
class Object:
    id: str
    name: str

    @cache
    @staticmethod
    def list():
        objects = []
        object_dir = ROOT_DIR / "xsd" / "objects"

        for file in object_dir.iterdir():
            with file.open(encoding="utf-8") as stream:
                soup = BeautifulSoup(stream, features="xml")
                element = soup.find(attrs=dict(name="ObjektovyTypNazev"))
                name = element["fixed"]

                obj = Object(file.stem, name)

                objects.append(obj)

        return objects
