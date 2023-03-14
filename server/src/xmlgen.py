from typing import Any, Optional

from xmlschema.validators import (
    XsdAtomic,
    XsdAtomicRestriction,
    XsdComplexType,
    XsdElement
)


def _build_root(namespaces: Optional[dict]) -> dict:
    root = {}

    if namespaces is None:
        return root

    for key, value in namespaces.items():
        if not key:
            continue

        root[f"@xmlns:{key}"] = value

    return root


class XmlGenerationError(Exception):
    pass


class UnsupportedOperationError(XmlGenerationError):
    def __init__(
            self,
            element: Optional[XsdElement] = None
    ) -> None:
        if element is not None:
            super().__init__(
                f"Can't generate object of type {element.prefixed_name}"
            )
        else:
            super().__init__()


class XmlGenerator:
    def generate(self, element: XsdElement) -> Any:
        raise UnsupportedOperationError


def generate_object(
        element: XsdElement,
        generator: XmlGenerator,
        namespaces: Optional[dict] = None
) -> dict:
    result = _build_root(namespaces)

    if element.type.content_type_label == "simple":
        result["$"] = element.fixed

        for name, attribute in element.attributes.items():
            result[f"@{name}"] = attribute.fixed

        return result

    for child in element.iterchildren():
        result[child.prefixed_name] = generate(child, generator)

    return result


def generate_value(element: XsdElement) -> Any:
    if element.fixed:
        return element.fixed

    if isinstance(element.type, XsdAtomicRestriction):
        enumeration = element.type.enumeration

        if len(enumeration) == 1:
            return enumeration[0]

    raise UnsupportedOperationError(element)


def generate(element: XsdElement, generator: XmlGenerator) -> Any:
    try:
        return generator.generate(element)
    except UnsupportedOperationError:
        pass

    match element.type:
        case XsdComplexType():
            return generate_object(element, generator)
        case XsdAtomic():
            return generate_value(element)

    raise UnsupportedOperationError(element)
