from src.main import json_read, mask_operation_to, mask_operation_from, sort_operation, filter_operation, format_date

import pytest


@pytest.fixture
def test_state():
    return [{"state": "EXECUTED"}, {"state": "EXECUTED"}, {"state": "CANCELLED"}]


@pytest.fixture
def test_data():
    return [{"date": "2019-08-26T10:50:58.294041"},
            {"date": "2018-06-30T02:08:58.425572"},
            {"date": "2019-04-04T23:20:05.206878"}
            ]


def test_json_read():
    assert json_read('test_json.json') == {"test": "test"}
    assert type(json_read('test_json.json')) == dict


def test_filter_operation(test_state):
    assert filter_operation(test_state) == [{"state": "EXECUTED"}, {"state": "EXECUTED"}]
    assert len(filter_operation(test_state)) == 2
    assert type(filter_operation(test_state)) == list


def test_sort_operation(test_data):
    assert sort_operation(test_data) == [{"date": "2019-08-26T10:50:58.294041"},
                                         {"date": "2019-04-04T23:20:05.206878"},
                                         {"date": "2018-06-30T02:08:58.425572"},
                                         ]


def test_format_date():
    assert format_date({"date": "2018-10-14T08:21:33.419441"}) == '14.10.2018'
    assert type(format_date({"date": "2018-10-14T08:21:33.419441"})) == str


def test_mask_operation_from():
    assert mask_operation_from({"from": "Счет 19708645243227258542"}) == "Счет **8542 ->"
    assert mask_operation_from({}) == "Без номера ->"
    assert mask_operation_from({"from": "Visa Classic 6831982476737658"}) == "Visa Classic 6831 98** **** 7658 ->"


def test_mask_operation_to():
    assert mask_operation_to({"to": "Счет 84163357546688983493"}) == "Счет **3493"
