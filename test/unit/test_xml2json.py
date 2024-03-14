import pytest

from src.xml2json import XmlToJsonParser


@pytest.fixture
def converter():
    return XmlToJsonParser()


@pytest.mark.parametrize("input, expected_output", [
    ('<ITEM type="object"><ITEM key="foo" type="integer" value="7" /></ITEM>', '{"foo": 7}'),
    ('<ITEM type="object"><ITEM key="foo" type="string" value="7" /></ITEM>', '{"foo": "7"}'),
    ('<ITEM type="object"><ITEM key="foo" type="boolean" value="true" /></ITEM>', '{"foo": true}'),
    ('<ITEM type="object"><ITEM key="foo" type="float" value="1.5" /></ITEM>', '{"foo": 1.5}'),
])
def test_primitive_types(input, expected_output, converter):
    assert converter.convert_xml_to_json(input) == expected_output


@pytest.mark.parametrize("input, expected_output", [
    ('<ITEM type="object" />', '{}'),
    ('<ITEM type="list" />', '[]'),
    ('<ITEM type="list"><ITEM type="integer" value="1" /><ITEM type="integer" value="2" /></ITEM>', '[1, 2]'),
    ('<ITEM type="object"><ITEM key="a" type="integer" value="1" /><ITEM key="b" type="integer" value="2" /></ITEM>',
     '{"a": 1, "b": 2}'),
])
def test_simple_non_primitive_types(input, expected_output, converter):
    assert converter.convert_xml_to_json(input) == expected_output


@pytest.mark.parametrize("input, expected_output", [
    ('<ITEM type="object"><ITEM key="mylist" type="list" /></ITEM>', '{"mylist": []}'),
    ('<ITEM type="list"><ITEM type="list" /></ITEM>', '[[]]'),
    ('<ITEM type="object"><ITEM key="mylist" type="list"><ITEM type="list" /></ITEM></ITEM>', '{"mylist": [[]]}'),
    ('<ITEM type="object"><ITEM key="mylist" type="list"><ITEM type="list"><ITEM type="boolean" value="true" /></ITEM></ITEM></ITEM>', '{"mylist": [[true]]}'),
    ('<ITEM type="object"><ITEM key="mylist" type="list"><ITEM type="boolean" value="true" /></ITEM></ITEM>', '{"mylist": [true]}'),
    ('<ITEM type="object"><ITEM key="mylist" type="list"><ITEM type="object"><ITEM key="a" type="integer" value="1" /></ITEM></ITEM></ITEM>', '{"mylist": [{"a": 1}]}'),
    ('<ITEM type="object"><ITEM key="myobj" type="object" /></ITEM>', '{"myobj": {}}'),
    ('<ITEM type="object"><ITEM key="myobj" type="object"><ITEM key="a" type="integer" value="1" /></ITEM></ITEM>', '{"myobj": {"a": 1}}'),
    ('<ITEM type="object"><ITEM key="myobj" type="object"><ITEM key="nested_obj" type="object" /></ITEM></ITEM>', '{"myobj": {"nested_obj": {}}}'),
])
def test_nested_types(input, expected_output, converter):
    assert converter.convert_xml_to_json(input) == expected_output
