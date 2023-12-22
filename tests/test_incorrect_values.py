from pytest import mark

from main import convert_text


dataset = [
    ('huit cent douze huit', 'единичный формат следует после числа формата сотен'),
    ('douze cent douze', 'число формата сотен следует после формата 11-19'),
    ('huit cent quatre-vingt huit quatre', 'единичный формат следует после числа формата сотен'),
]


@mark.parametrize('number_text,number', dataset)
def test_incorrect_values(number_text, number):
    assert convert_text(number_text) == number
