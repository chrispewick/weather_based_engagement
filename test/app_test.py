import json
from datetime import datetime
from app import weather


def test_daily_forecasts():
    with open('/Users/chrispewick/PycharmProjects/request_test/test/sample_response.json') as json_file:
        forecast_list = json.load(json_file)['list']
        daily_forecasts = weather.get_daily_forecasts(forecast_list)
        assert isinstance(daily_forecasts, list)
        assert 5 == len(daily_forecasts)


def test_get_contact_method_when_temp_above_75_and_raining():
    data = [dict(date=datetime(2020, 2, 18), avg_temp=85.1, is_rainy=True, is_sunny=False)]
    result = weather.get_contact_method(data)
    assert isinstance(result, list)
    assert 1 == len(result)
    assert 'call' == result[0]['method']


def test_get_contact_method_when_temp_above_75():
    data = [dict(date=datetime(2020, 2, 18), avg_temp=85.1, is_rainy=False, is_sunny=False)]
    result = weather.get_contact_method(data)
    assert isinstance(result, list)
    assert 1 == len(result)
    assert 'text' == result[0]['method']


def test_get_contact_method_when_temp_below_55():
    data = [dict(date=datetime(2020, 2, 18), avg_temp=5.1, is_rainy=False, is_sunny=False)]
    result = weather.get_contact_method(data)
    assert isinstance(result, list)
    assert 1 == len(result)
    assert 'call' == result[0]['method']


def test_get_contact_method_when_temp_between_55_and_75():
    data = [dict(date=datetime(2020, 2, 18), avg_temp=65.1, is_rainy=False, is_sunny=False)]
    result = weather.get_contact_method(data)
    assert isinstance(result, list)
    assert 1 == len(result)
    assert 'email' == result[0]['method']


def test_get_contact_method_when_temp_between_55_and_75_and_raining():
    data = [dict(date=datetime(2020, 2, 18), avg_temp=65.1, is_rainy=True, is_sunny=False)]
    result = weather.get_contact_method(data)
    assert isinstance(result, list)
    assert 1 == len(result)
    assert 'call' == result[0]['method']


def test_with_sample():
    with open('/Users/chrispewick/PycharmProjects/request_test/test/sample.json') as json_file:
        forecast_list = json.load(json_file)['list']
        daily_forecasts = weather.get_daily_forecasts(forecast_list)
        assert isinstance(daily_forecasts, list)
        assert 5 == len(daily_forecasts)
        daily_averages = weather.get_daily_averages(daily_forecasts)
        assert isinstance(daily_averages, list)
        assert 5 == len(daily_averages)
        results = weather.get_contact_method(daily_averages)
        assert isinstance(results, list)
        assert 5 == len(results)
        assert 'call' == results[0]['method']
        assert 'text' == results[1]['method']
        assert 'call' == results[2]['method']
        assert 'email' == results[3]['method']
        assert 'call' == results[4]['method']
