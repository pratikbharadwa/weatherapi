import unittest
from unittest.mock import MagicMock, patch,Mock
from weather_api_last import WeatherForecastApp

class TestWeatherForecast(unittest.TestCase):
    # Test fetch_weather_data method

    

    # def test_fetch_weather_data(self):
    #     # Mocking the response from the API
    #     mock_response = MagicMock()
    #     mock_response.status_code = 200
    #     mock_response.json.return_value = {"forecast": {"forecastday": [{"date": "2023-08-04", "day": {"maxtemp_c": 25, "mintemp_c": 18, "condition": {"text": "Cloudy"}}}]}}
    #     with patch('requests.get') as apiRequest:
    #         apiRequest.return_value = {"forecastday": [{"date": "2023-08-04", "day": {"maxtemp_c": 25, "mintemp_c": 18, "condition": {"text": "Cloudy"}}}]}
    #         data = self.weatherr_apii.fetch_weather_data(self,'65a1fe7bb1ff43619e8130922232107','London',1)
    #         self.assertEqual(data, {"forecast": {"forecastday": [{"date": "2023-08-04", "day": {"maxtemp_c": 25, "mintemp_c": 18, "condition": {"text": "Cloudy"}}}]}})

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[API]\nkey=mocked_api_key')
    @patch('requests.get')
    def test_fetch_weather_data(self, mock_get, mock_open, mock_parse_args):
        # Create a mock response object for requests.get
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "forecast": {
                "forecastday": [
                    {
                        "date": "2023-08-10",
                        "day": {
                            "maxtemp_c": 25,
                            "mintemp_c": 15,
                            "condition": {"text": "Sunny"}
                        }
                    }
                ]
            }
        }
        mock_get.return_value = mock_response
        
        # Mock the parsed arguments
        mock_parse_args.return_value = Mock(cities=["London"], days=1)
        
        # Create an instance of WeatherForecastApp
        app = WeatherForecastApp()
        
        # Fetch weather data using the mocked response
        weather_data = app.fetch_weather_data("mocked_api_key", "London", 1)
        
        # Assert the result
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data["forecast"]["forecastday"][0]["date"], "2023-08-10")
        self.assertEqual(weather_data["forecast"]["forecastday"][0]["day"]["maxtemp_c"], 25)
        self.assertEqual(weather_data["forecast"]["forecastday"][0]["day"]["mintemp_c"], 15)
        self.assertEqual(weather_data["forecast"]["forecastday"][0]["day"]["condition"]["text"], "Sunny")

    

    # Test parse_weather_data method
    def test_parse_weather_data(self):
        json_data = {"forecast": {"forecastday": [{"date": "2023-08-04", "day": {"maxtemp_c": 25, "mintemp_c": 18, "condition": {"text": "Cloudy"}}}]}}
        expected_result = [{"date": "2023-08-04", "max_temp": 25, "min_temp": 18, "condition": "Cloudy"}]
        result = WeatherForecastApp.parse_weather_data(self,json_data)
        self.assertEqual(result, expected_result)

    
if __name__ == '__main__':
    unittest.main()
