import requests
from datetime import datetime
import configparser
import os

# Read API key from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

api_key = config.get('openweathermap', 'api_key')

def fetch_weather_data_by_coords(lat, lon, date_time=None):
    if date_time:
        date_unix = int(date_time.timestamp())
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&dt={date_unix}&exclude=current,minutely,hourly&appid={api_key}'
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_weather_data_by_city(city, country):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=imperial&APPID={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    while True:
        user_input = input("Enter 1 to get weather data by city, 2 to get hourly data by coordinates, or 'exit' to quit: ")
        
        if user_input.lower() == 'exit':
            break
        elif user_input == '1':
            city_country = input("Enter city and country (e.g., Kingston, JM): ")
            city, country = map(str.strip, city_country.split(','))
            weather_data = fetch_weather_data_by_city(city, country)
            if weather_data:
                print(weather_data)
                weather = weather_data['weather'][0]['main']
                temp = round(weather_data['main']['temp'])
                
                if 'rain' in weather_data:
                    precipitation = weather_data['rain']
                    print(f"The precipitation in {city} ({country}) is: {precipitation} mm")
                elif 'snow' in weather_data:
                    precipitation = weather_data['snow']
                    print(f"The precipitation in {city} ({country}) is: {precipitation} mm")
                else:
                    print(f"No precipitation data available for {city} ({country})")
                
                print(f"The weather in {city} ({country}) is: {weather}")
                print(f"The temperature in {city} ({country}) is: {temp}ºF")
            else:
                print(f"No weather data found for {city}, {country}")
        
        elif user_input == '2':
            lat = float(input("Enter latitude: "))
            lon = float(input("Enter longitude: "))
            date_time_str = input("Enter date and time (YYYY-MM-DD HH:MM:SS) or press Enter for current time: ")
            
            if date_time_str:
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            else:
                date_time = None
            
            weather_data = fetch_weather_data_by_coords(lat, lon, date_time)
            
            if weather_data:
                print(weather_data)
                hourly_data = weather_data.get('hourly', [])
                if hourly_data:
                    while True:
                        try:
                            hour_filter = int(input("Enter the hour (1-24) to see detailed weather or 'exit': "))
                            if hour_filter < 1 or hour_filter > 24:
                                print("Please enter a valid hour between 1 and 24.")
                                continue
                            else:
                                print(f"Weather details for hour {hour_filter}:")
                                print(hourly_data[hour_filter - 1])
                        except ValueError:
                            if input("Invalid input. Enter 'exit' to quit or press Enter to try again: ").lower() == 'exit':
                                break
                            continue
            else:
                print("No weather data found for the given coordinates.")
        
        else:
            print("Invalid input. Please enter 1, 2, or 'exit'.")

if __name__ == "__main__":
    main()
