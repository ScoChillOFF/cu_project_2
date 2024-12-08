def is_weather_good(conditions: dict) -> bool:
    """Returns True if weather is 'good'"""
    return all([
        0 <= conditions["temperature"] <= 35,
        conditions["wind_speed"] <= 50,
        conditions["probability_of_precipitation"] <= 70
    ])


def get_weather_verdict(conditions: dict) -> str:
    """Returns string describing whether the weather is good or not"""
    if is_weather_good(conditions):
        return "Самое время для прогулки!"
    else:
        return "Прогулка сегодня не самый лучший выбор."