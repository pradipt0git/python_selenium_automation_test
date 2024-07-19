import pytest

def test_first_scenario():
    a=5
    b=6
    assert a==get_data()

def second_scenario():
    a=7
    b=7
    assert a==b

def get_data():
    return 40
