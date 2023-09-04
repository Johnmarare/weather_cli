import sys
import unittest
from unittest.mock import patch

sys.path.append('../')

import weather

class TestWeatherApp(unittest.TestCase):

    def setUp(self):
        # Disable sys.exit() calls during tests
        self.mock_exit = self.create_patch('sys.exit')

    def create_patch(self, name):
        mock = patch(name)
        self.addCleanup(mock.stop)
        return mock.start()

    def test_get_weather_data_404_error(self):
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = weather.error.HTTPError(
                "url", 404, "Not Found", None, None
            )
            with self.assertRaises(SystemExit):
                weather.get_weather_data("url")
        self.mock_exit.assert_called_once_with("Can't find weather data for this location.")

    def test_get_weather_data_401_error(self):
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = weather.error.HTTPError(
                "url", 401, "Unauthorized", None, None
            )
            with self.assertRaises(SystemExit):
                weather.get_weather_data("url")
        self.mock_exit.assert_called_once_with("Access denied. Check your API key.")

    def test_get_weather_data_other_http_error(self):
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = weather.error.HTTPError(
                "url", 500, "Internal Server Error", None, None
            )
            with self.assertRaises(SystemExit):
                weather.get_weather_data("url")
        self.mock_exit.assert_called_once_with("Something went wrong... (HTTPError() got an unexpected keyword argument 'code')")

    # Add more test cases for other error scenarios

    def test_read_user_cli_args_no_city(self):
        with patch('sys.argv', ['weather.py']):
            with self.assertRaises(SystemExit) as cm:
                with patch('sys.argv', ['weather.py']):
                    with self.assertRaises(SystemExit):
                        weather.read_user_cli_args()
        self.assertEqual(cm.exception.code, "Please provide the name of a city.")

    # Add more test cases for other error scenarios

if __name__ == '__main__':
    unittest.main()
