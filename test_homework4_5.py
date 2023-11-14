import urllib.request
import json
from unittest.mock import patch


API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год

    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


def test_ymd_format():
    with patch('json.load') as mock_json:
        mock_json.return_value.json = lambda: ('{"$id":"1",'
                                               '"currentDateTime":"2023-11-07T20:12Z",'
                                               '"utcOffset":"00:00:00",'
                                               '"isDayLightSavingsTime":false,'
                                               '"dayOfTheWeek":"Tuesday",'
                                               '"timeZoneName":"UTC",'
                                               '"currentFileTime":133438615432836090,'
                                               '"ordinalDate":"2023-311",'
                                               '"serviceResponse":null}', 2023)
    assert what_is_year_now() == 2023


def test_dmy_format():
    with patch('json.load') as mock_json:
        mock_json.return_value.json = lambda: ('{"$id":"1",'
                                               '"currentDateTime":"2023-11-07T20:12Z",'
                                               '"utcOffset":"00:00:00",'
                                               '"isDayLightSavingsTime":false,'
                                               '"dayOfTheWeek":"Tuesday",'
                                               '"timeZoneName":"UTC",'
                                               '"currentFileTime":133438615432836090,'
                                               '"ordinalDate":"2023-311",'
                                               '"serviceResponse":null}', 2023)
    assert what_is_year_now() == 2023


def test_invalid_format():
    with patch('json.load') as mock_json:
        mock_json.return_value.json = lambda: ('{"$id":"1",'
                                               '"currentDateTime":"2023-11-07T20:12Z",'
                                               '"utcOffset":"00:00:00",'
                                               '"isDayLightSavingsTime":false,'
                                               '"dayOfTheWeek":"Tuesday",'
                                               '"timeZoneName":"UTC",'
                                               '"currentFileTime":133438615432836090,'
                                               '"ordinalDate":"2023-311",'
                                               '"serviceResponse":null}', 2023)
        try:
            assert what_is_year_now() == ValueError
        except ValueError:
            pass


if __name__ == '__main__':  # pragma: no cover
    year = what_is_year_now()
    exp_year = 2023

    print(year)
    assert year == exp_year
