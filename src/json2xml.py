import json
from json import JSONDecodeError
from types import NoneType
from typing import Any
from xml.etree.ElementTree import Element, tostring

from src.exceptions import JsonToXmlConversionException


class JsonToXmlParser:
    python_xml_type_mapping = {
        int: "integer",
        bool: "boolean",
        str: "string",
        float: "float",
        list: "list",
        dict: "object",
        NoneType: "null",
    }

    def _parse_value(self, value: Any) -> str | None:
        if isinstance(value, bool):
            return "true" if value else "false"
        elif value is None:
            return None
        else:
            return str(value)

    def _parse_type(self, value: Any) -> str:
        return self.python_xml_type_mapping[type(value)]

    def _mark_item(self, item: Element, key: str | None, value: Any) -> None:
        if key:
            item.set("key", key)
        item.set("type", self._parse_type(value))

    def _parse_item(self, key: str | None, value: Any) -> Element:
        item = Element("ITEM")
        self._mark_item(item, key, value)
        if isinstance(value, dict):
            for k, v in value.items():
                item.append(self._parse_item(k, v))
        elif isinstance(value, list):
            for v in value:
                item.append(self._parse_item(None, v))
        else:
            if value:
                item.set("value", self._parse_value(value))
        return item

    def convert_to_xml(self, data: str) -> str:
        try:
            data = json.loads(data)
        except JSONDecodeError:
            raise JsonToXmlConversionException(
                message=f"Invalid JSON provided as input. Input: {data}"
            )

        root = Element("ITEM")
        root_type = self._parse_type(data)
        root.set("type", root_type)

        if root_type == "object":
            for key, value in data.items():
                root.append(self._parse_item(key, value))
        elif root_type == "list":
            for v in data:
                root.append(self._parse_item(None, v))
        return tostring(root, encoding="unicode")
