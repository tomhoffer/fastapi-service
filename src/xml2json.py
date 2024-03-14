import json
import xml.etree.ElementTree as ET
from typing import Any

from src.exceptions import XmlToJsonConversionException


class XmlToJsonParser:

    def _parse_value(self, element: ET.Element) -> Any:
        value = element.get("value")
        if element.get("type") == "integer":
            return int(value)
        elif element.get("type") == "float":
            return float(value)
        elif element.get("type") == "boolean":
            return value.lower() == "true"
        elif element.get("type") == "null":
            return None
        else:
            return value

    def _parse_element(self, element: ET.Element) -> Any:
        if element.get("type") == "object":
            obj = {}
            for child in element:
                obj[child.get("key")] = self._parse_element(child)
            return obj
        elif element.get("type") == "list":
            lst = []
            for child in element:
                lst.append(self._parse_element(child))
            return lst
        else:
            return self._parse_value(element)

    def convert_xml_to_json(self, data: str):
        try:
            root = ET.fromstring(data)
        except ET.ParseError:
            raise XmlToJsonConversionException(message="Invalid XML provided as input.")
        return json.dumps(self._parse_element(root))
