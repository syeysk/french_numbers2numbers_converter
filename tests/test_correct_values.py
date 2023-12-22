from pytest import mark

from main import convert_text


dataset = [
    ('zéro', 0),
    ('deux', 2),
    ('dix', 10),
    ('onze', 11),
    ('dix-neuf', 19),
    ('vingt', 20),
    ('vingt et un', 21),
    ('vingt-trois', 23),
    ('soixante et un', 61),
    ('soixante-trois', 63),
    ('quatre-vingt-un', 81),
    ('quatre-vingt-trois', 83),
    ('quatre-vingt-dix', 90),
    ('soixante et onze', 71),
    ('soixante-douze', 72),
    ('soixante-dix-sept', 77),
    ('quatre-vingt-onze', 91),
    ('quatre-vingt-douze', 92),
    ('quatre-vingt-dix-sept', 97),
    ('deux cents', 200),
    ('quatre cents', 400),
    ('cent deux', 102),
    ('deux cent trois', 203),
]


@mark.parametrize('number_text,number', dataset)
def test_convert_right_values(number_text, number):
    assert convert_text(number_text) == number


@mark.parametrize('number_text,number', [('soixante    et  un', 61), ('  vingt \net un\t', 21)])
def test_spaces(number_text, number):
    assert convert_text(number_text) == number
