import pytest
from src.exceptions import JsonToXmlConversionException
from src.json2xml import JsonToXmlParser


@pytest.fixture
def converter():
    return JsonToXmlParser()


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (
            '{"foo": 7}',
            '<ITEM type="object"><ITEM key="foo" type="integer" value="7" /></ITEM>',
        ),
        (
            '{"foo": -7}',
            '<ITEM type="object"><ITEM key="foo" type="integer" value="-7" /></ITEM>',
        ),
        (
            '{"foo": "7"}',
            '<ITEM type="object"><ITEM key="foo" type="string" value="7" /></ITEM>',
        ),
        ('{"foo": ""}', '<ITEM type="object"><ITEM key="foo" type="string" /></ITEM>'),
        (
            '{"foo": true}',
            '<ITEM type="object"><ITEM key="foo" type="boolean" value="true" /></ITEM>',
        ),
        (
            '{"foo": 1.5}',
            '<ITEM type="object"><ITEM key="foo" type="float" value="1.5" /></ITEM>',
        ),
        (
            '{"foo": -1.5}',
            '<ITEM type="object"><ITEM key="foo" type="float" value="-1.5" /></ITEM>',
        ),
    ],
)
def test_primitive_types(input, expected_output, converter):
    assert converter.convert_to_xml(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("{}", '<ITEM type="object" />'),
        ("[]", '<ITEM type="list" />'),
        (
            "[1,2]",
            '<ITEM type="list"><ITEM type="integer" value="1" /><ITEM type="integer" value="2" /></ITEM>',
        ),
        (
            '{"a": 1, "b": 2}',
            '<ITEM type="object"><ITEM key="a" type="integer" value="1" /><ITEM key="b" type="integer" value="2" /></ITEM>',
        ),
    ],
)
def test_simple_non_primitive_types(input, expected_output, converter):
    assert converter.convert_to_xml(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (
            '{"mylist": []}',
            '<ITEM type="object"><ITEM key="mylist" type="list" /></ITEM>',
        ),
        ("[[]]", '<ITEM type="list"><ITEM type="list" /></ITEM>'),
        (
            '{"mylist": [[]]}',
            '<ITEM type="object"><ITEM key="mylist" type="list"><ITEM type="list" /></ITEM></ITEM>',
        ),
        (
            '{"mylist": [[true]]}',
            '<ITEM type="object"><ITEM key="mylist" type="list"><ITEM type="list"><ITEM type="boolean" value="true" /></ITEM></ITEM></ITEM>',
        ),
        (
            '{"mylist": [true]}',
            '<ITEM type="object"><ITEM key="mylist" type="list"><ITEM type="boolean" value="true" /></ITEM></ITEM>',
        ),
        (
            '{"mylist": [{"a":1}]}',
            '<ITEM type="object"><ITEM key="mylist" type="list"><ITEM type="object"><ITEM key="a" type="integer" value="1" /></ITEM></ITEM></ITEM>',
        ),
        (
            '{"myobj": {}}',
            '<ITEM type="object"><ITEM key="myobj" type="object" /></ITEM>',
        ),
        (
            '{"myobj": {"a": 1}}',
            '<ITEM type="object"><ITEM key="myobj" type="object"><ITEM key="a" type="integer" value="1" /></ITEM></ITEM>',
        ),
        (
            '{"myobj": {"nested_obj": {}}}',
            '<ITEM type="object"><ITEM key="myobj" type="object"><ITEM key="nested_obj" type="object" /></ITEM></ITEM>',
        ),
    ],
)
def test_nested_types(input, expected_output, converter):
    assert converter.convert_to_xml(input) == expected_output


@pytest.mark.parametrize("invalid_json", ["", "{", '{"foo"}', "{{}}"])
def test_invalid_json_input(invalid_json, converter):
    with pytest.raises(JsonToXmlConversionException):
        converter.convert_to_xml(invalid_json)


def test_mixed_input(converter):
    input = """
    {
        "apple": 7,
        "orange": 4.1,
        "other": {
            "banana": "fruit"
        },
        "many": [
            true,
            "thing",
            {
                "pineapple": null
            }
        ]
    }
    """

    output = '<ITEM type="object"><ITEM key="apple" type="integer" value="7" /><ITEM key="orange" type="float" value="4.1" /><ITEM key="other" type="object"><ITEM key="banana" type="string" value="fruit" /></ITEM><ITEM key="many" type="list"><ITEM type="boolean" value="true" /><ITEM type="string" value="thing" /><ITEM type="object"><ITEM key="pineapple" type="null" /></ITEM></ITEM></ITEM>'
    assert converter.convert_to_xml(input) == output
