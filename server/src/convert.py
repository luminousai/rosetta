import xml.etree.ElementTree

import pandas as pd
import xmlschema

from . import jvfdtm
from .common import nan_to_none


def xlsx_to_jvfdtm(df: pd.DataFrame):
    rows = list(row for _, row in df.iterrows())
    attr_names = rows[2][1:]
    objects = []

    for row in rows[4:]:
        attr_values = list(map(nan_to_none, row[1:]))

        data = dict(zip(attr_names, attr_values))
        print(data)
        object_type = jvfdtm.ObjectType.find(data["ObjektovyTypNazev"])

        if object_type.id == "trasa_kanalizacni_site":
            data["trkasi:ObjektovyTypNazev"] = data["ObjektovyTypNazev"]
            del data["ObjektovyTypNazev"]

        etree = xmlschema.to_etree(data, schema=object_type.schema)
        print(xml.etree.ElementTree.tostring(etree, encoding="utf-8"))
        # objects.append(object)

    return objects
