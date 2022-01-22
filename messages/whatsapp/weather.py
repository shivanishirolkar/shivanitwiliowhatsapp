import calendar
from datetime import datetime
import requests

def generate_weather_message(weather_request):
    current_weather = {
        "temperature": int(weather_request["current"]["temp"]),
        "day_of_week": calendar.day_name[datetime.fromtimestamp(weather_request["current"]["dt"]).weekday()],
        "description": weather_request["current"]["weather"][0]["description"],
        "main": weather_request["current"]["weather"][0]["main"]
    }

    forecast_messages = []
    for daily_weather in weather_request["daily"]:
        max_temp = daily_weather["temp"]["max"]
        min_temp = daily_weather["temp"]["min"]
        weekday = calendar.day_name[datetime.fromtimestamp(daily_weather["dt"]).weekday()]
        description = daily_weather["weather"][0]["description"]
        forecast_message = f"{weekday}: {description}, " \
                           f"Low {min_temp}°F, High {max_temp}°F  \n"
        forecast_messages.append(forecast_message)
    forecast_messages = "\n".join(forecast_messages)
    message = f"*Current Weather* \n \n"\
                   f"{current_weather['day_of_week']}: "\
                   f"{current_weather['description']}, "\
                   f"{current_weather['temperature']} °F \n \n"\
                   f"*Forecast* \n \n"\
                   f"{forecast_messages}"

    return message

def get_weather(lat, lon, api_key):
    weather_request = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly&appid={api_key}&units=imperial").json()
    print(weather_request)
    return weather_request