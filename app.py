import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests
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

def get_weather_data(city, country):
    weather_data = fetch_weather_data_by_city(city, country)
    if weather_data:
        return weather_data
    else:
        messagebox.showerror("Error", f"No weather data found for {city}, {country}")
        return None

def show_weather_data():
    city = entry_city.get()
    country = entry_country.get()

    weather_data = get_weather_data(city, country)
    if weather_data:
        weather = weather_data['weather'][0]['main']
        temp = round(weather_data['main']['temp'])

        if 'rain' in weather_data:
            precipitation = weather_data['rain']
            precipitation_text = f"The precipitation is: {precipitation} mm"
        elif 'snow' in weather_data:
            precipitation = weather_data['snow']
            precipitation_text = f"The precipitation is: {precipitation} mm"
        else:
            precipitation_text = "No precipitation data available"

        weather_text = f"The weather is: {weather}"
        temperature_text = f"The temperature is: {temp}ºF"

        label_weather.config(text=weather_text)
        label_temperature.config(text=temperature_text)
        label_precipitation.config(text=precipitation_text)

def on_submit():
    show_weather_data()

# Create the main window
root = tk.Tk()
root.title("Weather Information")

# Create widgets
label_city = tk.Label(root, text="City:")
label_country = tk.Label(root, text="Country:")
entry_city = tk.Entry(root)
entry_country = tk.Entry(root)
button_submit = tk.Button(root, text="Get Weather", command=on_submit)
label_weather = tk.Label(root, text="")
label_temperature = tk.Label(root, text="")
label_precipitation = tk.Label(root, text="")

# Arrange widgets using grid layout
label_city.grid(row=0, column=0, padx=10, pady=10)
entry_city.grid(row=0, column=1, padx=10, pady=10)
label_country.grid(row=1, column=0, padx=10, pady=10)
entry_country.grid(row=1, column=1, padx=10, pady=10)
button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
label_weather.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
label_temperature.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
label_precipitation.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Start the main loop
root.mainloop()
