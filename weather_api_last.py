import argparse
import requests
import configparser
import logging
import csv

class WeatherForecastApp:

    def __init__(self):
        self.weather_base_url = "http://api.weatherapi.com/v1/forecast.json"
        self.args = self.parse_arguments()
        self.api_key = self.read_api_key()

        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename='weather.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    # def parse_arguments(self):
    #     parser = argparse.ArgumentParser(description="Fetch weather forecast for multiple cities.")
    #     parser.add_argument("cities", nargs="+", type=str, help="Names of the cities (separated by spaces)")
    #     parser.add_argument("days", type=int, help="Number of days of forecast (maximum 3)")
    #     return parser.parse_args()
    

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Fetch weather forecast for multiple cities.")
        parser.add_argument("cities", nargs="*", default=["London"], type=str, help="Names of the cities (separated by spaces)")
        parser.add_argument("days", default=1, type=int, help="Number of days of forecast (maximum 3)")
        return parser.parse_args()

    def read_api_key(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config.get("API", "key")

    def fetch_weather_data(self, api_key, city_name, days):

        print(city_name)
        try :
            params = {"key": api_key, "q": city_name, "days": days}
            response = requests.get("http://api.weatherapi.com/v1/forecast.json", params=params)
            print('response', response)
            r = response.json()
            # print('response r', r)
            
            self.log_info(f"Requesting weather data for {city_name} - Response code: {response.status_code}")

            if response.status_code == 200:
                #(r)
                return (r)
                
            else:
                self.log_error(f"Error fetching weather data for {city_name}: {response.status_code}, {response.text}")
                return None
        except (requests.exceptions.RequestException,requests.exceptions.HTTPError ,ValueError,Exception) as e:
            print(f"Error occurred during the request: {e}")


    def parse_weather_data(self, json_data):
        if not json_data:
            return None
            

        forecast_details = []
        forecast_days = json_data["forecast"]["forecastday"]

        for day in forecast_days:
            date = day["date"]
            max_temp = day["day"]["maxtemp_c"]
            min_temp = day["day"]["mintemp_c"]
            condition = day["day"]["condition"]["text"]

            forecast_details.append({
                "date": date,
                "max_temp": max_temp,
                "min_temp": min_temp,
                "condition": condition
            })

        return forecast_details

    def print_weather_details(self, city, forecast_details):
        if forecast_details:
            print(f"Weather forecast for {city}:")
            for day_data in forecast_details:
                print(f"Date: {day_data['date']}")
                print(f"Max Temperature: {day_data['max_temp']}°C")
                print(f"Min Temperature: {day_data['min_temp']}°C")
                print(f"Condition: {day_data['condition']}\n")
        else:
            print(f"Unable to fetch weather data for {city}. Please check your inputs and try again.")

    def write_to_csv(self, city, forecast_details):
        if forecast_details:
            csv_filename = f"{city}_weather_forecast.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                fieldnames = ["Date", "Max Temperature (°C)", "Min Temperature (°C)", "Condition"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for day_data in forecast_details:
                    writer.writerow({
                        "Date": day_data["date"],
                        "Max Temperature (°C)": day_data["max_temp"],
                        "Min Temperature (°C)": day_data["min_temp"],
                        "Condition": day_data["condition"]
                    })

            print(f"Weather forecast data for {city} has been written to {csv_filename}")
        else:
            print(f"No weather data available for {city} to write to CSV.")

    def main(self):
        for city in self.args.cities:
            weather_data = self.fetch_weather_data(self.api_key, city, self.args.days)
            forecast_details = self.parse_weather_data(weather_data)
            self.print_weather_details(city, forecast_details)
            self.write_to_csv(city, forecast_details)

if __name__ == "__main__":
    app = WeatherForecastApp()
    app.main()
