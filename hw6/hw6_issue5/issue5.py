import json
import urllib.request
import unittest
from unittest.mock import patch
import io

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



class Test_what_is_year_now(unittest.TestCase):
    def test_first_format(self):
        dict_for_json = '{"currentDateTime": "2010-10-10"}'

        with patch.object(urllib.request, "urlopen", return_value=io.StringIO(dict_for_json)):
            actual = what_is_year_now()
        expected = 2010
        self.assertEqual(actual, expected)

    def test_second_format(self):
        dict_for_json = '{"currentDateTime": "10.10.2010"}'

        with patch.object(urllib.request, "urlopen", return_value=io.StringIO(dict_for_json)):
            actual = what_is_year_now()
        expected = 2010
        self.assertEqual(actual, expected)

    def test_exception(self):
        dict_for_json = '{"currentDateTime": "two thousand and ten"}'

        with patch.object(urllib.request, "urlopen", return_value=io.StringIO(dict_for_json)):
            with self.assertRaises(ValueError):
                what_is_year_now()


if __name__ == '__main__':
    unittest.main()
