import voluptuous as vol

from voluptuous_form import get_form


def test_int_schema():
    for value in int, vol.Coerce(int):
        assert {'type': 'integer'} == get_form(vol.Schema(value))


def test_str_schema():
    for value in str, vol.Coerce(str):
        assert {'type': 'string'} == get_form(vol.Schema(value))


def test_float_schema():
    for value in float, vol.Coerce(float):
        assert {'type': 'float'} == get_form(vol.Schema(value))


def test_bool_schema():
    for value in bool, vol.Coerce(bool):
        assert {'type': 'boolean'} == get_form(vol.Schema(value))


def test_integer_clamp():
    assert {
        'type': 'integer',
        'value-min': 100,
        'value-max': 1000,
    } == get_form(vol.Schema(
            vol.All(vol.Coerce(int),
                    vol.Clamp(min=100, max=1000))))


def test_length():
    assert {
        'type': 'string',
        'length-min': 100,
        'length-max': 1000,
    } == get_form(vol.Schema(
            vol.All(vol.Coerce(str),
                    vol.Length(min=100, max=1000))))


def test_datetime():
    assert {
        'type': 'datetime',
        'format': '%Y-%m-%dT%H:%M:%S.%fZ',
    } == get_form(vol.Schema(vol.Datetime()))


def test_in():
    assert {
        'type': 'select',
        'options': ['beer', 'wine'],
    } == get_form(vol.Schema(vol.In(['beer', 'wine'])))


def test_dict():
    assert {
        'name': {
            'type': 'string',
            'length-min': 5,
            'required': True,
        },
        'age': {
            'type': 'integer',
            'value-min': 18,
            'required': True,
        },
        'hobby': {
            'type': 'string',
            'default': 'not specified',
            'optional': True,
        }
    } == get_form(vol.Schema({
        vol.Required('name'): vol.All(str, vol.Length(min=5)),
        vol.Required('age'): vol.All(vol.Coerce(int), vol.Range(min=18)),
        vol.Optional('hobby', default='not specified'): str
    }))
