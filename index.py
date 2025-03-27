import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from environment variable
API_KEY = os.getenv("API_KEY")

def get_weather(city):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    if not API_KEY:
        print("❌ Error: API key is missing. Please check your .env file.")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "weather" in data and "main" in data:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            print(f"\n✅ Weather in {city.capitalize()}:")
            print(f"🌡 Temperature: {temp}°C")
            print(f"💧 Humidity: {humidity}%")
            print(f"☁ Condition: {weather_desc.capitalize()}\n")
        else:
            print("❌ Error: Could not retrieve weather details.")

    except requests.exceptions.ConnectionError:
        print("❌ Error: No internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Error: The request timed out.")
    except requests.exceptions.HTTPError as err:
        if response.status_code == 401:
            print("❌ Error: Invalid API key. Check your .env file.")
        elif response.status_code == 404:
            print("❌ Error: City not found.")
        else:
            print(f"❌ HTTP Error: {err}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

# User input for city name
if __name__ == "__main__":
    city_name = input("🌍 Enter city name: ")
    get_weather(city_name)
