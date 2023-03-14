import datetime
import xml.etree.ElementTree

from typing import Any

import numpy as np
import pandas as pd
import xmlschema

from . import jvfdtm
from . import xmlgen


def _first_element(schema: xmlschema.XMLSchema) -> xmlschema.XsdElement:
    elements = [child for child in schema.iterchildren()]

    return elements[0]


class _JvfdtmObjectGenerator(xmlgen.XmlGenerator):
    def __init__(self, data, seed=1):
        self.data = data
        self.seed = seed

    def _generate_id(self):
        id = f"ID{str(self.seed).zfill(17)}"

        self.seed += 1

        return id

    def generate(self, element: xmlschema.XsdElement):
        local_name = element.local_name

        match local_name:
            case "ZapisObjektu":
                return "i"
            case "DatumVkladu":
                return datetime.datetime.now().isoformat()
            case "TridaPresnostiPoloha" | "TridaPresnostiVyska":
                return 9
            case "GeometrieObjektu":
                id = self._generate_id()
                positions = list(map(float, self.data["XYZ"].split(" ")))

                return {
                    "gml:curveProperty": {
                        "gml:LineString": {
                            "@gml:id": id,
                            "@srsDimension": 3,
                            "@srsName": "EPSG:5514",
                            "gml:posList": positions
                        }
                    }
                }
            case "SpolecneAtributyVsechObjektu":
                return {
                    "atr:ID": "00000000000000006",
                    "atr:IDZmeny": "2",
                    "atr:PopisObjektu": None,
                    "atr:IDEditora": "2",
                    "atr:DatumVkladu": "2022-01-31T10:00:00",
                    "atr:VkladOsoba": "vlo\u017eil",
                    "atr:DatumZmeny": "2022-01-31T10:00:00",
                    "atr:ZmenaOsoba": "zm\u011bnil",
                    "atr:DatumPlatnosti": "2022-01-31T10:00:00"
                }
            case "SpolecneAtributyObjektuTI":
                return {
                    "atr:IDVlastnika": "1",
                    "atr:IDProvozovateleZeZakona": None,
                    "atr:IDSpravce": None,
                    "atr:IDProvozovatele": None,
                    "atr:IDExterni": "1",
                    "atr:NeuplnaData": 0,
                    "atr:TridaPresnostiPoloha": 3,
                    "atr:TridaPresnostiVyska": 3,
                    "atr:UrovenUmisteniObjektuTI": -1,
                    "atr:EvidencniCisloObjektu": "1"
                }

        if local_name in self.data:
            return self.data[local_name]

        raise xmlgen.UnsupportedOperationError


class _JvfdtmEntryGenerator(xmlgen.XmlGenerator):
    def __init__(self, objects: dict) -> None:
        self.objects = objects
    
    def generate(self, element: xmlschema.XsdElement) -> Any:
        local_name = element.local_name

        match local_name:
            case "DatumZapisu":
                return datetime.datetime.now().isoformat()
            case "TypZapisu":
                return "kompletní zápis"
            case "OntologickyKatalogObjektuJVFDTM":
                return "https://jvfdtm.ogibeta2.gov.cz/SpravaJVFDTM/ontology/prostorovy_objekt/"
            case "KatalogObjektuJVFDTM":
                return "https://jvfdtm.ogibeta2.gov.cz/SpravaJVFDTM/data-model-management/1"
            case "Data":
                return self.objects
            case "DoprovodneInformace":
                return None
            case "ExtenzeJVFDTM":
                return None

        raise xmlgen.UnsupportedOperationError


def _nan_to_none(value):
    if value is np.nan:
        return None

    return value


def xlsx_to_jvfdtm(df: pd.DataFrame):
    rows = list(row for _, row in df.iterrows())
    attr_names = rows[2][1:]
    objects = {}
    namespaces = {
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }

    for row in rows[4:]:
        attr_values = map(_nan_to_none, row[1:])

        data = dict(zip(attr_names, attr_values))
        type_name = data.pop("ObjektovyTypNazev")
        object_type = jvfdtm.ObjectType.find(type_name)
        schema = object_type.schema
        element = _first_element(schema)
        prefixed_name = "objtyp:TrasaKanalizacniSite"
        object = xmlgen.generate_object(
            element,
            _JvfdtmObjectGenerator(data)
        )

        namespaces.update(schema.namespaces)
        print(prefixed_name)

        if prefixed_name not in objects:
            objects[prefixed_name] = []

        objects[prefixed_name].append(object)

    namespaces.update({"objtyp": "objtyp"})
    del namespaces["xs"]
    del namespaces["xml"]
    element = jvfdtm._XSD_INDEX.elements["JVFDTM"]
    entry = xmlgen.generate_object(
        element,
        _JvfdtmEntryGenerator(objects),
        namespaces=namespaces
    )
    del entry["objtyp:DataJVFDTM"]["dopinf:DoprovodneInformace"]
    del entry["ext:ExtenzeJVFDTM"]

    path = "/{objtyp}JVFDTM"
    with open("/app/data/jvfdtm/xml/gen_entry.json", "w", encoding="utf-8") as stream:
        import json
        json.dump(entry, stream, indent=2)
    etree = xmlschema.to_etree(entry, schema=jvfdtm._XSD_INDEX, path=path)
    print(xml.etree.ElementTree.tostring(etree, encoding="utf-8"))

    return objects
