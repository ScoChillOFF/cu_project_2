import json
import socket


def is_connected() -> bool:
    """Checks if Internet is available"""
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False


def save_cities_weathers(cities_weather: list) -> None:
    """Saves all weather data into JSON files. Each city separate"""
    for i, city in enumerate(cities_weather):
        with open(f"city_{i}.json", "w", encoding="utf-8") as file:
            json.dump(city, file)
