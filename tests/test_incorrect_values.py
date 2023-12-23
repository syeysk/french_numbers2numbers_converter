from itertools import chain

from pytest import mark

from main import convert_text, DIGITS

REVERSED_DIGITS = {v: k for k, v in DIGITS.items()}
FORMAT_11_19 = {
    11: 'onze',
    12: 'douze',
    13: 'treize',
    14: 'quatorze',
    15: 'quinze',
    16: 'seize',
    17: 'dix-sept',
    18: 'dix-huit',
    19: 'dix-neuf',
}
FORMAT_TENS = {
    20: 'vingt',
    30: 'trente',
    40: 'quarante',
    50: 'cinquante',
    60: 'soixante',
    70: 'soixante-dix',
    80: 'quatre-vingt',
    90: 'quatre-vingt-dix',
}

dataset = [
    ('huit cent douze huit', 'единичный формат следует после формата 11-19'),
    ('douze cent douze', 'число формата сотни следует после формата 11-19'),
    ('huit cent quatre-vingt huit quatre', 'единичный формат следует после единичного формата'),
    ('cent quatre-vingt huit un', 'единичный формат следует после единичного формата'),
    ('cinq cent cinq cent', 'число формата сотни следует после единичного формата'),
    ('huit cent dix dix', 'десятичный формат следует после десятичного формата'),
    ('dix un', 'единичный формат следует после десятичного формата'),
    ('cinq cent soixante-quinze un', 'единичный формат следует после единичного формата'),
    ('soixante-et-onze soixante-douze', 'десятичный формат следует после единичного формата'),
    ('soixante et onze un', 'единичный формат следует после единичного формата'),
]


@mark.parametrize('number_text,number', dataset)
def test_incorrect_values_by_hardcode(number_text, number):
    assert convert_text(number_text) == number


def gen_cases_after_one(ones=''):
    if ones:
        ones = f'{ones} '

    for number in range(10):
        number = REVERSED_DIGITS[number]
        for useless_number in range(10):
            useless_number = REVERSED_DIGITS[useless_number]
            yield f'{ones}cent {number} {useless_number}', 'единичный формат следует после единичного формата'

        for useless_number in FORMAT_11_19.values():
            yield f'{ones}cent {number} {useless_number}', 'формат 11-19 следует после единичного формата'

        for useless_number in FORMAT_TENS.values():
            yield f'{ones}cent {number} {useless_number}', 'десятичный формат следует после единичного формата'


@mark.parametrize(
    'number_text,number',
    chain(gen_cases_after_one(), *[gen_cases_after_one(REVERSED_DIGITS[number]) for number in range(2, 10)]),
)
def test_incorrect_values_after_one(number_text, number):
    assert convert_text(number_text) == number


def gen_cases_after_11_19(ones=''):
    if ones:
        ones = f'{ones} '

    for number in FORMAT_11_19.values():
        for useless_number in range(10):
            useless_number = REVERSED_DIGITS[useless_number]
            yield f'{ones}cent {number} {useless_number}', 'единичный формат следует после формата 11-19'

        for useless_number in FORMAT_11_19.values():
            yield f'{ones}cent {number} {useless_number}', 'формат 11-19 следует после формата 11-19'

        for useless_number in FORMAT_TENS.values():
            yield f'{ones}cent {number} {useless_number}', 'десятичный формат следует после формата 11-19'

        yield f'{ones}cent {number} cent', 'число формата сотни следует после формата 11-19'


@mark.parametrize(
    'number_text,number',
    chain(gen_cases_after_11_19(), *[gen_cases_after_11_19(REVERSED_DIGITS[number]) for number in range(2, 10)]),
)
def test_incorrect_values_after_11_19(number_text, number):
    assert convert_text(number_text) == number


def gen_cases_after_tens(ones=''):
    if ones:
        ones = f'{ones} '

    for number in FORMAT_TENS.values():
        for useless_number in FORMAT_11_19.values():
            yield f'{ones}cent {number} {useless_number}', 'формат 11-19 следует после десятичного формата'

        for useless_number in FORMAT_TENS.values():
            yield f'{ones}cent {number} {useless_number}', 'десятичный формат следует после десятичного формата'

        yield f'{ones}cent {number} cent', 'число формата сотни следует после десятичного формата'


@mark.parametrize(
    'number_text,number',
    chain(gen_cases_after_tens(), *[gen_cases_after_tens(REVERSED_DIGITS[number]) for number in range(2, 10)]),
)
def test_incorrect_values_after_tens(number_text, number):
    assert convert_text(number_text) == number
