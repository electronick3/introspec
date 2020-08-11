import pytest
from introspec import _trim


def test_trim_name():
    assert _trim('TestString  ', 20) == 'TestString  '


def test_trim_big_name():
    bigString = 'TestStriiiiiiiiiiiiiiiiing'
    assert _trim(bigString, 20) == 'TestStriiiiiiiiiiiii'


def test_trim_text():
    bigString = 'TestStriiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiing'
    assert _trim(bigString, 79) == 'TestStriiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiing'


def test_trim_big_text():
    bigString = 'TestStriiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiing'
    assert _trim(bigString, 79) == 'TestStriiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii...'
