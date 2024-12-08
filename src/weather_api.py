import requests


API_KEY = "CKTWrDEbHaXRGa8Sc5WlHRGNmsxktzPP"
BASE_URL = "http://dataservice.accuweather.com"


def get_forecast(location_key: str) -> dict | None:
    """Returns 1-day forecast response in JSON format. If any error prints it and returns None"""
    url = f"{BASE_URL}/forecasts/v1/daily/1day/{location_key}?apikey={API_KEY}&details=true&metric=true"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('DailyForecasts', [None])[0] # If no key, return None as first element of a list
    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения данных о прогнозе: {e}")
        return None


def get_location_key(city: str) -> str | None:
    """Returns location key for further requests. If any error prints it and returns None"""
    location_url = f"{BASE_URL}/locations/v1/cities/search?apikey={API_KEY}&q={city}"
    try:
        response = requests.get(location_url)
        response.raise_for_status()
        location_data = response.json()
        return location_data[0]["Key"] if location_data else None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения данных для города '{city}': {e}")
        return None


def get_weather(location_key: str) -> dict | None:
    """Returns weather info in JSON format. If error prints it and returns None"""
    weather_url = f'{BASE_URL}/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true'
    try:
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        return weather_data[0] if weather_data else None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения данных о погоде: {e}")
        return None


def get_conditions(city: str) -> dict | None:
    """Requests weather data and extracts conditions from it. If weather or forecast is not available returns None"""
    location_key = get_location_key(city)
    if not location_key:
        return None
    weather_data = get_weather(location_key)
    forecast_data = get_forecast(location_key)
    if not weather_data or not forecast_data:
        return None

    temperature = weather_data["Temperature"]["Metric"]["Value"]
    wind_speed = weather_data["Wind"]["Speed"]["Metric"]["Value"]
    probability_of_precipitation = forecast_data["Day"].get("PrecipitationProbability")
    humidity = weather_data['RelativeHumidity']

    return {
        "temperature": temperature,
        "wind_speed": wind_speed,
        "probability_of_precipitation": probability_of_precipitation,
        "humidity": humidity,
    }
